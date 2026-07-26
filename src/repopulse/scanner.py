"""Repository scanner orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import List

from repopulse.checks import run_checks
from repopulse.config import RepoPulseConfig, load_config
from repopulse.models import HealthReport, RepositoryProfile
from repopulse.scoring import calculate_score, grade_for_score
from repopulse.utils import count_directories, iter_repository_files, list_root_files


class ScanError(Exception):
    """Raised when a repository cannot be scanned."""


def detect_project_type(root: Path) -> str:
    """Detect a repository type from common files."""

    if (root / "pyproject.toml").is_file() or (root / "requirements.txt").is_file():
        return "Python"
    if (root / "package.json").is_file():
        return "Node"
    if (root / "Cargo.toml").is_file():
        return "Rust"
    if (root / "go.mod").is_file():
        return "Go"
    if (root / "pom.xml").is_file() or (root / "build.gradle").is_file():
        return "Java"
    return "General"


def build_profile(root: Path, config: RepoPulseConfig) -> RepositoryProfile:
    """Build basic repository metadata."""

    files = list(iter_repository_files(root, config.ignore))
    return RepositoryProfile(
        path=root,
        name=root.name,
        project_type=detect_project_type(root),
        files_count=len(files),
        directories_count=count_directories(root, config.ignore),
        detected_files=list_root_files(root),
    )


def scan_repository(path: Path | str) -> HealthReport:
    """Scan a local repository and return a health report."""

    root = Path(path).expanduser().resolve()
    if not root.exists():
        raise ScanError(f"Path does not exist: {root}")
    if not root.is_dir():
        raise ScanError(f"Path is not a directory: {root}")

    try:
        config = load_config(root)
    except ValueError as exc:
        raise ScanError(str(exc)) from exc

    profile = build_profile(root, config)
    results = run_checks(root, profile, config)
    score = calculate_score(results)
    grade = grade_for_score(score)

    return HealthReport(profile=profile, results=results, score=score, grade=grade)


def scan_many(paths: List[Path | str]) -> List[HealthReport]:
    """Scan multiple repositories."""

    return [scan_repository(path) for path in paths]
