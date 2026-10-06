from dataclasses import dataclass

@dataclass
class AnchorAlignConfig:
    L_min: int = 10
    anchor_merge_threshold: int = 5
    band_width: int = 100
    gap_length_threshold: int = 50
    gap_mismatch_threshold: float = 0.2
    match_score: int = 2
    mismatch_penalty: int = -1
    gap_penalty: int = -2
    clustering_k: int = 3
    anchor_algorithm: str = "kmp"
    
    # Phase 5 Adaptive Options
    adaptive_band_enabled: bool = False
    band_safety_margin: int = 2
    max_band_retries: int = 2
    band_growth_factor: int = 2
