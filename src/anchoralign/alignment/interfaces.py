from ..models.gap import Gap
from ..models.alignment import AlignmentResult
from ..config import AnchorAlignConfig
from .full_dp import full_dp_align
from .banded_dp import banded_dp_align
from .selector import select_strategy

def align_gap(gap: Gap, reference: str, query: str, config: AnchorAlignConfig) -> AlignmentResult:
    """
    Adaptive Alignment Engine entry point.
    Extracts the actual sequence slices for the gap and runs the selected strategy.
    """
    ref_slice = reference[gap.reference_start:gap.reference_end]
    query_slice = query[gap.query_start:gap.query_end]
    
    strategy, reason, params = select_strategy(gap, config)
    gap.selected_strategy = strategy
    
    if strategy == "banded_dp":
        return banded_dp_align(ref_slice, query_slice, config, params["band_width"])
    else:
        return full_dp_align(ref_slice, query_slice, config)
    
def banded_align(reference_gap: str, query_gap: str, config: AnchorAlignConfig) -> AlignmentResult:
    return banded_dp_align(reference_gap, query_gap, config, config.band_width)

def full_align(reference_gap: str, query_gap: str, config: AnchorAlignConfig) -> AlignmentResult:
    return full_dp_align(reference_gap, query_gap, config)
