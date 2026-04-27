from errormate.patterns import ErrorPattern
from errormate.patterns.common_patterns import COMMON_PATTERNS
from errormate.patterns.node_patterns import NODE_PATTERNS


def get_patterns() -> list[ErrorPattern]:
    return [*NODE_PATTERNS, *COMMON_PATTERNS]
