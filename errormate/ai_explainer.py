"""Free AI-powered error explanation using DuckDuckGo AI Chat (no API key needed)."""
from __future__ import annotations

from typing import Optional

from errormate.error_classifier import ErrorReport


def get_ai_explanation(report: ErrorReport) -> Optional[str]:
    """Get a human-friendly AI explanation for the error. Returns None if AI is unavailable."""
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        return None

    prompt = _build_prompt(report)

    try:
        with DDGS() as ddgs:
            result = ddgs.chat(prompt, model="gpt-4o-mini")
        if result and isinstance(result, str) and len(result.strip()) > 20:
            return result.strip()
    except Exception:
        pass

    return None


def _build_prompt(report: ErrorReport) -> str:
    fixes_text = "\n".join(f"- {fix}" for fix in report.possible_fixes) if report.possible_fixes else "None identified"

    return (
        "You are a helpful coding assistant. A developer hit an error. "
        "Explain the error in simple, beginner-friendly language. "
        "Then give clear step-by-step instructions to fix it.\n\n"
        "Rules:\n"
        "- Use plain English, no jargon\n"
        "- Be concise (max 15 lines)\n"
        "- Start with 'What went wrong:' then 'How to fix it:'\n"
        "- Number the fix steps\n"
        "- If a terminal command is needed, show the exact command\n\n"
        f"Framework: {report.framework}\n"
        f"Error Type: {report.error_type}\n"
        f"Error Message: {report.main_error}\n"
        f"Terminal Output:\n{report.excerpt}\n"
        f"Root Cause: {report.root_cause or 'Unknown'}\n"
        f"Current Suggested Fixes:\n{fixes_text}\n"
    )
