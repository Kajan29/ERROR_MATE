from rich.panel import Panel
from rich.text import Text

from errormate.error_classifier import ErrorReport


def render_error_text(report: ErrorReport) -> str:
    fixes = "\n".join(f"{idx}. {fix}" for idx, fix in enumerate(report.possible_fixes, start=1))
    return (
        "Error Detected\n\n"
        f"Framework: {report.framework}\n"
        f"Error Type: {report.error_type}\n"
        f"Main Error: {report.main_error}\n"
        f"Matched Output: {report.excerpt}\n\n"
        "Meaning:\n"
        f"{report.meaning}\n\n"
        "Possible Fix:\n"
        f"{fixes}"
    )


def build_error_panel(report: ErrorReport) -> Panel:
    text = Text(render_error_text(report), style="bold red")
    return Panel(text, title="ErrorMate", border_style="red")
