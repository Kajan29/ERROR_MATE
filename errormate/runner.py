from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import queue
import subprocess
import threading
from typing import Callable, Optional, Sequence

from rich.console import Console
from rich.panel import Panel

from errormate.error_classifier import ErrorClassifier, ErrorReport
from errormate.utils.output_formatter import style_stream_line


@dataclass
class ExecutionResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str
    output: str
    framework: str
    detected_error: Optional[ErrorReport]
    detected_errors: list[ErrorReport]


def build_shell_invocation(command: str, shell_mode: str = "auto") -> list[str]:
    shell_mode = shell_mode.lower().strip()
    if shell_mode not in {"auto", "powershell", "bash"}:
        raise ValueError("shell must be one of: auto, powershell, bash")

    if shell_mode == "auto":
        shell_mode = "powershell" if os.name == "nt" else "bash"

    if shell_mode == "powershell":
        return ["powershell", "-NoProfile", "-Command", command]

    return ["bash", "-lc", command]


class CommandRunner:
    def __init__(self, console: Optional[Console] = None, classifier: Optional[ErrorClassifier] = None) -> None:
        self.console = console or Console()
        self.classifier = classifier or ErrorClassifier()

    def run(
        self,
        command: str,
        framework: str,
        cwd: Path,
        shell: str = "auto",
        on_new_errors: Optional[Callable[[list[ErrorReport]], None]] = None,
    ) -> ExecutionResult:
        stream_queue: queue.Queue[tuple[str, str]] = queue.Queue()
        stdout_lines: list[str] = []
        stderr_lines: list[str] = []
        output_lines: list[str] = []
        live_detected_errors: list[ErrorReport] = []
        last_live_error_signature: tuple[tuple[str, str, str], ...] | None = None

        try:
            invocation = build_shell_invocation(command, shell)
            self.console.print(Panel.fit(f"Running: [bold]{command}[/bold]", title="ErrorMate"))

            process = subprocess.Popen(
                invocation,
                cwd=str(cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )
        except Exception as error:
            return self._build_runtime_failure_result(
                command=command,
                framework=framework,
                stdout_lines=stdout_lines,
                stderr_lines=stderr_lines,
                output_lines=output_lines,
                stage="starting command",
                error=error,
            )

        def stream_reader(stream, source: str) -> None:
            for line in iter(stream.readline, ""):
                stream_queue.put((source, line))
            stream.close()

        stdout_thread = threading.Thread(target=stream_reader, args=(process.stdout, "stdout"), daemon=True)
        stderr_thread = threading.Thread(target=stream_reader, args=(process.stderr, "stderr"), daemon=True)
        stdout_thread.start()
        stderr_thread.start()

        try:
            while stdout_thread.is_alive() or stderr_thread.is_alive() or not stream_queue.empty():
                try:
                    source, line = stream_queue.get(timeout=0.1)
                except queue.Empty:
                    continue

                output_lines.append(line)
                if source == "stderr":
                    stderr_lines.append(line)
                else:
                    stdout_lines.append(line)

                self.console.print(style_stream_line(source, line))

                if on_new_errors is not None:
                    last_live_error_signature = self._emit_live_errors(
                        framework=framework,
                        cwd=cwd,
                        output_lines=output_lines,
                        last_live_error_signature=last_live_error_signature,
                        live_errors=live_detected_errors,
                        on_new_errors=on_new_errors,
                    )
        except KeyboardInterrupt:
            self.console.print("[yellow]Stopping command...[/yellow]")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        except Exception as error:
            try:
                process.terminate()
            except Exception:
                pass
            return self._build_runtime_failure_result(
                command=command,
                framework=framework,
                stdout_lines=stdout_lines,
                stderr_lines=stderr_lines,
                output_lines=output_lines,
                stage="reading command output",
                error=error,
            )

        exit_code = process.wait()
        combined_output = "".join(output_lines)
        try:
            detected_errors = self.classifier.classify_all(combined_output, framework, project_path=cwd)
        except Exception as error:
            runtime_report = self.classifier.runtime_error_report(framework, error, "classifying command output")
            detected_errors = [runtime_report]

        detected_errors = self._merge_reports(live_detected_errors, detected_errors)

        detected_error = detected_errors[0] if detected_errors else None

        return ExecutionResult(
            command=command,
            exit_code=exit_code,
            stdout="".join(stdout_lines),
            stderr="".join(stderr_lines),
            output=combined_output,
            framework=framework,
            detected_error=detected_error,
            detected_errors=detected_errors,
        )

    def _emit_live_errors(
        self,
        framework: str,
        cwd: Path,
        output_lines: list[str],
        last_live_error_signature: tuple[tuple[str, str, str], ...] | None,
        live_errors: list[ErrorReport],
        on_new_errors: Callable[[list[ErrorReport]], None],
    ) -> tuple[tuple[str, str, str], ...] | None:
        try:
            stream_reports = self.classifier.classify_all("".join(output_lines), framework, project_path=cwd)
        except Exception:
            return last_live_error_signature

        if not stream_reports:
            return last_live_error_signature

        current_signature = tuple(sorted(self._report_key(report) for report in stream_reports))
        if current_signature == last_live_error_signature:
            return last_live_error_signature

        live_errors.extend(stream_reports)

        try:
            on_new_errors(stream_reports)
        except Exception:
            return current_signature

        return current_signature

    @staticmethod
    def _report_key(report: ErrorReport) -> tuple[str, str, str]:
        return (report.error_type, report.main_error, report.excerpt.lower())

    def _merge_reports(self, *report_groups: Sequence[ErrorReport]) -> list[ErrorReport]:
        merged_by_key: dict[tuple[str, str, str], ErrorReport] = {}
        ordered_keys: list[tuple[str, str, str]] = []

        for reports in report_groups:
            for report in reports:
                key = self._report_key(report)
                if key not in merged_by_key:
                    merged_by_key[key] = report
                    ordered_keys.append(key)
                    continue

                existing = merged_by_key[key]
                if self._report_richness(report) > self._report_richness(existing):
                    merged_by_key[key] = report

        return [merged_by_key[key] for key in ordered_keys]

    @staticmethod
    def _report_richness(report: ErrorReport) -> int:
        score = 0
        if report.root_cause and report.root_cause != report.excerpt:
            score += 1
        if report.source_file:
            score += 2
        if report.source_line is not None:
            score += 1
        if report.source_folder:
            score += 1
        if report.source_kind == "exact":
            score += 3
        elif report.source_kind == "likely":
            score += 1
        score += min(len(report.related_files), 3)
        score += min(len(report.related_folders), 2)
        return score

    def _build_runtime_failure_result(
        self,
        command: str,
        framework: str,
        stdout_lines: list[str],
        stderr_lines: list[str],
        output_lines: list[str],
        stage: str,
        error: Exception,
    ) -> ExecutionResult:
        runtime_report = self.classifier.runtime_error_report(framework, error, stage)
        return ExecutionResult(
            command=command,
            exit_code=1,
            stdout="".join(stdout_lines),
            stderr="".join(stderr_lines),
            output="".join(output_lines),
            framework=framework,
            detected_error=runtime_report,
            detected_errors=[runtime_report],
        )
