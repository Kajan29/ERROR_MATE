from dataclasses import dataclass
import re
from typing import Optional

from errormate.detectors import get_patterns_for_framework
from errormate.patterns.common_patterns import COMMON_PATTERNS
from errormate.patterns import ErrorPattern


@dataclass
class ErrorReport:
    framework: str
    error_type: str
    main_error: str
    meaning: str
    possible_fixes: list[str]
    matched_pattern: str
    excerpt: str


class ErrorClassifier:
    """Regex-based error classifier with framework-aware pattern selection."""

    def classify(self, output: str, framework: str) -> Optional[ErrorReport]:
        if not output.strip():
            return None

        framework_patterns = get_patterns_for_framework(framework)
        patterns = self._dedupe_patterns([*framework_patterns, *COMMON_PATTERNS])

        for pattern in patterns:
            match = re.search(pattern.regex, output, flags=pattern.flags)
            if match:
                excerpt = match.group(0).strip().splitlines()[0]
                return ErrorReport(
                    framework=framework,
                    error_type=pattern.error_type,
                    main_error=pattern.summary,
                    meaning=pattern.meaning,
                    possible_fixes=pattern.fixes,
                    matched_pattern=pattern.regex,
                    excerpt=excerpt,
                )

        return None

    @staticmethod
    def _dedupe_patterns(patterns: list[ErrorPattern]) -> list[ErrorPattern]:
        seen: set[tuple[str, str]] = set()
        deduped: list[ErrorPattern] = []
        for pattern in patterns:
            key = (pattern.error_type, pattern.regex)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(pattern)
        return deduped
