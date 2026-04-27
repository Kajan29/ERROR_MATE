from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from errormate.error_explainer import build_error_panel
from errormate.framework_detector import detect_framework
from errormate.runner import CommandRunner
from errormate.terminal import show_error_in_new_terminal

app = typer.Typer(add_completion=False, help="Run dev commands and detect errors with rule-based matching.")
console = Console()


@app.command("run")
def run_command(
    command: str = typer.Argument(..., help="Command to run, for example: npm run dev"),
    project_path: Path = typer.Option(Path.cwd(), "--project-path", "-p", help="Project directory."),
    shell: str = typer.Option("auto", "--shell", help="Shell to use: auto, powershell, bash."),
    no_popup: bool = typer.Option(False, "--no-popup", help="Disable separate terminal popup explanation."),
) -> None:
    """Run a command and classify errors from output."""
    framework = detect_framework(project_path)
    console.print(Panel.fit(f"Framework detected: [bold cyan]{framework}[/bold cyan]", title="ErrorMate"))

    runner = CommandRunner(console=console)
    result = runner.run(command=command, framework=framework, cwd=project_path, shell=shell)

    if result.detected_error is not None:
        console.print(build_error_panel(result.detected_error))
        if not no_popup:
            opened = show_error_in_new_terminal(result.detected_error)
            if not opened:
                console.print("[yellow]Could not open a separate terminal window. Showing explanation in current terminal only.[/yellow]")
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


def main() -> None:
    app()


if __name__ == "__main__":
    main()
