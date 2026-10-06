from ..models.gap import Gap
from ..config import AnchorAlignConfig
from typing import Tuple

def classify_gap(gap: Gap, config: AnchorAlignConfig) -> Tuple[str, str]:
    """
    Classifies a gap based on its features and configuration thresholds.
    Returns (classification_class, explanation).
    """
    is_short = gap.reference_length <= config.gap_length_threshold and gap.query_length <= config.gap_length_threshold
    is_matched = gap.mismatch_ratio <= config.gap_mismatch_threshold
    
    # We add detailed features for Phase 5
    length_diff = abs(gap.reference_length - gap.query_length)
    
    # Store length diff in gap for selector
    gap.length_difference = length_diff
    
    if config.adaptive_band_enabled:
        if length_diff > 0 or gap.mismatch_ratio > 0:
            classification = "adaptive_band"
            reason = f"Adaptive band selected. Length diff: {length_diff}, Mismatch ratio: {gap.mismatch_ratio:.2f}."
        else:
            classification = "exact_match"
            reason = "Gap has 0 length difference and 0 mismatch ratio."
    else:
        if is_short and is_matched:
            classification = "short_length_matched"
            reason = f"Gap is short (<= {config.gap_length_threshold}) and reference/query lengths are closely matched (ratio {gap.mismatch_ratio:.2f} <= {config.gap_mismatch_threshold})."
        else:
            classification = "long_or_length_mismatched"
            reason = f"Gap is long (> {config.gap_length_threshold}) or has substantial reference/query length mismatch (ratio {gap.mismatch_ratio:.2f} > {config.gap_mismatch_threshold})."
        
    gap.classification = classification
    return classification, reason
