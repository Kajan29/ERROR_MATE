from __future__ import annotations

from errormate.patterns import ErrorPattern
from errormate.patterns.common_patterns import COMMON_PATTERNS
from errormate.patterns.java_patterns import JAVA_PATTERNS


def get_patterns() -> list[ErrorPattern]:
    return [*JAVA_PATTERNS, *COMMON_PATTERNS]
