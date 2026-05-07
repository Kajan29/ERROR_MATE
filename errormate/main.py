from __future__ import annotations

import os
import platform
import sys
from pathlib import Path

MIN_PYTHON = (3, 8)


def _detect_linux_distro() -> str:
    """Detect which Linux distro is running."""
    try:
        with open("/etc/os-release", encoding="utf-8") as f:
            content = f.read().lower()
        if "ubuntu" in content or "debian" in content or "mint" in content:
            return "debian"
        if "fedora" in content or "centos" in content or "rhel" in content or "rocky" in content or "alma" in content:
            return "fedora"
        if "arch" in content or "manjaro" in content or "endeavour" in content:
            return "arch"
        if "suse" in content or "opensuse" in content:
            return "suse"
    except Exception:
        pass
    return "unknown"


def _print_python_install_guide() -> None:
    """Print OS-specific Python installation instructions."""
    _v = f"{sys.version_info.major}.{sys.version_info.minor}"
    _need = f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]}"
    print(f"\n[ErrorMate] Python {_need}+ is required. You have Python {_v}.\n")

    system = platform.system().lower()

    if system == "windows":
        print("How to install/upgrade Python on Windows:")
        print("  1. Go to https://www.python.org/downloads/")
        print("  2. Download the latest Python installer")
        print('  3. Run the installer (check "Add Python to PATH")')
        print("  4. Restart your terminal")
        print(f"  5. Verify: python --version\n")

    elif system == "darwin":
        print("How to install/upgrade Python on macOS:")
        print("  brew update")
        print("  brew install python")
        print("")
        print("  If you don't have Homebrew:")
        print('  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
        print(f"\n  Then verify: python3 --version\n")

    elif system == "linux":
        distro = _detect_linux_distro()
        print("How to install/upgrade Python on Linux:\n")

        if distro == "debian":
            print("  Detected: Ubuntu/Debian-based system")
            print("    sudo apt update")
            print("    sudo apt install python3 python3-pip -y")
        elif distro == "fedora":
            print("  Detected: Fedora/CentOS/RHEL-based system")
            print("    sudo dnf upgrade --refresh -y")
            print("    sudo dnf install python3 python3-pip -y")
        elif distro == "arch":
            print("  Detected: Arch-based system")
            print("    sudo pacman -Syu")
            print("    sudo pacman -S python python-pip")
        elif distro == "suse":
            print("  Detected: openSUSE-based system")
            print("    sudo zypper refresh")
            print("    sudo zypper install python3 python3-pip")
        else:
            print("  Ubuntu/Debian:")
            print("    sudo apt update")
            print("    sudo apt install python3 python3-pip -y")
            print("")
            print("  Fedora/CentOS:")
            print("    sudo dnf upgrade --refresh -y")
            print("    sudo dnf install python3 python3-pip -y")
            print("")
            print("  Arch Linux:")
            print("    sudo pacman -Syu")
            print("    sudo pacman -S python python-pip")

        print(f"\n  Then verify: python3 --version\n")

    else:
        print(f"  Visit https://www.python.org/downloads/ to install Python {_need}+\n")


if sys.version_info < MIN_PYTHON:
    _print_python_install_guide()
    sys.exit(1)

import typer
from rich.console import Console
from rich.panel import Panel

from errormate import __version__
from errormate.ai_explainer import get_ai_explanation
from errormate.error_classifier import ErrorReport
from errormate.error_explainer import build_error_panel
from errormate.framework_detector import detect_framework
from errormate.runner import CommandRunner
from errormate.terminal import show_errors_in_new_terminal


def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"ErrorMate v{__version__}")
        raise typer.Exit()


app = typer.Typer(add_completion=False, help="Run dev commands and detect errors with rule-based matching.")
console = Console()


@app.command("run")
def run_command(
    command: str = typer.Argument(..., help="Command to run, for example: npm run dev"),
    project_path: Path = typer.Option(Path.cwd(), "--project-path", "-p", help="Project directory."),
    shell: str = typer.Option("auto", "--shell", help="Shell to use: auto, powershell, bash."),
    no_popup: bool = typer.Option(False, "--no-popup", help="Disable separate terminal popup explanation."),
    no_ai: bool = typer.Option(False, "--no-ai", help="Disable AI-powered error explanations."),
) -> None:
    """Run a command and classify errors from output."""
    framework = detect_framework(project_path)
    console.print(Panel.fit(f"Framework detected: [bold cyan]{framework}[/bold cyan]", title="ErrorMate"))

    runner = CommandRunner(console=console)
    shown_live_error_keys: set[tuple[str, str, str, bool]] = set()
    popup_warning_shown = False
    live_popup_shown = False
    accumulated_reports: list[ErrorReport] = []

    def report_key(report: ErrorReport) -> tuple[str, str, str, bool]:
        return (report.error_type, report.main_error, report.excerpt.lower(), report.is_warning)

    def _fetch_ai_explanations(reports: list[ErrorReport]) -> list[str | None]:
        if no_ai:
            return [None] * len(reports)
        ai_results: list[str | None] = []
        for report in reports:
            console.print("[dim]Asking AI for a better explanation...[/dim]")
            ai_results.append(get_ai_explanation(report))
        return ai_results

    def display_reports(reports: list[ErrorReport], *, final_pass: bool) -> bool:
        nonlocal popup_warning_shown

        if not reports:
            return False

        ai_explanations = _fetch_ai_explanations(reports)

        if no_popup:
            for report, ai_text in zip(reports, ai_explanations):
                console.print(build_error_panel(report, ai_explanation=ai_text))
            return False

        opened = show_errors_in_new_terminal(reports, ai_explanations=ai_explanations)
        if opened:
            message = (
                "Opened final error explanation in a separate terminal window."
                if final_pass
                else "Opened live error explanation in a separate terminal window."
            )
            console.print(f"[cyan]{message}[/cyan]")
            return True

        if not popup_warning_shown:
            console.print("[yellow]Could not open a separate terminal window. Showing explanation in current terminal instead.[/yellow]")
            popup_warning_shown = True

        for report, ai_text in zip(reports, ai_explanations):
            console.print(build_error_panel(report, ai_explanation=ai_text))
        return False

    def on_new_errors(new_reports: list[ErrorReport]) -> None:
        nonlocal accumulated_reports, live_popup_shown

        fresh_reports: list[ErrorReport] = []
        for report in new_reports:
            key = report_key(report)
            if key in shown_live_error_keys:
                continue
            shown_live_error_keys.add(key)
            fresh_reports.append(report)
            accumulated_reports.append(report)

        if not fresh_reports:
            return

        error_count = sum(1 for r in fresh_reports if not r.is_warning)
        warning_count = sum(1 for r in fresh_reports if r.is_warning)
        message_parts = []
        if error_count > 0:
            message_parts.append(f"{error_count} error(s)")
        if warning_count > 0:
            message_parts.append(f"{warning_count} warning(s)")
        
        # Open popup immediately for live errors
        if not no_popup and not live_popup_shown:
            display_reports(fresh_reports, final_pass=False)
            live_popup_shown = True
        else:
            console.print(Panel.fit(f"Detected {' and '.join(message_parts)} while command is running. All will be shown at the end.", title="ErrorMate"))

    result = runner.run(
        command=command,
        framework=framework,
        cwd=project_path,
        shell=shell,
        on_new_errors=on_new_errors,
    )

    # Add any final errors that weren't caught during live detection
    for report in result.detected_errors:
        key = report_key(report)
        if key not in shown_live_error_keys:
            shown_live_error_keys.add(key)
            accumulated_reports.append(report)

    if accumulated_reports:
        error_count = sum(1 for r in accumulated_reports if not r.is_warning)
        warning_count = sum(1 for r in accumulated_reports if r.is_warning)
        message_parts = []
        if error_count > 0:
            message_parts.append(f"{error_count} error(s)")
        if warning_count > 0:
            message_parts.append(f"{warning_count} warning(s)")
        console.print(
            Panel.fit(
                f"Total detected: {' and '.join(message_parts)}",
                title="ErrorMate",
            )
        )

        display_reports(accumulated_reports, final_pass=True)
    else:
        if result.exit_code == 0:
            console.print("[bold green]No known error pattern detected.[/bold green]")
        else:
            console.print(
                "[bold yellow]Command exited with an error code, but no known pattern matched."
                "[/bold yellow]"
            )

    raise typer.Exit(code=result.exit_code)


@app.command("detect")
def detect_only(
    project_path: Path = typer.Option(Path.cwd(), "--project-path", "-p", help="Project directory."),
) -> None:
    """Detect framework for a project path and print it."""
    framework = detect_framework(project_path)
    console.print(Panel.fit(f"Framework detected: [bold cyan]{framework}[/bold cyan]", title="ErrorMate"))


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit.", callback=version_callback, is_eager=True),
    command: str = typer.Argument(None, help="Command to run (optional - same as 'run' subcommand)"),
    project_path: Path = typer.Option(Path.cwd(), "--project-path", "-p", help="Project directory."),
    shell: str = typer.Option("auto", "--shell", help="Shell to use: auto, powershell, bash."),
    no_popup: bool = typer.Option(False, "--no-popup", help="Disable separate terminal popup explanation."),
    no_ai: bool = typer.Option(False, "--no-ai", help="Disable AI-powered error explanations."),
) -> None:
    if ctx.invoked_subcommand is not None:
        return
    
    if command is None:
        console.print("[bold]ErrorMate[/bold] - Run dev commands and detect errors with rule-based matching.")
        console.print("\nUsage: errormate [OPTIONS] COMMAND\n")
        console.print("Options:")
        console.print("  --version, -v     Show version and exit.")
        console.print("  --help            Show this message and exit.")
        console.print("  --project-path, -p Project directory.")
        console.print("  --shell           Shell to use: auto, powershell, bash.")
        console.print("  --no-popup        Disable separate terminal popup explanation.")
        console.print("  --no-ai           Disable AI-powered error explanations.")
        console.print("\nCommands:")
        console.print("  run               Run a command and classify errors from output.")
        console.print("  detect            Detect framework for a project path.")
        console.print("\nExamples:")
        console.print('  errormate run "npm run dev"')
        console.print('  errormate run "dotnet run"')
        console.print('  errormate "npm run dev"  # (same as above)')
        console.print('  errormate detect')
        raise typer.Exit()
    
    # If command is provided directly, invoke the run command
    run_command(command, project_path, shell, no_popup, no_ai)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
