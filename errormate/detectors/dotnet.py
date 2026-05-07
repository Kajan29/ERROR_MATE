from __future__ import annotations

from errormate.patterns import ErrorPattern
from errormate.patterns.common_patterns import COMMON_PATTERNS
from errormate.patterns.dotnet_patterns import DOTNET_PATTERNS


def get_patterns() -> list[ErrorPattern]:
    return [*DOTNET_PATTERNS, *COMMON_PATTERNS]
