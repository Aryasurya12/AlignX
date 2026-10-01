from typing import List
from ..models.anchor import Anchor
from ..config import AnchorAlignConfig
from .anchor_resolver import run_anchor_engine

def find_anchors(reference: str, query: str, config: AnchorAlignConfig) -> List[Anchor]:
    """
    Phase 1 Anchor Engine entry point.
    """
    anchors, _ = run_anchor_engine(reference, query, config)
    return anchors
