from __future__ import annotations

from errormate.patterns import ErrorPattern
from errormate.patterns.common_patterns import COMMON_PATTERNS
from errormate.patterns.node_patterns import EXPRESS_PATTERNS, NODE_PATTERNS


def get_patterns() -> list[ErrorPattern]:
    return [*EXPRESS_PATTERNS, *NODE_PATTERNS, *COMMON_PATTERNS]
