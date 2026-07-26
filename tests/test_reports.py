from pathlib import Path

from repopulse.reports import to_json, to_markdown
from repopulse.scanner import scan_repository


def test_markdown_report_contains_score(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    report = scan_repository(tmp_path)
    markdown = to_markdown(report)

    assert "# RepoPulse Report" in markdown
    assert "**Score:**" in markdown
    assert "## Checks" in markdown


def test_json_report_contains_repository_metadata(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    report = scan_repository(tmp_path)
    payload = to_json(report)

    assert '"repository"' in payload
    assert '"checks"' in payload
    assert tmp_path.name in payload
