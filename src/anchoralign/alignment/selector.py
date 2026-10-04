from ..models.gap import Gap
from ..config import AnchorAlignConfig
from typing import Tuple, Dict, Any

def select_strategy(gap: Gap, config: AnchorAlignConfig) -> Tuple[str, str, Dict[str, Any]]:
    """
    Deterministically chooses 'banded_dp' or 'full_dp' based on gap classification.
    Returns (strategy, reason, parameters).
    """
    if gap.classification == "short_length_matched":
        return ("banded_dp", "Short gap with small reference/query length mismatch.", {"band_width": config.band_width})
    else:
        return ("full_dp", "Gap is long or has significant length mismatch.", {})
