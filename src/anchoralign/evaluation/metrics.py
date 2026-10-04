from typing import List, Dict, Any

def check_correctness(adaptive_score: int, baseline_score: int) -> bool:
    """
    Checks if adaptive alignment is correct relative to the baseline.
    Since different alignments can have the same optimal score, matching the score
    is the primary criterion for mathematical correctness.
    """
    return adaptive_score == baseline_score

def compute_speedup(baseline_time: float, adaptive_time: float) -> float:
    if adaptive_time <= 0:
        return 0.0
    return baseline_time / adaptive_time

def compute_anchor_coverage(anchor_bases: int, reference_length: int) -> float:
    if reference_length <= 0:
        return 0.0
    return anchor_bases / reference_length
