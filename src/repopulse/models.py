"""Data models used by RepoPulse."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class CheckStatus(str, Enum):
    """Supported check result statuses."""

    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


@dataclass(frozen=True)
class CheckDefinition:
    """Metadata for a built-in repository check."""

    code: str
    name: str
    category: str
    max_points: int
    description: str


@dataclass(frozen=True)
class CheckResult:
    """Result returned by an individual repository check."""

    code: str
    name: str
    category: str
    status: CheckStatus
    points: int
    max_points: int
    message: str
    recommendation: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return self.status == CheckStatus.PASS

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "name": self.name,
            "category": self.category,
            "status": self.status.value,
            "points": self.points,
            "max_points": self.max_points,
            "message": self.message,
            "recommendation": self.recommendation,
            "details": self.details,
        }


@dataclass(frozen=True)
class RepositoryProfile:
    """Detected repository metadata."""

    path: Path
    name: str
    project_type: str
    files_count: int
    directories_count: int
    detected_files: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": str(self.path),
            "name": self.name,
            "project_type": self.project_type,
            "files_count": self.files_count,
            "directories_count": self.directories_count,
            "detected_files": self.detected_files,
        }


@dataclass(frozen=True)
class HealthReport:
    """Full repository health report."""

    profile: RepositoryProfile
    results: List[CheckResult]
    score: int
    grade: str
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def passed_count(self) -> int:
        return sum(1 for result in self.results if result.status == CheckStatus.PASS)

    @property
    def warning_count(self) -> int:
        return sum(1 for result in self.results if result.status == CheckStatus.WARN)

    @property
    def failed_count(self) -> int:
        return sum(1 for result in self.results if result.status == CheckStatus.FAIL)

    @property
    def recommendations(self) -> List[str]:
        seen: set[str] = set()
        recommendations: List[str] = []
        for result in self.results:
            if result.recommendation and result.recommendation not in seen:
                seen.add(result.recommendation)
                recommendations.append(result.recommendation)
        return recommendations

    def to_dict(self) -> Dict[str, Any]:
        return {
            "generated_at": self.generated_at.isoformat(),
            "score": self.score,
            "grade": self.grade,
            "summary": {
                "passed": self.passed_count,
                "warnings": self.warning_count,
                "failed": self.failed_count,
                "total": len(self.results),
            },
            "repository": self.profile.to_dict(),
            "checks": [result.to_dict() for result in self.results],
            "recommendations": self.recommendations,
        }
