import pytest
from anchoralign.gaps.gap_features import calculate_gap_features
from anchoralign.models.gap import Gap

def create_gap(r_start, r_end, q_start, q_end):
    return Gap("test", r_start, r_end, q_start, q_end, 0, 0, 0, 0.0)

def test_equal_lengths():
    g = create_gap(0, 5, 0, 5)
    calculate_gap_features(g)
    assert g.length_difference == 0
    assert g.mismatch_ratio == 0.0

def test_unequal_lengths():
    g = create_gap(0, 5, 0, 10)
    calculate_gap_features(g)
    assert g.length_difference == 5
    assert g.mismatch_ratio == 0.5

def test_zero_length_reference():
    g = create_gap(5, 5, 0, 10)
    calculate_gap_features(g)
    assert g.reference_length == 0
    assert g.length_difference == 10
    assert g.mismatch_ratio == 1.0

def test_zero_length_query():
    g = create_gap(0, 10, 5, 5)
    calculate_gap_features(g)
    assert g.query_length == 0
    assert g.length_difference == 10
    assert g.mismatch_ratio == 1.0

def test_both_zero():
    g = create_gap(0, 0, 0, 0)
    calculate_gap_features(g)
    assert g.length_difference == 0
    assert g.mismatch_ratio == 0.0
