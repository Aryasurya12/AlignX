from typing import List
from ..models.anchor import Anchor
from ..models.gap import Gap
from ..config import AnchorAlignConfig
from .gap_extractor import extract_gaps_engine
from .gap_classifier import classify_gap

def extract_gaps(reference: str, query: str, anchors: List[Anchor], config: AnchorAlignConfig) -> List[Gap]:
    """
    Phase 2 Gap Extraction and Classification.
    """
    gaps = extract_gaps_engine(reference, query, anchors)
    for gap in gaps:
        classify_gap(gap, config)
    return gaps
