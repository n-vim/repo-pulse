from pathlib import Path

from repopulse.scanner import detect_project_type, scan_repository


def test_detect_python_project(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    assert detect_project_type(tmp_path) == "Python"


def test_scan_repository_returns_report(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "# Demo\n\n## Overview\n\nUseful demo project.\n\n## Usage\n\nRun it.\n" * 20,
        encoding="utf-8",
    )
    (tmp_path / "LICENSE").write_text("MIT", encoding="utf-8")
    (tmp_path / ".gitignore").write_text("__pycache__/\n.venv/\ndist/\nbuild/\n.env\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (tmp_path / "src" / "demo").mkdir(parents=True)
    (tmp_path / "src" / "demo" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_demo.py").write_text("def test_demo():\n    assert True\n", encoding="utf-8")

    report = scan_repository(tmp_path)

    assert report.profile.name == tmp_path.name
    assert report.profile.project_type == "Python"
    assert report.score > 60
    assert report.passed_count >= 5


def test_secret_like_file_fails_security_check(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / ".env").write_text("TOKEN=secret", encoding="utf-8")

    report = scan_repository(tmp_path)
    secrets = [result for result in report.results if result.code == "secrets"][0]

    assert secrets.status.value == "fail"
    assert ".env" in secrets.details["files"]
