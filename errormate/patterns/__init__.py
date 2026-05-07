from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ErrorPattern:
    error_type: str
    regex: str
    summary: str
    meaning: str
    fixes: list[str]
    flags: int = re.IGNORECASE | re.MULTILINE
    is_warning: bool = False
