import pytest
from anchoralign.alignment.banded_dp import banded_dp_align
from anchoralign.alignment.full_dp import full_dp_align
from anchoralign.config import AnchorAlignConfig

def test_identical_sequences():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-1, gap_penalty=-2)
    res = banded_dp_align("ACGT", "ACGT", config, 2)
    assert res.score == 4

def test_substitution():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-1, gap_penalty=-2)
    res = banded_dp_align("ACGT", "ACCT", config, 2)
    assert res.score == 2

def test_insertion():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-1, gap_penalty=-2)
    res = banded_dp_align("ACT", "ACGT", config, 2)
    assert res.score == 1

def test_deletion():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-1, gap_penalty=-2)
    res = banded_dp_align("ACGT", "ACT", config, 2)
    assert res.score == 1

def test_band_width_0():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-1, gap_penalty=-2)
    res = banded_dp_align("ACGT", "ACGT", config, 0)
    assert res.score == 4
    assert res.boundary_touched == True # It's exactly on the diagonal boundary

def test_sufficient_band_agrees_with_full_dp():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-1, gap_penalty=-2)
    res_b = banded_dp_align("ACGTTT", "ACGGGTT", config, 5)
    res_f = full_dp_align("ACGTTT", "ACGGGTT", config)
    assert res_b.score == res_f.score

def test_narrow_band():
    config = AnchorAlignConfig(match_score=1, mismatch_penalty=-5, gap_penalty=-1)
    # The optimal alignment requires moving far off the diagonal
    res_b = banded_dp_align("AAA" + "C"*10, "C"*10 + "AAA", config, 2)
    res_f = full_dp_align("AAA" + "C"*10, "C"*10 + "AAA", config)
    assert res_b.score != res_f.score
    assert res_b.boundary_touched == True
