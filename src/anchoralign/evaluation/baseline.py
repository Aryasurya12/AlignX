import time
from typing import Tuple, List, Dict
from ..alignment.full_dp import full_dp_align
from ..config import AnchorAlignConfig
from ..mutations.mutation_detector import detect_mutations_engine

def full_sequence_align(reference: str, query: str, config: AnchorAlignConfig) -> Tuple[str, str, int, float, List[Dict]]:
    start_time = time.perf_counter()
    
    # Run full DP over entire sequences
    result = full_dp_align(reference, query, config)
    
    # Detect mutations
    mutations = detect_mutations_engine(result.aligned_reference, result.aligned_query)
    
    end_time = time.perf_counter()
    runtime = end_time - start_time
    
    # Convert mutations to dict for generic use
    mutations_dict = [
        {
            "type": m.type.upper(),
            "ref_pos": m.reference_position,
            "ref_seq": m.reference_sequence,
            "query_seq": m.query_sequence
        }
        for m in mutations
    ]
    
    return result.aligned_reference, result.aligned_query, result.score, runtime, mutations_dict
