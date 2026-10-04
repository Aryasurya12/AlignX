from typing import List, Dict, Any
from ..models.alignment import AlignmentResult
from ..models.mutation import Mutation
from ..config import AnchorAlignConfig
from .mutation_detector import detect_mutations_engine
from .clustering import cluster_mutations

def detect_mutations(alignment: AlignmentResult) -> List[Mutation]:
    return detect_mutations_engine(alignment.aligned_reference, alignment.aligned_query)
    
def get_compound_events(mutations: List[Mutation], config: AnchorAlignConfig) -> List[Dict[str, Any]]:
    return cluster_mutations(mutations, config)
