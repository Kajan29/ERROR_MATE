from __future__ import annotations

from errormate.patterns import ErrorPattern
from errormate.patterns.common_patterns import COMMON_PATTERNS
from errormate.patterns.python_patterns import FASTAPI_PATTERNS, PYTHON_PATTERNS


def get_patterns() -> list[ErrorPattern]:
    return [*FASTAPI_PATTERNS, *PYTHON_PATTERNS, *COMMON_PATTERNS]
