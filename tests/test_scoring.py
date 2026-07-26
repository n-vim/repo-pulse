from repopulse.models import CheckResult, CheckStatus
from repopulse.scoring import calculate_score, grade_for_score


def make_result(points: int, max_points: int) -> CheckResult:
    return CheckResult(
        code="x",
        name="Check",
        category="Test",
        status=CheckStatus.PASS,
        points=points,
        max_points=max_points,
        message="ok",
    )


def test_calculate_score_normalizes_to_100() -> None:
    results = [make_result(5, 10), make_result(10, 10)]
    assert calculate_score(results) == 75


def test_calculate_score_handles_empty_results() -> None:
    assert calculate_score([]) == 0


def test_grade_for_score() -> None:
    assert grade_for_score(95) == "A+"
    assert grade_for_score(82) == "A"
    assert grade_for_score(74) == "B"
    assert grade_for_score(62) == "C"
    assert grade_for_score(51) == "D"
    assert grade_for_score(20) == "F"
