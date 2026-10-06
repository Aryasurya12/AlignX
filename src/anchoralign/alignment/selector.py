from ..models.gap import Gap
from ..config import AnchorAlignConfig
from typing import Tuple, Dict, Any

def select_strategy(gap: Gap, config: AnchorAlignConfig) -> Tuple[str, str, Dict[str, Any]]:
    """
    Deterministically chooses 'banded_dp' or 'full_dp' based on gap classification.
    Returns (strategy, reason, parameters).
    """
    if config.adaptive_band_enabled:
        if gap.classification in ["adaptive_band", "exact_match"]:
            # Base bandwidth is length diff + safety margin
            # Add a small proportion of gap length for mismatch/drift safety
            drift = int(max(gap.reference_length, gap.query_length) * gap.mismatch_ratio * 0.1)
            estimated_band = getattr(gap, 'length_difference', abs(gap.reference_length - gap.query_length)) + config.band_safety_margin + drift
            
            # Bound estimated band to reasonable limits
            estimated_band = max(config.band_safety_margin, estimated_band)
            
            # If band gets close to full DP sizes anyway, just use Full DP?
            # Actually, let's keep it bounded to config.band_width if we want to fallback? No, adaptive band doesn't care.
            
            # We don't use Full DP initially in adaptive mode unless the band is extremely huge.
            # But the user specifies "fallback policy". We try banded DP first!
            
            reason = f"Adaptive Banded DP selected. Length difference is {getattr(gap, 'length_difference', 0)}, estimated band is {estimated_band}."
            return ("banded_dp", reason, {"band_width": estimated_band, "adaptive": True})
        else:
            return ("full_dp", "Fallback to Full DP.", {})
    else:
        if gap.classification == "short_length_matched":
            return ("banded_dp", "Short gap with small reference/query length mismatch.", {"band_width": config.band_width})
        else:
            return ("full_dp", "Gap is long or has significant length mismatch.", {})

