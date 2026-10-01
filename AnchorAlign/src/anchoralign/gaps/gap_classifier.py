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
    
    if is_short and is_matched:
        classification = "short_length_matched"
        reason = f"Gap is short (<= {config.gap_length_threshold}) and reference/query lengths are closely matched (ratio {gap.mismatch_ratio:.2f} <= {config.gap_mismatch_threshold})."
    else:
        classification = "long_or_length_mismatched"
        reason = f"Gap is long (> {config.gap_length_threshold}) or has substantial reference/query length mismatch (ratio {gap.mismatch_ratio:.2f} > {config.gap_mismatch_threshold})."
        
    gap.classification = classification
    return classification, reason
