"""Scoring helpers for RepoPulse."""

from __future__ import annotations

from typing import Iterable

from repopulse.models import CheckResult


def calculate_score(results: Iterable[CheckResult]) -> int:
    """Calculate a normalized score out of 100."""

    result_list = list(results)
    max_points = sum(result.max_points for result in result_list)
    if max_points <= 0:
        return 0

    points = sum(max(result.points, 0) for result in result_list)
    return round((points / max_points) * 100)


def grade_for_score(score: int) -> str:
    """Return a simple letter grade for a health score."""

    if score >= 90:
        return "A+"
    if score >= 80:
        return "A"
    if score >= 70:
        return "B"
    if score >= 60:
        return "C"
    if score >= 50:
        return "D"
    return "F"
