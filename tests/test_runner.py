import os
import sys

from errormate.runner import CommandRunner, build_shell_invocation


def test_build_shell_invocation_auto():
    invocation = build_shell_invocation("echo hello", "auto")
    if os.name == "nt":
        assert invocation[0].lower().startswith("powershell")
    else:
        assert invocation[0] == "bash"


def test_build_shell_invocation_invalid_raises():
    try:
        build_shell_invocation("echo hello", "fish")
        assert False, "Expected ValueError"
    except ValueError:
        assert True


def test_runner_captures_stdout(tmp_path):
    if os.name == "nt":
        command = f'& "{sys.executable}" -c "print(\'hello\')"'
    else:
        command = f'"{sys.executable}" -c "print(\'hello\')"'

    result = CommandRunner().run(command=command, framework="Unknown", cwd=tmp_path, shell="auto")

    assert result.exit_code == 0
    assert "hello" in result.stdout
