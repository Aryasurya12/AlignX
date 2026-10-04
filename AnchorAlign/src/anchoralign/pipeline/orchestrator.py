from ..config import AnchorAlignConfig
from ..preprocessing.sequence import preprocess_sequence
from ..anchors.interfaces import find_anchors
from ..gaps.interfaces import extract_gaps
from ..alignment.interfaces import align_gap
from ..reconstruction.interfaces import reconstruct_alignment
from ..mutations.interfaces import detect_mutations, get_compound_events
from ..models.result import FinalResult

def run_pipeline(reference: str, query: str, config: AnchorAlignConfig = None) -> FinalResult:
    if config is None:
        config = AnchorAlignConfig()
    
    # 1. Preprocessing
    ref_norm = preprocess_sequence(reference)
    query_norm = preprocess_sequence(query)
    
    # 2. Anchor Engine
    anchors = find_anchors(ref_norm, query_norm, config)
    
    # 3. Gap Engine
    gaps = extract_gaps(ref_norm, query_norm, anchors, config)
    
    # 4. Adaptive Alignment
    aligned_gaps = []
    for gap in gaps:
        aligned_result = align_gap(gap, ref_norm, query_norm, config)
        aligned_gaps.append(aligned_result)
    
    # 5. Reconstruction
    final_alignment = reconstruct_alignment(ref_norm, query_norm, anchors, aligned_gaps)
    
    # 6. Mutation Engine
    mutations = detect_mutations(final_alignment)
    
    # 7. Compound Clustering
    compound_events = get_compound_events(mutations, config)
    
    # Check boundary warnings
    warnings = []
    if final_alignment.boundary_touched:
        warnings.append("Banded DP boundary_touched=True. The optimal alignment might have drifted outside the band.")
    
    # 8. Final Result Construction
    return FinalResult(
        reference_length=len(ref_norm),
        query_length=len(query_norm),
        anchors=anchors,
        gaps=gaps,
        alignments=aligned_gaps,
        mutations=mutations,
        compound_events=compound_events,
        warnings=warnings,
        configuration=config,
        final_alignment=final_alignment
    )
