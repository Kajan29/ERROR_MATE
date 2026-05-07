from __future__ import annotations

import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Optional, Sequence
import uuid

from errormate.error_classifier import ErrorReport
from errormate.error_explainer import render_errors_text


_ACTIVE_PAYLOAD_PATH: Path | None = None
_ACTIVE_HEARTBEAT_PATH: Path | None = None
_SESSION_HEARTBEAT_TTL_SECONDS = 3.0


def show_error_in_new_terminal(report: ErrorReport) -> bool:
    return show_errors_in_new_terminal([report])


def show_errors_in_new_terminal(
    reports: Sequence[ErrorReport],
    ai_explanations: Optional[list[Optional[str]]] = None,
) -> bool:
    """Open explanation in a separate terminal window when possible."""
    text = render_errors_text(list(reports), ai_explanations=ai_explanations)

    if _is_active_popup_session() and _ACTIVE_PAYLOAD_PATH is not None:
        try:
            _ACTIVE_PAYLOAD_PATH.write_text(text, encoding="utf-8")
            return True
        except Exception:
            _reset_active_popup_session()

    payload_path = _write_popup_payload(text)
    if payload_path is None:
        return False

    if os.name == "nt":
        opened = _open_windows_terminal(payload_path)
        if not opened:
            _cleanup_payload(payload_path)
            _cleanup_payload(_heartbeat_path(payload_path))
        else:
            _set_active_popup_session(payload_path)
        return opened

    if os.name == "posix":
        opened = _open_posix_terminal(payload_path)
        if not opened:
            _cleanup_payload(payload_path)
            _cleanup_payload(_heartbeat_path(payload_path))
        else:
            _set_active_popup_session(payload_path)
        return opened

    _cleanup_payload(payload_path)
    _cleanup_payload(_heartbeat_path(payload_path))
    return False


def _write_popup_payload(text: str) -> Path | None:
    try:
        payload_path = Path(tempfile.gettempdir()) / f"errormate-popup-{uuid.uuid4().hex}.txt"
        payload_path.write_text(text, encoding="utf-8")
        return payload_path
    except Exception:
        return None


def _cleanup_payload(payload_path: Path) -> None:
    try:
        payload_path.unlink(missing_ok=True)
    except Exception:
        pass


def _heartbeat_path(payload_path: Path) -> Path:
    return payload_path.with_suffix(payload_path.suffix + ".alive")


def _set_active_popup_session(payload_path: Path) -> None:
    global _ACTIVE_PAYLOAD_PATH, _ACTIVE_HEARTBEAT_PATH
    _ACTIVE_PAYLOAD_PATH = payload_path
    _ACTIVE_HEARTBEAT_PATH = _heartbeat_path(payload_path)


def _reset_active_popup_session() -> None:
    global _ACTIVE_PAYLOAD_PATH, _ACTIVE_HEARTBEAT_PATH
    _ACTIVE_PAYLOAD_PATH = None
    _ACTIVE_HEARTBEAT_PATH = None


def _is_active_popup_session() -> bool:
    if _ACTIVE_PAYLOAD_PATH is None or _ACTIVE_HEARTBEAT_PATH is None:
        return False

    if not _ACTIVE_HEARTBEAT_PATH.exists():
        _reset_active_popup_session()
        return False

    try:
        age_seconds = time.time() - _ACTIVE_HEARTBEAT_PATH.stat().st_mtime
    except Exception:
        _reset_active_popup_session()
        return False

    if age_seconds > _SESSION_HEARTBEAT_TTL_SECONDS:
        _reset_active_popup_session()
        return False

    return True


def _popup_viewer_invocation(payload_path: Path) -> list[str]:
    viewer_script = Path(__file__).with_name("popup_viewer.py")
    return [sys.executable, str(viewer_script), str(payload_path)]


def _open_windows_terminal(payload_path: Path) -> bool:
    command = _popup_viewer_invocation(payload_path)

    try:
        subprocess.Popen(
            command,
            creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0),
        )
        return True
    except Exception:
        pass

    powershell_exe = shutil.which("powershell") or shutil.which("pwsh")
    if powershell_exe is None:
        return False

    working_directory = str(Path.cwd())
    file_path = command[0]
    argument_list = ", ".join(_quote_powershell_argument(argument) for argument in command[1:])
    start_process_command = (
        f"Start-Process -FilePath { _quote_powershell_argument(file_path) } "
        f"-ArgumentList @({argument_list}) -WorkingDirectory { _quote_powershell_argument(working_directory) }"
    )

    try:
        subprocess.Popen([powershell_exe, "-NoProfile", "-Command", start_process_command])
        return True
    except Exception:
        return False


def _quote_powershell_argument(value: str) -> str:
    escaped = value.replace("'", "''")
    return f"'{escaped}'"


def _open_posix_terminal(payload_path: Path) -> bool:
    script = " ".join(shlex.quote(part) for part in _popup_viewer_invocation(payload_path))

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
