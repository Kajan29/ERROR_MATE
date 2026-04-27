from pathlib import Path

from errormate.utils.file_utils import read_json_file


def _has_any(path: Path, patterns: list[str]) -> bool:
    for pattern in patterns:
        if any(path.glob(pattern)):
            return True
    return False


def detect_framework(project_path: Path) -> str:
    """Detect framework using marker files and dependency hints."""
    project_path = Path(project_path)

    package_json = project_path / "package.json"
    if package_json.exists():
        package_data = read_json_file(package_json)
        deps = {
            **package_data.get("dependencies", {}),
            **package_data.get("devDependencies", {}),
        }
        dep_keys = set(deps.keys())

        if "@nestjs/core" in dep_keys:
            return "NestJS"
        if "next" in dep_keys:
            return "Next.js"
        if "react" in dep_keys:
            return "React"
        if "express" in dep_keys:
            return "Express.js"
        return "Node.js"

    if (project_path / "manage.py").exists():
        return "Django"

    if _has_any(project_path, ["*.csproj", "*.sln"]):
        return ".NET"

    if _has_any(project_path, ["pom.xml", "build.gradle", "build.gradle.kts"]):
        return "Java Spring Boot"

    if (project_path / "artisan").exists() and (project_path / "composer.json").exists():
        return "PHP Laravel"

    return "Unknown"
