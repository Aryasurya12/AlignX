from ..config import AnchorAlignConfig
from ..preprocessing.sequence import preprocess_sequence
from ..anchors.interfaces import find_anchors
from ..gaps.interfaces import extract_gaps
from ..alignment.interfaces import align_gap
from ..reconstruction.interfaces import reconstruct_alignment
from ..mutations.interfaces import detect_mutations
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
    final_alignment = reconstruct_alignment(anchors, aligned_gaps)
    
    # 6. Mutation Engine
    mutations = detect_mutations(final_alignment)
    
    # 7. Final Result Construction
    return FinalResult(
        reference_length=len(ref_norm),
        query_length=len(query_norm),
        anchors=anchors,
        gaps=gaps,
        alignments=aligned_gaps,
        mutations=mutations,
        configuration=config
    )
