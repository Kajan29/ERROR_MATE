import json
from pathlib import Path
from typing import Any


def read_json_file(path: Path) -> dict[str, Any]:
    try:
        content = path.read_text(encoding="utf-8")
        data = json.loads(content)
        if isinstance(data, dict):
            return data
        return {}
    except Exception:
        return {}
