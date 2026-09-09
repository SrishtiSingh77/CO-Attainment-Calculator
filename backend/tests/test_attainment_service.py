import pytest

from app.services.attainment import calculate_attainment


def test_score_exactly_at_threshold_counts_as_met():
    result = calculate_attainment(scores=[50.0], threshold=50.0)
    assert result["students_met"] == 1
    assert result["attainment_percentage"] == 100.0


def test_score_above_threshold_counts_as_met():
    result = calculate_attainment(scores=[75.0], threshold=50.0)
    assert result["students_met"] == 1
    assert result["attainment_percentage"] == 100.0


def test_score_below_threshold_does_not_count():
    result = calculate_attainment(scores=[40.0], threshold=50.0)
    assert result["students_met"] == 0
    assert result["attainment_percentage"] == 0.0


def test_empty_scores_returns_zero_no_division_error():
    result = calculate_attainment(scores=[], threshold=50.0)
    assert result["total_students"] == 0
    assert result["students_met"] == 0
    assert result["attainment_percentage"] == 0.0


def test_mixed_scores_calculates_correct_percentage():
    # 3 of 4 meet the threshold of 50 (50, 60, 90 meet; 40 does not)
    result = calculate_attainment(scores=[40.0, 50.0, 60.0, 90.0], threshold=50.0)
    assert result["total_students"] == 4
    assert result["students_met"] == 3
    assert result["attainment_percentage"] == 75.0


@pytest.mark.parametrize("threshold", [-1, 101, 150])
def test_invalid_threshold_raises_value_error(threshold):
    with pytest.raises(ValueError):
        calculate_attainment(scores=[50.0], threshold=threshold)


def test_threshold_boundary_values_are_valid():
    # 0 and 100 are valid thresholds, should not raise
    calculate_attainment(scores=[0.0], threshold=0)
    calculate_attainment(scores=[100.0], threshold=100)
