from typing import List, Dict, Any
from ..models.mutation import Mutation
from ..config import AnchorAlignConfig

def cluster_mutations(mutations: List[Mutation], config: AnchorAlignConfig) -> List[Dict[str, Any]]:
    """
    Groups nearby mutation events into higher-level compound events.
    Two mutations are clustered if their reference_position difference <= clustering_k.
    Insertion boundaries use the reference_position before the insertion.
    """
    if not mutations:
        return []
        
    clusters = []
    current_cluster = [mutations[0]]
    
    for m in mutations[1:]:
        prev_m = current_cluster[-1]
        
        # Calculate distance based on reference_position
        # Deletion/Substitution spans bases. We should use the end position of prev_m.
        prev_end = prev_m.reference_position + len(prev_m.reference_sequence)
        
        distance = m.reference_position - prev_end
        
        if distance <= config.clustering_k:
            current_cluster.append(m)
        else:
            clusters.append(current_cluster)
            current_cluster = [m]
            
    clusters.append(current_cluster)
    
    compound_events = []
    for cluster in clusters:
        compound_events.append({
            "start_position": cluster[0].reference_position,
            "end_position": cluster[-1].reference_position + len(cluster[-1].reference_sequence),
            "mutation_count": len(cluster),
            "mutations": cluster
        })
        
    return compound_events
