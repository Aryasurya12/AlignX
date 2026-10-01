import pytest
from anchoralign.anchors.anchor_resolver import run_anchor_engine, generate_candidates, merge_anchors, resolve_conflicts
from anchoralign.config import AnchorAlignConfig
from anchoralign.models.anchor import Anchor

def test_identical_sequences():
    config = AnchorAlignConfig(L_min=2, anchor_algorithm="kmp")
    anchors, diag = run_anchor_engine("ACGT", "ACGT", config)
    assert len(anchors) == 1
    a = anchors[0]
    assert a.reference_start == 0 and a.reference_end == 4
    assert a.query_start == 0 and a.query_end == 4
    assert a.length == 4

def test_one_exact_matching_region():
    config = AnchorAlignConfig(L_min=3, anchor_algorithm="kmp")
    anchors, _ = run_anchor_engine("TTTACGTTTT", "CCACGTC", config)
    assert len(anchors) == 1
    a = anchors[0]
    assert a.reference_start == 3 and a.reference_end == 7
    assert a.query_start == 2 and a.query_end == 6

def test_multiple_anchors():
    config = AnchorAlignConfig(L_min=3)
    anchors, _ = run_anchor_engine("AAAACGTGGGGACGT", "CCACGTCCCCACGT", config)
    assert len(anchors) == 2
    assert anchors[0].reference_start == 3
    assert anchors[1].reference_start == 11

def test_one_mutation_between():
    config = AnchorAlignConfig(L_min=3)
    anchors, _ = run_anchor_engine("ACGTACGT", "ACGTCACGT", config)
    assert len(anchors) == 2

def test_overlapping_candidate_matches():
    config = AnchorAlignConfig(L_min=2)
    # pattern AA overlaps in AAAA
    anchors, _ = run_anchor_engine("AAAA", "AAAA", config)
    assert len(anchors) == 1
    assert anchors[0].length == 4

def test_no_sufficiently_long_anchors():
    config = AnchorAlignConfig(L_min=5)
    anchors, _ = run_anchor_engine("ACGT", "ACGT", config)
    assert len(anchors) == 0

def test_l_min_filtering():
    config = AnchorAlignConfig(L_min=3)
    anchors, _ = run_anchor_engine("ACGT", "ACG", config)
    assert len(anchors) == 1
    config2 = AnchorAlignConfig(L_min=4)
    anchors2, _ = run_anchor_engine("ACGT", "ACG", config2)
    assert len(anchors2) == 0

def test_anchor_merging():
    # Tested effectively by identical_sequences where multiple L_min matches merge into 1 big anchor
    config = AnchorAlignConfig(L_min=2)
    anchors, diag = run_anchor_engine("ACGT", "ACGT", config)
    assert diag["merged_anchor_count"] == 1
    assert anchors[0].length == 4

def test_no_merge_case():
    config = AnchorAlignConfig(L_min=2)
    anchors, _ = run_anchor_engine("ACGGGT", "ACCCGT", config)
    # AC and GT should be two separate anchors
    assert len(anchors) == 2
    assert anchors[0].length == 2
    assert anchors[1].length == 2

def test_conflicting_anchors():
    config = AnchorAlignConfig(L_min=3)
    # "ACGT" and "CGTA". Suppose reference has "ACGTA", query has "ACGT" and "CGTA" in strange places
    anchors, _ = run_anchor_engine("ACGTA", "CGTACGT", config)
    # query has CGT at 0, ACGT at 3.
    # ref has ACGT at 0, CGTA at 1.
    # length 4 anchor: ref=0..4, query=3..7. Length 4 anchor: ref=1..5, query=0..4.
    # They overlap in reference. Conflict resolution should pick one.
    assert len(anchors) == 1
    assert anchors[0].length == 4

def test_deterministic_ordering():
    config = AnchorAlignConfig(L_min=2)
    anchors, _ = run_anchor_engine("ACGT", "ACGT", config)
    assert anchors[0].reference_start == 0

def test_short_sequences():
    config = AnchorAlignConfig(L_min=10)
    anchors, _ = run_anchor_engine("A", "A", config)
    assert len(anchors) == 0

def test_empty_sequences():
    config = AnchorAlignConfig(L_min=2)
    anchors, _ = run_anchor_engine("", "", config)
    assert len(anchors) == 0

def test_invariants():
    config = AnchorAlignConfig(L_min=3)
    anchors, _ = run_anchor_engine("ACGTAAAGGGTTTACGT", "ACGTCCCACGTTTT", config)
    for i, a in enumerate(anchors):
        assert a.reference_start < a.reference_end
        assert a.query_start < a.query_end
        assert a.length == a.reference_end - a.reference_start
        assert a.length == a.query_end - a.query_start
        assert a.length >= config.L_min
        
        if i > 0:
            assert anchors[i-1].reference_end <= a.reference_start
            assert anchors[i-1].query_end <= a.query_start

def test_rabin_karp_execution():
    config = AnchorAlignConfig(L_min=2, anchor_algorithm="rabin-karp")
    anchors, diag = run_anchor_engine("ACGT", "ACGT", config)
    assert len(anchors) == 1
    assert anchors[0].length == 4
    assert anchors[0].source_algorithm == "rabin-karp"
