from errormate.patterns import ErrorPattern
from errormate.patterns.common_patterns import COMMON_PATTERNS
from errormate.patterns.python_patterns import DJANGO_PATTERNS, PYTHON_PATTERNS


def get_patterns() -> list[ErrorPattern]:
    return [*DJANGO_PATTERNS, *PYTHON_PATTERNS, *COMMON_PATTERNS]
