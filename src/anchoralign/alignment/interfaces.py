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
        band_width = params["band_width"]
        is_adaptive = params.get("adaptive", False)
        
        metadata = {
            "initial_band_width": band_width,
            "final_band_width": band_width,
            "retry_count": 0,
            "boundary_touched": False,
            "fallback_used": False,
            "decision_reason": reason,
            "gap_id": id(gap)
        }
        
        res = banded_dp_align(ref_slice, query_slice, config, band_width)
        
        if config.adaptive_band_enabled and is_adaptive:
            retries = 0
            while (res.boundary_touched or (len(res.aligned_reference) == 0 and (len(ref_slice) > 0 or len(query_slice) > 0))) and retries < config.max_band_retries:
                retries += 1
                band_width *= config.band_growth_factor
                res = banded_dp_align(ref_slice, query_slice, config, band_width)
            
            metadata["retry_count"] = retries
            metadata["final_band_width"] = band_width
            metadata["boundary_touched"] = res.boundary_touched
            
            if res.boundary_touched or (len(res.aligned_reference) == 0 and (len(ref_slice) > 0 or len(query_slice) > 0)):
                # Fallback to Full DP
                metadata["fallback_used"] = True
                res = full_dp_align(ref_slice, query_slice, config)
                res.strategy = "full_dp_fallback"
        else:
            if len(res.aligned_reference) == 0 and (len(ref_slice) > 0 or len(query_slice) > 0):
                # Legacy fallback
                metadata["fallback_used"] = True
                res = full_dp_align(ref_slice, query_slice, config)
                res.boundary_touched = True
                res.strategy = "full_dp_fallback"
                
        res.decision_metadata = metadata
        return res
    else:
        res = full_dp_align(ref_slice, query_slice, config)
        res.decision_metadata = {
            "initial_band_width": None,
            "final_band_width": None,
            "retry_count": 0,
            "boundary_touched": False,
            "fallback_used": False,
            "decision_reason": reason,
            "gap_id": id(gap)
        }
        return res
    
def banded_align(reference_gap: str, query_gap: str, config: AnchorAlignConfig) -> AlignmentResult:
    return banded_dp_align(reference_gap, query_gap, config, config.band_width)

def full_align(reference_gap: str, query_gap: str, config: AnchorAlignConfig) -> AlignmentResult:
    return full_dp_align(reference_gap, query_gap, config)
