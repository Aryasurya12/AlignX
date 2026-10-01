from typing import List
from ..models.anchor import Anchor
from ..models.gap import Gap
from .gap_features import calculate_gap_features

def extract_gaps_engine(reference: str, query: str, anchors: List[Anchor]) -> List[Gap]:
    """
    Extracts prefix, internal, and suffix gaps given ordered anchors.
    """
    gaps = []
    
    # 0 anchors case
    if not anchors:
        gap = Gap(
            id="gap_0",
            reference_start=0,
            reference_end=len(reference),
            query_start=0,
            query_end=len(query),
            reference_length=len(reference),
            query_length=len(query),
            length_difference=0,
            mismatch_ratio=0.0
        )
        calculate_gap_features(gap)
        gaps.append(gap)
        return gaps
        
    # Prefix gap
    first_anchor = anchors[0]
    if first_anchor.reference_start > 0 or first_anchor.query_start > 0:
        gap = Gap(
            id="gap_prefix",
            reference_start=0,
            reference_end=first_anchor.reference_start,
            query_start=0,
            query_end=first_anchor.query_start,
            reference_length=0, query_length=0, length_difference=0, mismatch_ratio=0.0
        )
        calculate_gap_features(gap)
        gaps.append(gap)
        
    # Internal gaps
    for i in range(len(anchors) - 1):
        a = anchors[i]
        b = anchors[i+1]
        
        # Only create if there's actual sequence gap
        if a.reference_end < b.reference_start or a.query_end < b.query_start:
            gap = Gap(
                id=f"gap_internal_{i}",
                reference_start=a.reference_end,
                reference_end=b.reference_start,
                query_start=a.query_end,
                query_end=b.query_start,
                reference_length=0, query_length=0, length_difference=0, mismatch_ratio=0.0
            )
            calculate_gap_features(gap)
            gaps.append(gap)
            
    # Suffix gap
    last_anchor = anchors[-1]
    if last_anchor.reference_end < len(reference) or last_anchor.query_end < len(query):
        gap = Gap(
            id="gap_suffix",
            reference_start=last_anchor.reference_end,
            reference_end=len(reference),
            query_start=last_anchor.query_end,
            query_end=len(query),
            reference_length=0, query_length=0, length_difference=0, mismatch_ratio=0.0
        )
        calculate_gap_features(gap)
        gaps.append(gap)
        
    return gaps
