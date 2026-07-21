"""Configuration loading for RepoPulse."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping

import yaml

DEFAULT_IGNORE = [
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    ".idea",
    ".vscode",
]

CONFIG_FILENAMES = (".repopulse.yaml", ".repopulse.yml", "repopulse.yaml", "repopulse.yml")


@dataclass(frozen=True)
class RepoPulseConfig:
    """Runtime configuration for a repository scan."""

    min_readme_chars: int = 400
    fail_under: int = 70
    ignore: List[str] = field(default_factory=lambda: list(DEFAULT_IGNORE))

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "RepoPulseConfig":
        ignore = data.get("ignore", DEFAULT_IGNORE)
        if not isinstance(ignore, list):
            ignore = list(DEFAULT_IGNORE)

        return cls(
            min_readme_chars=_safe_int(data.get("min_readme_chars"), 400),
            fail_under=_safe_int(data.get("fail_under"), 70),
            ignore=[str(item) for item in ignore],
        )

    def merged_with(self, data: Mapping[str, Any]) -> "RepoPulseConfig":
        merged: Dict[str, Any] = {
            "min_readme_chars": self.min_readme_chars,
            "fail_under": self.fail_under,
            "ignore": list(self.ignore),
        }
        merged.update(data)
        return RepoPulseConfig.from_mapping(merged)


def _safe_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def find_config_file(path: Path) -> Path | None:
    """Return the first RepoPulse config file found in a repository root."""

    for filename in CONFIG_FILENAMES:
        candidate = path / filename
        if candidate.is_file():
            return candidate
    return None


def load_config(path: Path) -> RepoPulseConfig:
    """Load RepoPulse configuration from a repository path."""

    config = RepoPulseConfig()
    config_file = find_config_file(path)
    if not config_file:
        return config

    try:
        loaded = yaml.safe_load(config_file.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid config file: {config_file}: {exc}") from exc

    if not isinstance(loaded, dict):
        raise ValueError(f"Config file must contain a YAML object: {config_file}")

    return config.merged_with(loaded)


def write_default_config(path: Path, overwrite: bool = False) -> Path:
    """Write a default .repopulse.yaml file."""

    target = path / ".repopulse.yaml"
    if target.exists() and not overwrite:
        raise FileExistsError(target)

    content = """min_readme_chars: 400\nfail_under: 70\nignore:\n  - .git\n  - .venv\n  - node_modules\n  - dist\n  - build\n"""
    target.write_text(content, encoding="utf-8")
    return target


def extend_ignore(base: Iterable[str], extra: Iterable[str]) -> List[str]:
    """Merge ignore patterns while preserving order."""

    merged: List[str] = []
    for item in [*base, *extra]:
        if item not in merged:
            merged.append(item)
    return merged
