import pytest
from src.anchoralign.config import AnchorAlignConfig
from src.anchoralign.models.gap import Gap
from src.anchoralign.gaps.gap_classifier import classify_gap
from src.anchoralign.alignment.selector import select_strategy
from src.anchoralign.alignment.interfaces import align_gap
from src.anchoralign.pipeline.orchestrator import run_pipeline

def test_adaptive_band_calculation_and_safety_margin():
    config = AnchorAlignConfig(adaptive_band_enabled=True, band_safety_margin=5)
    gap = Gap(id="1", reference_start=0, reference_end=100, query_start=0, query_end=80, reference_length=100, query_length=80, length_difference=20, mismatch_ratio=0.2)
    
    classification, reason = classify_gap(gap, config)
    assert classification == "adaptive_band"
    
    strategy, reason, params = select_strategy(gap, config)
    assert strategy == "banded_dp"
    # length_diff = 20. safety = 5. drift = int(100 * 0.2 * 0.1) = 2.
    # Total = 20 + 5 + 2 = 27
    assert params["band_width"] == 27
    assert params["adaptive"] is True

def test_minimum_band_enforcement():
    config = AnchorAlignConfig(adaptive_band_enabled=True, band_safety_margin=10)
    gap = Gap(id="2", reference_start=0, reference_end=10, query_start=0, query_end=10, reference_length=10, query_length=10, length_difference=0, mismatch_ratio=0.0)
    
    classify_gap(gap, config)
    strategy, _, params = select_strategy(gap, config)
    # length_diff = 0. safety = 10. drift = 0.
    assert params["band_width"] == 10

def test_decision_metadata_and_reason():
    config = AnchorAlignConfig(adaptive_band_enabled=True)
    gap = Gap(id="3", reference_start=0, reference_end=5, query_start=0, query_end=5, reference_length=5, query_length=5, length_difference=0, mismatch_ratio=0.0)
    
    classify_gap(gap, config)
    strategy, reason, params = select_strategy(gap, config)
    assert "0 length difference" in reason or "Adaptive Banded DP selected" in reason
    
    ref = "ACGTA"
    query = "ACGTA"
    res = align_gap(gap, ref, query, config)
    assert res.decision_metadata is not None
    assert res.decision_metadata["retry_count"] == 0
    assert not res.decision_metadata["boundary_touched"]
    assert not res.decision_metadata["fallback_used"]
    assert res.decision_metadata["initial_band_width"] == params["band_width"]

def test_boundary_retry_and_full_dp_fallback():
    # Force a situation where band is too small and retries fail
    config = AnchorAlignConfig(adaptive_band_enabled=True, band_safety_margin=0, max_band_retries=0, band_growth_factor=2)
    # 20 length diff, very little mismatch ratio
    gap = Gap(id="4", reference_start=0, reference_end=50, query_start=0, query_end=30, reference_length=50, query_length=30, length_difference=20, mismatch_ratio=0.0)
    
    classify_gap(gap, config)
    # We provide a reference and query that has a large insertion that will hit the band boundary
    # A band of 20 won't cover an insertion of 25 followed by match
    ref = "A" * 50
    query = "B" * 25 + "A" * 50
    
    res = align_gap(gap, ref, query, config)
    
    assert res.decision_metadata["fallback_used"] is True
    assert res.decision_metadata["retry_count"] == 0
    assert res.strategy == "full_dp_fallback"

def test_adaptive_vs_fixed_correctness():
    # Test on a specific gap rather than the full pipeline to avoid anchor issues
    ref = "ACGTACGTACGT" * 5
    query = "ACGT" + "A"*10 + "ACGTACGT" * 4
    
    config_fixed = AnchorAlignConfig(adaptive_band_enabled=False, band_width=5)
    config_adaptive = AnchorAlignConfig(adaptive_band_enabled=True, band_safety_margin=2)
    
    gap = Gap(id="5", reference_start=0, reference_end=len(ref), query_start=0, query_end=len(query), reference_length=len(ref), query_length=len(query), length_difference=abs(len(ref)-len(query)), mismatch_ratio=0.1)
    
    classify_gap(gap, config_fixed)
    res_fixed = align_gap(gap, ref, query, config_fixed)
    
    classify_gap(gap, config_adaptive)
    res_adaptive = align_gap(gap, ref, query, config_adaptive)
    
    assert res_fixed.score == res_adaptive.score
    assert len(res_fixed.aligned_reference) == len(res_adaptive.aligned_reference)
