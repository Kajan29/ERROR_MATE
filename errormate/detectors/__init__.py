from errormate.patterns import ErrorPattern

from errormate.detectors import django, dotnet, express, laravel, nestjs, nextjs, node, react, spring


def get_patterns_for_framework(framework: str) -> list[ErrorPattern]:
    key = framework.strip().lower()

    mapping = {
        "node.js": node.get_patterns,
        "react": react.get_patterns,
        "express.js": express.get_patterns,
        "next.js": nextjs.get_patterns,
        "nestjs": nestjs.get_patterns,
        "django": django.get_patterns,
        ".net": dotnet.get_patterns,
        "java spring boot": spring.get_patterns,
        "php laravel": laravel.get_patterns,
    }

    getter = mapping.get(key)
    if getter is None:
        return []
    return getter()
