import pytest
from anchoralign.reconstruction.reconstruct import reconstruct_alignment_engine
from anchoralign.models.anchor import Anchor
from anchoralign.models.alignment import AlignmentResult

def test_identical_sequences():
    ref = "ACGTACGT"
    query = "ACGTACGT"
    anchors = [Anchor(0, 8, 0, 8, 8, "kmp")]
    # 0 gaps
    res = reconstruct_alignment_engine(ref, query, anchors, [])
    assert res.aligned_reference == "ACGTACGT"
    assert res.aligned_query == "ACGTACGT"

def test_substitution():
    ref = "ACGT"
    query = "ACAT"
    anchors = [Anchor(0, 2, 0, 2, 2, "kmp")]
    aligned_gaps = [AlignmentResult("GT", "AT", 0, "full_dp", 0, False)]
    res = reconstruct_alignment_engine(ref, query, anchors, aligned_gaps)
    assert res.aligned_reference == "ACGT"
    assert res.aligned_query == "ACAT"

def test_insertion():
    ref = "ACGT"
    query = "ACAGT"
    anchors = [Anchor(0, 2, 0, 2, 2, "kmp"), Anchor(2, 4, 3, 5, 2, "kmp")]
    aligned_gaps = [AlignmentResult("-", "A", 0, "full_dp", 0, False)]
    res = reconstruct_alignment_engine(ref, query, anchors, aligned_gaps)
    assert res.aligned_reference == "AC-GT"
    assert res.aligned_query == "ACAGT"

def test_deletion():
    ref = "ACAGT"
    query = "ACGT"
    anchors = [Anchor(0, 2, 0, 2, 2, "kmp"), Anchor(3, 5, 2, 4, 2, "kmp")]
    aligned_gaps = [AlignmentResult("A", "-", 0, "full_dp", 0, False)]
    res = reconstruct_alignment_engine(ref, query, anchors, aligned_gaps)
    assert res.aligned_reference == "ACAGT"
    assert res.aligned_query == "AC-GT"
    
def test_zero_anchors():
    ref = "ACGT"
    query = "TGCA"
    aligned_gaps = [AlignmentResult("ACGT", "TGCA", 0, "full_dp", 0, False)]
    res = reconstruct_alignment_engine(ref, query, [], aligned_gaps)
    assert res.aligned_reference == "ACGT"
    assert res.aligned_query == "TGCA"

def test_invalid_gap_length():
    with pytest.raises(ValueError, match="Number of gaps"):
        reconstruct_alignment_engine("ACGT", "ACGT", [], [])

def test_validation_failure():
    # Provide a gap alignment that doesn't match the original sequences
    ref = "ACGT"
    query = "ACAT"
    anchors = [Anchor(0, 2, 0, 2, 2, "kmp")]
    # Fake aligned_gap that is completely wrong
    aligned_gaps = [AlignmentResult("GG", "CC", 0, "full_dp", 0, False)]
    with pytest.raises(ValueError, match="Aligned gap reference does not match original sequence"):
        reconstruct_alignment_engine(ref, query, anchors, aligned_gaps)
        
def test_boundary_warning_propagation():
    ref = "ACGT"
    query = "ACAT"
    aligned_gaps = [AlignmentResult("ACGT", "ACAT", 0, "banded_dp", 2, True)]
    res = reconstruct_alignment_engine(ref, query, [], aligned_gaps)
    assert res.boundary_touched == True
