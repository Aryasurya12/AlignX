from typing import List, Dict, Any
from ..models.anchor import Anchor
from ..config import AnchorAlignConfig
from .kmp import kmp_search
from .rabin_karp import rabin_karp_search

def generate_candidates(reference: str, query: str, config: AnchorAlignConfig) -> List[Anchor]:
    """
    Conceptually, this should find all exact matches >= L_min.
    For demonstration of Phase 1, we will generate candidate anchors by treating 
    substrings of the query of length L_min as patterns and searching them in the reference.
    We'll do this sequentially for the query to build up a set of candidate matches.
    In a real full implementation, a suffix tree/array might be used to find ALL maximal exact matches, 
    but for this project, we explicitly use KMP/RK as requested to find exact matches.
    
    Since we need to find long matches, we'll extract overlapping k-mers from query (k=L_min),
    find them in reference using the chosen algorithm, and create initial L_min anchors.
    Then we can merge them to form longer anchors.
    """
    L_min = config.L_min
    algo = config.anchor_algorithm
    
    candidates = []
    if len(query) < L_min or len(reference) < L_min:
        return candidates
        
    # Extract patterns of length L_min from query and search in reference
    for q_start in range(len(query) - L_min + 1):
        pattern = query[q_start:q_start + L_min]
        
        if algo == "kmp":
            ref_starts = kmp_search(reference, pattern)
        elif algo == "rabin-karp":
            ref_starts = rabin_karp_search(reference, pattern)
        else:
            ref_starts = kmp_search(reference, pattern) # default
            
        for r_start in ref_starts:
            candidates.append(Anchor(
                reference_start=r_start,
                reference_end=r_start + L_min,
                query_start=q_start,
                query_end=q_start + L_min,
                length=L_min,
                source_algorithm=algo
            ))
            
    return candidates

def merge_anchors(candidates: List[Anchor], config: AnchorAlignConfig) -> List[Anchor]:
    """
    Merge overlapping or adjacent candidate anchors if they form a continuous exact match.
    Candidates must have the same offset (reference_start - query_start) to be merged as a single exact match block.
    Two anchors can be merged if they overlap or are adjacent and share the same offset.
    """
    if not candidates:
        return []
        
    # Group by offset
    offset_groups = {}
    for c in candidates:
        offset = c.reference_start - c.query_start
        if offset not in offset_groups:
            offset_groups[offset] = []
        offset_groups[offset].append(c)
        
    merged = []
    
    for offset, group in offset_groups.items():
        # Sort by reference start
        group.sort(key=lambda x: x.reference_start)
        
        current = group[0]
        for next_anc in group[1:]:
            # Check if they overlap or are adjacent within merge threshold
            # Since they are exact matches of length L_min with same offset, if reference coords overlap/adjacent, so do query coords.
            # Merge condition: next_anc.reference_start <= current.reference_end
            if next_anc.reference_start <= current.reference_end:
                new_end = max(current.reference_end, next_anc.reference_end)
                current.reference_end = new_end
                current.query_end = current.query_start + (new_end - current.reference_start)
                current.length = current.reference_end - current.reference_start
            else:
                merged.append(current)
                current = next_anc
        merged.append(current)
        
    return merged

def resolve_conflicts(anchors: List[Anchor]) -> List[Anchor]:
    """
    Resolves conflicts between overlapping anchors (with different offsets).
    Policy:
    1. Sort anchors by length (descending). Tie-breaker: earliest reference_start.
    2. Greedily pick anchors if they don't overlap with already picked anchors 
       in both reference and query coordinates.
    """
    # Sort by length descending, then reference_start ascending
    sorted_anchors = sorted(anchors, key=lambda a: (-a.length, a.reference_start, a.query_start))
    
    final_anchors = []
    
    for a in sorted_anchors:
        conflict = False
        for f in final_anchors:
            # Check reference overlap
            ref_overlap = (a.reference_start < f.reference_end) and (a.reference_end > f.reference_start)
            # Check query overlap
            query_overlap = (a.query_start < f.query_end) and (a.query_end > f.query_start)
            
            if ref_overlap or query_overlap:
                conflict = True
                break
        
        if not conflict:
            final_anchors.append(a)
            
    # Final sort by reference start
    return sorted(final_anchors, key=lambda a: a.reference_start)

def run_anchor_engine(reference: str, query: str, config: AnchorAlignConfig) -> (List[Anchor], Dict[str, Any]):
    """
    Runs the full anchor engine pipeline.
    Returns the ordered list of final anchors and a diagnostics dictionary.
    """
    candidates = generate_candidates(reference, query, config)
    candidate_count = len(candidates)
    
    merged = merge_anchors(candidates, config)
    merged_count = len(merged)
    
    final_anchors = resolve_conflicts(merged)
    final_count = len(final_anchors)
    
    diagnostics = {
        "candidate_anchor_count": candidate_count,
        "retained_anchor_count": final_count,
        "merged_anchor_count": merged_count,
        "discarded_anchor_count": merged_count - final_count,
        "L_min": config.L_min,
        "merge_threshold": config.anchor_merge_threshold
    }
    
    return final_anchors, diagnostics
