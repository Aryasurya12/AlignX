from anchoralign.models.anchor import Anchor
from anchoralign.models.gap import Gap
from anchoralign.models.alignment import AlignmentResult
from anchoralign.models.mutation import Mutation
from anchoralign.models.result import FinalResult

def test_anchor_creation():
    a = Anchor(0, 10, 0, 10, 10, "kmp")
    assert a.length == 10

def test_gap_creation():
    g = Gap("g1", 10, 20, 10, 20, 10, 10, 0, 0.0)
    assert g.id == "g1"

def test_alignment_result_creation():
    r = AlignmentResult("ACGT", "ACGT", 10.0, "full", 0, False)
    assert r.score == 10.0

def test_mutation_creation():
    m = Mutation("substitution", 5, 5, "A", "T")
    assert m.type == "substitution"

def test_final_result_creation():
    r = FinalResult(10, 10)
    assert r.reference_length == 10
    assert r.query_length == 10
