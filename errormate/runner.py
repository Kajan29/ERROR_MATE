from dataclasses import dataclass
import os
from pathlib import Path
import queue
import subprocess
import threading
from typing import Optional

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

    def run(self, command: str, framework: str, cwd: Path, shell: str = "auto") -> ExecutionResult:
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

        stream_queue: queue.Queue[tuple[str, str]] = queue.Queue()
        stdout_lines: list[str] = []
        stderr_lines: list[str] = []
        output_lines: list[str] = []

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
        except KeyboardInterrupt:
            self.console.print("[yellow]Stopping command...[/yellow]")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

        exit_code = process.wait()
        combined_output = "".join(output_lines)
        detected_error = self.classifier.classify(combined_output, framework)

        return ExecutionResult(
            command=command,
            exit_code=exit_code,
            stdout="".join(stdout_lines),
            stderr="".join(stderr_lines),
            output=combined_output,
            framework=framework,
            detected_error=detected_error,
        )
