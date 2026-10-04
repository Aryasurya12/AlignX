from typing import List
from ..models.anchor import Anchor
from ..models.alignment import AlignmentResult
from .reconstruct import reconstruct_alignment_engine

def reconstruct_alignment(reference: str, query: str, anchors: List[Anchor], aligned_gaps: List[AlignmentResult]) -> AlignmentResult:
    """
    Phase 3 Alignment reconstruction.
    Stitches ordered anchors and aligned gaps into a complete global alignment.
    """
    return reconstruct_alignment_engine(reference, query, anchors, aligned_gaps)
