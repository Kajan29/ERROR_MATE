from __future__ import annotations

from errormate.patterns import ErrorPattern
from errormate.patterns.common_patterns import COMMON_PATTERNS
from errormate.patterns.php_patterns import LARAVEL_PATTERNS, PHP_PATTERNS


def get_patterns() -> list[ErrorPattern]:
    return [*LARAVEL_PATTERNS, *PHP_PATTERNS, *COMMON_PATTERNS]
