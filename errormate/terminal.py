import os
from pathlib import Path
import shutil
import subprocess

from errormate.error_classifier import ErrorReport
from errormate.error_explainer import render_error_text


def show_error_in_new_terminal(report: ErrorReport) -> bool:
    """Open explanation in a separate terminal window when possible."""
    text = render_error_text(report)

    if os.name == "nt":
        return _open_windows_terminal(text)

    if os.name == "posix":
        return _open_posix_terminal(text)

    return False


def _open_windows_terminal(text: str) -> bool:
    script = (
        "$content = @'\n"
        + text
        + "\n'@; "
        + "Write-Host $content -ForegroundColor Red; "
        + "Read-Host 'Press Enter to close'"
    )

    try:
        subprocess.Popen(
            ["powershell", "-NoExit", "-Command", script],
            creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0),
        )
        return True
    except Exception:
        return False


def _open_posix_terminal(text: str) -> bool:
    escaped = text.replace("\\", "\\\\").replace('"', '\\"').replace("$", "\\$")
    script = f'printf "%s\\n" "{escaped}"; echo; read -r -p "Press Enter to close"'

    terminal_candidates: list[tuple[str, list[str]]] = [
        ("gnome-terminal", ["gnome-terminal", "--", "bash", "-lc", script]),
        ("x-terminal-emulator", ["x-terminal-emulator", "-e", "bash", "-lc", script]),
        ("konsole", ["konsole", "-e", "bash", "-lc", script]),
        ("xterm", ["xterm", "-hold", "-e", "bash", "-lc", script]),
    ]

    for binary, command in terminal_candidates:
        if shutil.which(binary) is None:
            continue
        try:
            subprocess.Popen(command, cwd=str(Path.cwd()))
            return True
        except Exception:
            continue

    return False
