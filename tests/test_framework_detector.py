import json

from errormate.framework_detector import detect_framework


def test_detect_nextjs(tmp_path):
    (tmp_path / "package.json").write_text(
        json.dumps({"dependencies": {"next": "14.2.0", "react": "18.3.0"}}),
        encoding="utf-8",
    )
    assert detect_framework(tmp_path) == "Next.js"


def test_detect_react(tmp_path):
    (tmp_path / "package.json").write_text(
        json.dumps({"dependencies": {"react": "18.3.0"}}),
        encoding="utf-8",
    )
    assert detect_framework(tmp_path) == "React"


def test_detect_django(tmp_path):
    (tmp_path / "manage.py").write_text("print('django')\n", encoding="utf-8")
    assert detect_framework(tmp_path) == "Django"


def test_detect_dotnet(tmp_path):
    (tmp_path / "Sample.csproj").write_text("<Project />\n", encoding="utf-8")
    assert detect_framework(tmp_path) == ".NET"


def test_detect_spring_boot(tmp_path):
    (tmp_path / "pom.xml").write_text("<project></project>\n", encoding="utf-8")
    assert detect_framework(tmp_path) == "Java Spring Boot"


def test_detect_laravel(tmp_path):
    (tmp_path / "artisan").write_text("#!/usr/bin/env php\n", encoding="utf-8")
    (tmp_path / "composer.json").write_text("{}\n", encoding="utf-8")
    assert detect_framework(tmp_path) == "PHP Laravel"


def test_detect_unknown(tmp_path):
    assert detect_framework(tmp_path) == "Unknown"
