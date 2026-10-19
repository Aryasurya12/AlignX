import pytest
from anchoralign.gaps.gap_classifier import classify_gap
from anchoralign.models.gap import Gap
from anchoralign.config import AnchorAlignConfig

def test_short_length_matched_gap():
    config = AnchorAlignConfig(adaptive_band_enabled=False, gap_length_threshold=10, gap_mismatch_threshold=0.2)
    gap = Gap("g1", 0, 5, 0, 5, 5, 5, 0, 0.0)
    classification, reason = classify_gap(gap, config)
    assert classification == "short_length_matched"

def test_short_mismatched_gap():
    config = AnchorAlignConfig(adaptive_band_enabled=False, gap_length_threshold=10, gap_mismatch_threshold=0.2)
    gap = Gap("g1", 0, 5, 0, 10, 5, 10, 5, 0.5)
    classification, reason = classify_gap(gap, config)
    assert classification == "long_or_length_mismatched"

def test_long_matched_gap():
    config = AnchorAlignConfig(adaptive_band_enabled=False, gap_length_threshold=10, gap_mismatch_threshold=0.2)
    gap = Gap("g1", 0, 20, 0, 20, 20, 20, 0, 0.0)
    classification, reason = classify_gap(gap, config)
    assert classification == "long_or_length_mismatched"

def test_long_mismatched_gap():
    config = AnchorAlignConfig(adaptive_band_enabled=False, gap_length_threshold=10, gap_mismatch_threshold=0.2)
    gap = Gap("g1", 0, 20, 0, 30, 20, 30, 10, 0.33)
    classification, reason = classify_gap(gap, config)
    assert classification == "long_or_length_mismatched"

def test_explanation_correctness():
    config = AnchorAlignConfig(adaptive_band_enabled=False, gap_length_threshold=10, gap_mismatch_threshold=0.2)
    gap = Gap("g1", 0, 5, 0, 5, 5, 5, 0, 0.0)
    c, r = classify_gap(gap, config)
    assert "closely matched" in r

def test_adaptive_classification():
    """Test adaptive mode classifies gaps as adaptive_band or exact_match."""
    config = AnchorAlignConfig(adaptive_band_enabled=True)
    gap = Gap("g1", 0, 10, 0, 12, 10, 12, 2, 0.1)
    classification, reason = classify_gap(gap, config)
    assert classification == "adaptive_band"

def test_adaptive_exact_match():
    """Test adaptive mode classifies zero-difference gaps as exact_match."""
    config = AnchorAlignConfig(adaptive_band_enabled=True)
    gap = Gap("g1", 0, 10, 0, 10, 10, 10, 0, 0.0)
    classification, reason = classify_gap(gap, config)
    assert classification == "exact_match"
