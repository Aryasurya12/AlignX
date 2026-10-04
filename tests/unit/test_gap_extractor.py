import pytest
from anchoralign.gaps.gap_extractor import extract_gaps_engine
from anchoralign.models.anchor import Anchor

def test_zero_anchors():
    gaps = extract_gaps_engine("ACGT", "TGCA", [])
    assert len(gaps) == 1
    g = gaps[0]
    assert g.reference_start == 0 and g.reference_end == 4
    assert g.query_start == 0 and g.query_end == 4

def test_one_anchor():
    anchors = [Anchor(1, 3, 1, 3, 2, "kmp")]
    gaps = extract_gaps_engine("AATT", "AATT", anchors)
    # prefix gap: 0..1, suffix gap: 3..4
    assert len(gaps) == 2
    assert gaps[0].reference_start == 0 and gaps[0].reference_end == 1
    assert gaps[1].reference_start == 3 and gaps[1].reference_end == 4

def test_prefix_internal_suffix():
    anchors = [Anchor(1, 2, 1, 2, 1, "kmp"), Anchor(4, 5, 4, 5, 1, "kmp")]
    gaps = extract_gaps_engine("AAAAAA", "AAAAAA", anchors)
    assert len(gaps) == 3
    assert gaps[0].id == "gap_prefix"
    assert gaps[1].id == "gap_internal_0"
    assert gaps[2].id == "gap_suffix"

def test_anchor_covering_complete_sequence():
    anchors = [Anchor(0, 4, 0, 4, 4, "kmp")]
    gaps = extract_gaps_engine("ACGT", "ACGT", anchors)
    assert len(gaps) == 0

def test_empty_sequences():
    gaps = extract_gaps_engine("", "", [])
    assert len(gaps) == 1
    assert gaps[0].reference_length == 0
