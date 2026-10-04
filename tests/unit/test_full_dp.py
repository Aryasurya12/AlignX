import pytest
from anchoralign.alignment.full_dp import full_dp_align
from anchoralign.config import AnchorAlignConfig

def test_identical_sequences():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-1, gap_penalty=-2)
    res = full_dp_align("ACGT", "ACGT", config)
    assert res.score == 4
    assert res.aligned_reference == "ACGT"
    assert res.aligned_query == "ACGT"

def test_substitution():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-1, gap_penalty=-2)
    res = full_dp_align("ACGT", "ACCT", config)
    assert res.score == 2
    assert res.aligned_reference == "ACGT"
    assert res.aligned_query == "ACCT"

def test_insertion():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-1, gap_penalty=-2)
    res = full_dp_align("ACT", "ACGT", config)
    assert res.score == 1
    assert len(res.aligned_reference) == 4

def test_deletion():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-1, gap_penalty=-2)
    res = full_dp_align("ACGT", "ACT", config)
    assert res.score == 1
    assert len(res.aligned_query) == 4

def test_empty_reference():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-1, gap_penalty=-2)
    res = full_dp_align("", "ACGT", config)
    assert res.score == -8

def test_empty_query():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-1, gap_penalty=-2)
    res = full_dp_align("ACGT", "", config)
    assert res.score == -8

def test_both_empty():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-1, gap_penalty=-2)
    res = full_dp_align("", "", config)
    assert res.score == 0

def test_alignment_length_equality():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-1, gap_penalty=-2)
    res = full_dp_align("ACGT", "TGCA", config)
    assert len(res.aligned_reference) == len(res.aligned_query)
