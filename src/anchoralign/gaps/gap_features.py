from ..models.gap import Gap

def calculate_gap_features(gap: Gap) -> None:
    """
    Calculate length_difference and mismatch_ratio for a Gap in-place.
    """
    gap.reference_length = gap.reference_end - gap.reference_start
    gap.query_length = gap.query_end - gap.query_start
    
    gap.length_difference = abs(gap.reference_length - gap.query_length)
    
    max_len = max(gap.reference_length, gap.query_length)
    if max_len == 0:
        gap.mismatch_ratio = 0.0
    else:
        gap.mismatch_ratio = gap.length_difference / max_len
