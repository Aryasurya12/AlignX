import pytest
from anchoralign.pipeline.orchestrator import run_pipeline
from anchoralign.config import AnchorAlignConfig

def test_preset_identical():
    ref = "ATGCGATCGATCGATCGATC" * 10
    query = "ATGCGATCGATCGATCGATC" * 10
    config = AnchorAlignConfig(adaptive_band_enabled=True)
    res = run_pipeline(ref, query, config)
    assert res.final_alignment.score is not None

def test_preset_substitution():
    ref = "ATGCGATCGATCGATCGATC" * 10
    query = "ATGCGATCG" + "T" + "TCGATCGATC" + "ATGCGATCGATCGATCGATC" * 9
    config = AnchorAlignConfig(adaptive_band_enabled=True)
    res = run_pipeline(ref, query, config)
    assert res.final_alignment.score is not None

def test_preset_insertion():
    ref = "A"*50 + "C"*50 + "G"*50 + "T"*50
    query = "A"*50 + "C"*50 + "AAAAA" + "G"*50 + "T"*50
    config = AnchorAlignConfig(adaptive_band_enabled=True)
    res = run_pipeline(ref, query, config)
    assert res.final_alignment.score is not None

def test_preset_long_indel():
    ref = "A" * 100 + "G" * 50
    query = "A" * 10 + "T" * 80 + "A" * 90 + "G" * 50
    config = AnchorAlignConfig(adaptive_band_enabled=True, band_safety_margin=5)
    res = run_pipeline(ref, query, config)
    assert len(res.alignments) > 0

def test_preset_complex():
    ref = "ACGT" * 20 + "TGCA" * 20
    query = "ACGT" * 5 + "AAAAA" + "ACGT" * 5 + "G" + "ACGT" * 9 + "TGCA" * 20
    config = AnchorAlignConfig(adaptive_band_enabled=True)
    res = run_pipeline(ref, query, config)
    assert res.final_alignment.score is not None

def test_export_report_payload():
    ref = "ACGT" * 10
    query = "ACGT" * 10
    config = AnchorAlignConfig(adaptive_band_enabled=True)
    res = run_pipeline(ref, query, config)
    
    # Simulate UI export
    export_data = {
        "config": config.__dict__,
        "metrics": {
            "reference_length": res.reference_length,
            "query_length": res.query_length,
            "score": res.final_alignment.score,
            "anchors": len(res.anchors),
            "gaps": len(res.gaps),
            "mutations": len(res.mutations)
        }
    }
    
    assert export_data["metrics"]["score"] is not None
    assert export_data["metrics"]["reference_length"] == 40
    assert export_data["metrics"]["query_length"] == 40
    assert "band_width" in export_data["config"]
