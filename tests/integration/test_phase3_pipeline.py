import pytest
from anchoralign.pipeline.orchestrator import run_pipeline
from anchoralign.config import AnchorAlignConfig

def test_pipeline_identical():
    config = AnchorAlignConfig(L_min=2)
    res = run_pipeline("ACGT", "ACGT", config)
    assert len(res.mutations) == 0

def test_pipeline_substitution():
    config = AnchorAlignConfig(L_min=2)
    res = run_pipeline("ACGT", "ACCT", config)
    assert len(res.mutations) == 1
    assert res.mutations[0].type == "substitution"
    assert res.mutations[0].reference_sequence == "G"
    assert res.mutations[0].query_sequence == "C"

def test_pipeline_insertion():
    config = AnchorAlignConfig(L_min=2)
    res = run_pipeline("ACGT", "ACAGT", config)
    assert len(res.mutations) == 1
    assert res.mutations[0].type == "insertion"
    assert res.mutations[0].query_sequence == "A"

def test_pipeline_deletion():
    config = AnchorAlignConfig(L_min=2)
    res = run_pipeline("ACAGT", "ACGT", config)
    assert len(res.mutations) == 1
    assert res.mutations[0].type == "deletion"
    assert res.mutations[0].reference_sequence == "A"

def test_pipeline_compound_clustering():
    config = AnchorAlignConfig(L_min=2, clustering_k=3)
    # T -> C at 2, A insertion after 3
    res = run_pipeline("ACGTAC", "ACCTAGAC", config)
    # mut 1: G -> C at 2. mut 2: insertion GA at 4.
    assert len(res.compound_events) == 1
    assert res.compound_events[0]["mutation_count"] == 2
    
def test_pipeline_warning_propagation():
    # Force a narrow band and a large shift
    config = AnchorAlignConfig(band_width=2, L_min=50, mismatch_penalty=-5, gap_penalty=-1)
    # The gap extractor will give 1 gap for the whole thing.
    res = run_pipeline("AAA" + "C"*10, "C"*10 + "AAA", config)
    assert any("boundary_touched" in w for w in res.warnings)
