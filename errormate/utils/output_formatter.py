from rich.text import Text


def style_stream_line(source: str, line: str) -> Text:
    cleaned = line.rstrip("\n")
    if source == "stderr":
        return Text(cleaned, style="red")
    return Text(cleaned, style="white")
