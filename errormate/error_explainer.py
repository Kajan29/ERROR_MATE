from __future__ import annotations

from typing import Optional

from rich.panel import Panel
from rich.text import Text

from errormate.error_classifier import ErrorReport

_SEPARATOR = "-" * 50


def render_error_text(report: ErrorReport, ai_explanation: Optional[str] = None) -> str:
    return render_errors_text([report], ai_explanations=[ai_explanation] if ai_explanation else None)


def render_errors_text(
    reports: list[ErrorReport],
    ai_explanations: Optional[list[Optional[str]]] = None,
) -> str:
    if not reports:
        return "No error details available."

    blocks: list[str] = []
    total = len(reports)
    error_count = sum(1 for r in reports if not r.is_warning)
    warning_count = sum(1 for r in reports if r.is_warning)

    for idx, report in enumerate(reports, start=1):
        if report.is_warning:
            heading = "WARNING DETECTED" if total == 1 else f"WARNING {idx} of {total}"
        else:
            heading = "ERROR DETECTED" if total == 1 else f"ERROR {idx} of {total}"
        main_error = report.main_error.strip() if report.main_error else report.excerpt

        lines: list[str] = []
        lines.append(heading)
        lines.append(_SEPARATOR)
        lines.append("")
        lines.append(f"  Error:     {main_error}")
        lines.append(f"  Framework: {report.framework}")
        lines.append(f"  Type:      {report.error_type}")
        lines.append("")

        # AI explanation (if available)
        ai_text = ai_explanations[idx - 1] if ai_explanations and idx - 1 < len(ai_explanations) else None
        if ai_text:
            lines.append(_SEPARATOR)
            lines.append("  AI EXPLANATION")
            lines.append(_SEPARATOR)
            lines.append("")
            for ai_line in ai_text.splitlines():
                lines.append(f"  {ai_line}")
            lines.append("")

        # Simple meaning
        lines.append(_SEPARATOR)
        lines.append("  WHAT THIS MEANS")
        lines.append(_SEPARATOR)
        lines.append("")
        lines.append(f"  {report.meaning}")
        lines.append("")

        # Root cause
        root_cause = _resolve_root_cause(report)
        lines.append(f"  Why it happened: {root_cause}")
        lines.append("")

        # Where it happened
        location_text = _build_location_text(report)
        if location_text:
            lines.append(_SEPARATOR)
            lines.append("  WHERE IT HAPPENED")
            lines.append(_SEPARATOR)
            lines.append("")
            for loc_line in location_text.splitlines():
                lines.append(f"  {loc_line}")
            lines.append("")

        # Terminal output snippet
        if report.excerpt.strip():
            lines.append(_SEPARATOR)
            lines.append("  TERMINAL OUTPUT")
            lines.append(_SEPARATOR)
            lines.append("")
            for exc_line in report.excerpt.strip().splitlines():
                lines.append(f"    {exc_line}")
            lines.append("")

        # How to fix
        lines.append(_SEPARATOR)
        lines.append("  HOW TO FIX")
        lines.append(_SEPARATOR)
        lines.append("")
        if report.possible_fixes:
            for fix_idx, fix in enumerate(report.possible_fixes, start=1):
                lines.append(f"  {fix_idx}. {fix}")
        else:
            lines.append("  No suggested fixes were identified.")
        lines.append("")
        lines.append(_SEPARATOR)

        blocks.append("\n".join(lines))

    # Add summary at the top
    summary_lines: list[str] = []
    summary_lines.append("=" * 50)
    summary_lines.append("ERRORMATE REPORT")
    summary_lines.append("=" * 50)
    summary_lines.append("")
    if error_count > 0:
        summary_lines.append(f"Errors found:   {error_count}")
    if warning_count > 0:
        summary_lines.append(f"Warnings found: {warning_count}")
    summary_lines.append("")
    summary_lines.append("=" * 50)
    summary_lines.append("")

    return "\n".join(summary_lines) + "\n\n".join(blocks)


def _resolve_root_cause(report: ErrorReport) -> str:
    root_cause = report.root_cause.strip() if report.root_cause else ""
    if root_cause:
        return root_cause

    main_error = report.main_error.strip() if report.main_error else ""
    if main_error:
        return main_error

    excerpt = report.excerpt.strip() if report.excerpt else ""
    if excerpt:
        return excerpt

    return "Root cause could not be determined from the command output."


def _build_location_text(report: ErrorReport) -> str:
    location_lines: list[str] = []

    if report.source_kind == "exact":
        if report.source_file:
            location_lines.append(f"File: {report.source_file}")
        if report.source_line is not None:
            location_lines.append(f"Line: {report.source_line}")
        if report.source_folder:
            location_lines.append(f"Folder: {report.source_folder}")
        if report.related_files:
            location_lines.append("Also check these files:")
            location_lines.extend(f"  - {file_path}" for file_path in report.related_files)
        if report.related_folders:
            location_lines.append("Also check these folders:")
            location_lines.extend(f"  - {folder_path}" for folder_path in report.related_folders)
        return "\n".join(location_lines)

    if report.source_kind == "likely":
        if report.related_files:
            location_lines.append("Check these files:")
            location_lines.extend(f"  - {file_path}" for file_path in report.related_files)
        elif report.source_file:
            location_lines.append(f"Check this file: {report.source_file}")

        if report.related_folders:
            location_lines.append("Check these folders:")
            location_lines.extend(f"  - {folder_path}" for folder_path in report.related_folders)
        elif report.source_folder:
            location_lines.append(f"Check this folder: {report.source_folder}")

        return "\n".join(location_lines)

    if report.source_file:
        location_lines.append(f"File: {report.source_file}")
    if report.source_line is not None:
        location_lines.append(f"Line: {report.source_line}")
    if report.source_folder:
        location_lines.append(f"Folder: {report.source_folder}")

    return "\n".join(location_lines) if location_lines else ""


def build_error_panel(report: ErrorReport, ai_explanation: Optional[str] = None) -> Panel:
    if report.is_warning:
        text = Text(render_error_text(report, ai_explanation=ai_explanation), style="bold yellow")
        return Panel(text, title="ErrorMate - Warning", border_style="yellow")
    else:
        text = Text(render_error_text(report, ai_explanation=ai_explanation), style="bold red")
        return Panel(text, title="ErrorMate - Error", border_style="red")
