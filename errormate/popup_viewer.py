from pathlib import Path
import sys

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


def main() -> int:
    if len(sys.argv) < 2:
        return 1

    payload_path = Path(sys.argv[1])
    try:
        content = payload_path.read_text(encoding="utf-8")
    except Exception as error:
        Console().print(Panel.fit(f"ErrorMate could not read the popup payload.\n\n{error}", title="ErrorMate", border_style="red"))
        return 1
    finally:
        try:
            payload_path.unlink(missing_ok=True)
        except Exception:
            pass

    console = Console()
    console.print()
    console.print(Panel(
        Text(content),
        title="[bold white on red] ErrorMate - Error Explanation [/bold white on red]",
        border_style="bright_red",
        padding=(1, 2),
    ))
    console.print()
    console.print("[dim]This window was opened by ErrorMate to show error details.[/dim]")
    console.print()

    try:
        input("Press Enter to close this window...")
    except EOFError:
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
