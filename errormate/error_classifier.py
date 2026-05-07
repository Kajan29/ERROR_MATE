from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
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
    root_cause: str = ""
    source_file: Optional[str] = None
    source_line: Optional[int] = None
    source_folder: Optional[str] = None
    source_kind: str = "unknown"
    related_files: list[str] = field(default_factory=list)
    related_folders: list[str] = field(default_factory=list)
    is_warning: bool = False


class ErrorClassifier:
    """Regex-based error classifier with framework-aware pattern selection."""

    def classify(self, output: str, framework: str, project_path: Optional[Path] = None) -> Optional[ErrorReport]:
        reports = self.classify_all(output, framework, project_path=project_path)
        if not reports:
            return None
        return reports[0]

    def classify_all(self, output: str, framework: str, project_path: Optional[Path] = None) -> list[ErrorReport]:
        if not output.strip():
            return []

        framework_patterns = get_patterns_for_framework(framework)
        patterns = self._dedupe_patterns([*framework_patterns, *COMMON_PATTERNS])

        seen_reports: set[tuple[str, str]] = set()
        reports: list[ErrorReport] = []

        for pattern in patterns:
            for match in re.finditer(pattern.regex, output, flags=pattern.flags):
                excerpt = self._build_excerpt(output, match.start(), match.end())
                main_error = self._extract_main_error(
                    output,
                    excerpt,
                    fallback_summary=pattern.summary,
                )
                dedupe_key = (pattern.error_type, main_error.lower())
                if dedupe_key in seen_reports:
                    continue

                seen_reports.add(dedupe_key)
                (
                    source_file,
                    source_line,
                    source_folder,
                    source_kind,
                    related_files,
                    related_folders,
                ) = self._extract_source_location(
                    output,
                    excerpt,
                    framework=framework,
                    error_type=pattern.error_type,
                    project_path=project_path,
                )
                root_cause = self._extract_root_cause(
                    output,
                    excerpt,
                    framework=framework,
                    error_type=pattern.error_type,
                    project_path=project_path,
                )
                reports.append(
                    ErrorReport(
                        framework=framework,
                        error_type=pattern.error_type,
                        main_error=main_error,
                        meaning=pattern.meaning,
                        possible_fixes=pattern.fixes,
                        matched_pattern=pattern.regex,
                        excerpt=excerpt,
                        root_cause=root_cause,
                        source_file=source_file,
                        source_line=source_line,
                        source_folder=source_folder,
                        source_kind=source_kind,
                        related_files=related_files,
                        related_folders=related_folders,
                        is_warning=pattern.is_warning,
                    )
                )

        return reports

    @staticmethod
    def runtime_error_report(framework: str, error: Exception, stage: str) -> ErrorReport:
        message = str(error).strip() or error.__class__.__name__
        return ErrorReport(
            framework=framework,
            error_type="ErrorMate Runtime Error",
            main_error=f"ErrorMate failed while {stage}",
            meaning="ErrorMate had an internal runtime problem while processing the command.",
            possible_fixes=[
                "Retry the same command once.",
                "Use --shell powershell or --shell bash explicitly.",
                "Run with --no-popup to isolate terminal popup issues.",
                "If it still fails, report this issue with the command and full output.",
            ],
            matched_pattern="internal-runtime-error",
            excerpt=message,
            root_cause=message,
        )

    @classmethod
    def _extract_root_cause(
        cls,
        output: str,
        excerpt: str,
        framework: str,
        error_type: str,
        project_path: Optional[Path],
    ) -> str:
        if framework == ".NET" and error_type == "Configuration Error":
            return cls._describe_dotnet_provider_conflict(project_path, output, excerpt)

        unhandled_match = re.search(
            r"Unhandled exception\.\s*(?P<exception>[A-Za-z0-9_.`]+):\s*(?P<message>[^\r\n]+)",
            output,
            flags=re.IGNORECASE,
        )
        if unhandled_match:
            exception_type = unhandled_match.group("exception").strip()
            message = unhandled_match.group("message").strip()
            return f"{exception_type}: {message}"

        access_denied_match = re.search(
            r"(Access denied for user\s+'.+?'@'.+?'.*)",
            output,
            flags=re.IGNORECASE,
        )
        if access_denied_match:
            return access_denied_match.group(1).strip()

        specific_error_line = cls._extract_specific_error_line(output)
        if specific_error_line:
            return specific_error_line

        return excerpt

    @classmethod
    def _extract_main_error(
        cls,
        output: str,
        excerpt: str,
        fallback_summary: str,
    ) -> str:
        normalized_excerpt = cls._normalize_error_text(excerpt)
        if normalized_excerpt and not cls._is_generic_error_text(normalized_excerpt):
            return normalized_excerpt

        specific_error_line = cls._extract_specific_error_line(output)
        if specific_error_line:
            return specific_error_line

        if normalized_excerpt:
            return normalized_excerpt

        return fallback_summary

    @classmethod
    def _describe_dotnet_provider_conflict(
        cls,
        project_path: Optional[Path],
        output: str,
        excerpt: str,
    ) -> str:
        fallback = (
            "Startup validation rejected the database provider flags because they are not in a valid one-provider-only state. "
            "This usually means both MYSQL and POSTGRES are true, or both are false."
        )
        if project_path is None:
            return fallback

        candidates = cls._rank_dotnet_configuration_candidates(project_path, output, excerpt)
        for candidate in candidates:
            mysql_value = candidate["mysql_value"]
            postgres_value = candidate["postgres_value"]
            if mysql_value is None or postgres_value is None or mysql_value != postgres_value:
                continue

            mysql_text = "true" if mysql_value else "false"
            postgres_text = "true" if postgres_value else "false"
            state = "enabled" if mysql_value else "disabled"
            return (
                f"{candidate['path']} sets MYSQL={mysql_text} and POSTGRES={postgres_text}, so both providers are {state}. "
                "Exactly one provider must be enabled before the app can start."
            )

        return fallback

    @classmethod
    def _extract_specific_error_line(cls, output: str) -> Optional[str]:
        lines = [line.strip() for line in output.splitlines() if line.strip()]
        if not lines:
            return None

        reverse_priority_patterns = [
            r"^Unhandled exception\.\s+(?P<exception>[A-Za-z0-9_.`]+):\s*(?P<message>.+)$",
            r"^Caused by:\s+(?P<exception>[A-Za-z0-9_.$`]+(?:Exception|Error)):\s*(?P<message>.+)$",
            r"^(?P<exception>[A-Za-z0-9_.$`]+(?:Exception|Error)):\s*(?P<message>.+)$",
        ]
        for line in reversed(lines):
            for pattern in reverse_priority_patterns:
                match = re.search(pattern, line, flags=re.IGNORECASE)
                if not match:
                    continue

                exception_name = match.group("exception").strip()
                message = match.group("message").strip()
                return cls._normalize_error_text(cls._format_exception_headline(exception_name, message))

        forward_priority_patterns = [
            r"Module not found:.*",
            r"Can't resolve ['\"].+['\"].*",
            r"error\s+(?:CS|NU)\d{4}:\s+.+",
            r"SQLSTATE\[[0-9A-Z]+\]\s*\[[0-9]+\].+",
            r"Access denied for user\s+'.+?'@'.+?'.*",
            r"Missing required environment variable.+",
            r"environment variable .+ is not set.*",
            r"process\.env\.[A-Z0-9_]+.*undefined.*",
            r"ImproperlyConfigured: Set the .+ environment variable.*",
            r"(?:EADDRINUSE|Address already in use|Only one usage of each socket address).+",
            r"(?:EACCES|EPERM|Permission denied|Access is denied).+",
        ]
        for pattern in forward_priority_patterns:
            for line in lines:
                if re.search(pattern, line, flags=re.IGNORECASE):
                    return cls._normalize_error_text(line)

        return None

    @staticmethod
    def _format_exception_headline(exception_name: str, message: str) -> str:
        simplified_name = exception_name.split(".")[-1].split("$")[-1]
        if simplified_name:
            exception_name = simplified_name
        return f"{exception_name}: {message}"

    @staticmethod
    def _normalize_error_text(text: str, limit: int = 160) -> str:
        normalized = " ".join(text.strip().split())
        if len(normalized) <= limit:
            return normalized
        return normalized[: limit - 3].rstrip() + "..."

    @staticmethod
    def _is_generic_error_text(text: str) -> bool:
        lowered = text.strip().lower()
        if not lowered or lowered == "(no excerpt)":
            return True

        generic_markers = {
            "traceback (most recent call last):",
            "compiled with problems",
            "failed to compile",
            "compilation error",
            'exception in thread "main"',
        }
        return lowered in generic_markers

    @classmethod
    def _extract_source_location(
        cls,
        output: str,
        excerpt: str,
        framework: str,
        error_type: str,
        project_path: Optional[Path],
    ) -> tuple[Optional[str], Optional[int], Optional[str], str, list[str], list[str]]:
        stack_patterns = [
            r"\bin\s+(?P<file>(?:[A-Za-z]:\\|/)[^:\r\n]+?\.[A-Za-z0-9]+):line\s+(?P<line>\d+)",
            r"\bin\s+(?P<file>(?:[A-Za-z]:\\|/)[^:\r\n]+?\.[A-Za-z0-9]+):(?P<line>\d+)",
        ]

        for pattern in stack_patterns:
            match = re.search(pattern, output, flags=re.IGNORECASE)
            if not match:
                continue

            file_path = match.group("file").strip()
            line = int(match.group("line"))
            folder = cls._extract_folder(file_path)
            _, _, related_files, related_folders = cls._find_project_location_hints(
                framework=framework,
                error_type=error_type,
                output=output,
                excerpt=excerpt,
                project_path=project_path,
            )
            return file_path, line, folder, "exact", related_files, related_folders

        compile_style_match = re.search(
            r"(?P<file>[A-Za-z0-9_./\\-]+\.[A-Za-z0-9]+)\((?P<line>\d+),\d+\):\s*error",
            excerpt,
            flags=re.IGNORECASE,
        )
        if compile_style_match:
            file_path = compile_style_match.group("file").strip()
            line = int(compile_style_match.group("line"))
            folder = cls._extract_folder(file_path)
            return file_path, line, folder, "exact", [], []

        likely_file, likely_folder, related_files, related_folders = cls._find_project_location_hints(
            framework=framework,
            error_type=error_type,
            output=output,
            excerpt=excerpt,
            project_path=project_path,
        )
        if likely_file or likely_folder or related_files or related_folders:
            return likely_file, None, likely_folder, "likely", related_files, related_folders

        return None, None, None, "unknown", [], []

    @classmethod
    def _find_project_location_hints(
        cls,
        framework: str,
        error_type: str,
        output: str,
        excerpt: str,
        project_path: Optional[Path],
    ) -> tuple[Optional[str], Optional[str], list[str], list[str]]:
        if project_path is None:
            return None, None, [], []

        if framework == ".NET" and error_type == "Configuration Error":
            return cls._find_dotnet_configuration_files(project_path, output, excerpt)

        return None, None, [], []

    @classmethod
    def _find_dotnet_configuration_files(
        cls,
        project_path: Path,
        output: str,
        excerpt: str,
    ) -> tuple[Optional[str], Optional[str], list[str], list[str]]:
        ranked_candidates = cls._rank_dotnet_configuration_candidates(project_path, output, excerpt)
        if not ranked_candidates:
            return None, None, [], []

        related_files = [str(item["path"]) for item in ranked_candidates[:5]]
        related_folders = list(dict.fromkeys(str(item["folder"]) for item in ranked_candidates if item["folder"]))[:3]

        primary_file = related_files[0] if related_files else None
        primary_folder = related_folders[0] if related_folders else None
        return primary_file, primary_folder, related_files, related_folders

    @classmethod
    def _rank_dotnet_configuration_candidates(
        cls,
        project_path: Path,
        output: str,
        excerpt: str,
    ) -> list[dict[str, object]]:
        if not project_path.exists():
            return []

        skip_dirs = {
            ".git",
            ".idea",
            ".vs",
            ".vscode",
            "bin",
            "build",
            "dist",
            "node_modules",
            "obj",
            "packages",
            "target",
            "venv",
            ".venv",
            "__pycache__",
        }
        search_patterns = (".env", ".env.*", "appsettings*.json", "launchSettings.json")
        output_upper = f"{output}\n{excerpt}".upper()
        token_weights = {
            "MYSQL": 3,
            "POSTGRES": 3,
            "DATABASE": 1,
            "PROVIDER": 1,
        }

        candidate_paths: list[Path] = []
        for pattern in search_patterns:
            for path in project_path.rglob(pattern):
                if any(part in skip_dirs for part in path.parts):
                    continue
                if not path.is_file():
                    continue
                candidate_paths.append(path)

        unique_candidates = list(dict.fromkeys(candidate_paths))
        if not unique_candidates:
            return []

        scored_candidates: list[dict[str, object]] = []
        for path in unique_candidates:
            score = 0
            path_str = str(path.resolve())
            path_upper = path_str.upper()

            if path.name == ".env":
                score += 2
            if path.name.lower() == "launchsettings.json":
                score += 1
            if "PROPERTIES" in path_upper:
                score += 1

            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                content = ""

            content_upper = content.upper()

            for token, weight in token_weights.items():
                if token in content_upper:
                    score += weight
                if token in output_upper and token in content_upper:
                    score += weight

            mysql_value = cls._extract_config_bool(content, "MYSQL")
            postgres_value = cls._extract_config_bool(content, "POSTGRES")
            if mysql_value is not None:
                score += 1
            if postgres_value is not None:
                score += 1
            if mysql_value is not None and postgres_value is not None and mysql_value == postgres_value:
                score += 2

            scored_candidates.append(
                {
                    "score": score,
                    "path": path.resolve(),
                    "folder": path.parent.resolve(),
                    "mysql_value": mysql_value,
                    "postgres_value": postgres_value,
                }
            )

        scored_candidates.sort(
            key=lambda item: (-int(item["score"]), len(str(item["path"])), str(item["path"]).lower())
        )
        return scored_candidates

    @staticmethod
    def _extract_config_bool(content: str, key: str) -> Optional[bool]:
        patterns = [
            rf'(?im)^\s*{re.escape(key)}\s*=\s*"?(?P<value>true|false|1|0)"?\s*$',
            rf'(?im)"{re.escape(key)}"\s*:\s*"?(?P<value>true|false|1|0)"?',
        ]
        for pattern in patterns:
            match = re.search(pattern, content)
            if not match:
                continue

            raw_value = match.group("value").strip().lower()
            if raw_value in {"true", "1"}:
                return True
            if raw_value in {"false", "0"}:
                return False

        return None

    @staticmethod
    def _extract_folder(file_path: str) -> Optional[str]:
        if "\\" in file_path:
            return file_path.rsplit("\\", 1)[0]
        if "/" in file_path:
            return file_path.rsplit("/", 1)[0]
        return None

    @staticmethod
    def _build_excerpt(output: str, start: int, end: int) -> str:
        line_start = output.rfind("\n", 0, start) + 1
        line_end = output.find("\n", end)
        if line_end == -1:
            line_end = len(output)

        text = output[line_start:line_end].strip()
        if not text:
            return "(no excerpt)"
        return text

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
