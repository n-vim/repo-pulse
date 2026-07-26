"""Utility helpers for repository scanning."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Iterator, List, Sequence

SECRET_FILE_PATTERNS = (
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "*.pem",
    "*.key",
    "credentials.json",
    "service-account.json",
)

README_NAMES = ("README.md", "README.rst", "README.txt")
LICENSE_NAMES = ("LICENSE", "LICENSE.md", "LICENCE", "LICENCE.md")
CHANGELOG_NAMES = ("CHANGELOG.md", "HISTORY.md", "RELEASES.md")
CONTRIBUTING_NAMES = ("CONTRIBUTING.md", "CONTRIBUTING.rst")
SECURITY_NAMES = ("SECURITY.md", "SECURITY.rst")


def normalize_name(name: str) -> str:
    """Convert a project name into a safe Python-style slug."""

    lowered = name.strip().lower()
    cleaned = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return cleaned or "project"


def package_name(name: str) -> str:
    """Convert a project name into an import-friendly package name."""

    return normalize_name(name).replace("-", "_")


def has_any_file(root: Path, names: Sequence[str]) -> Path | None:
    """Return the first matching file at repository root."""

    for name in names:
        candidate = root / name
        if candidate.is_file():
            return candidate
    return None


def has_any_path(root: Path, names: Sequence[str]) -> Path | None:
    """Return the first matching file or directory at repository root."""

    for name in names:
        candidate = root / name
        if candidate.exists():
            return candidate
    return None


def should_ignore(path: Path, ignore_names: Iterable[str]) -> bool:
    """Return True when a path should be ignored by scanner traversal."""

    parts = set(path.parts)
    return any(pattern in parts or path.name == pattern for pattern in ignore_names)


def iter_repository_files(root: Path, ignore_names: Iterable[str]) -> Iterator[Path]:
    """Yield files under a repository while skipping common generated folders."""

    ignored = set(ignore_names)
    for path in root.rglob("*"):
        if should_ignore(path.relative_to(root), ignored):
            continue
        if path.is_file():
            yield path


def list_root_files(root: Path) -> List[str]:
    """Return sorted root-level file names."""

    return sorted(path.name for path in root.iterdir() if path.is_file())


def count_directories(root: Path, ignore_names: Iterable[str]) -> int:
    """Count non-ignored directories in a repository."""

    count = 0
    ignored = set(ignore_names)
    for path in root.rglob("*"):
        if path.is_dir() and not should_ignore(path.relative_to(root), ignored):
            count += 1
    return count


def read_text_safely(path: Path, max_chars: int = 250_000) -> str:
    """Read a text file safely and avoid loading huge files into memory."""

    try:
        return path.read_text(encoding="utf-8")[:max_chars]
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="ignore")[:max_chars]
    except OSError:
        return ""


def is_secret_like(path: Path) -> bool:
    """Detect common secret-like file names."""

    name = path.name.lower()
    if name == ".env.example":
        return False

    exact = {
        ".env",
        ".env.local",
        ".env.production",
        ".env.development",
        "id_rsa",
        "id_dsa",
        "id_ecdsa",
        "id_ed25519",
        "credentials.json",
        "service-account.json",
    }
    suffixes = (".pem", ".key", ".p12", ".pfx")
    return name in exact or name.endswith(suffixes)


def find_secret_like_files(root: Path, ignore_names: Iterable[str]) -> List[str]:
    """Find suspicious secret-like files in a repository."""

    matches: List[str] = []
    for file_path in iter_repository_files(root, ignore_names):
        if is_secret_like(file_path):
            matches.append(str(file_path.relative_to(root)))
    return sorted(matches)
