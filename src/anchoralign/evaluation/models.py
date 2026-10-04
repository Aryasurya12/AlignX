from dataclasses import dataclass
from typing import List, Dict, Optional, Any

@dataclass
class GroundTruthCase:
    case_id: str
    reference: str
    query: str
    expected_mutations: List[Dict[str, Any]]
    expected_mutation_count: int
    target_similarity: float
    actual_similarity: float
    generation_parameters: Dict[str, Any]

@dataclass
class ExperimentResult:
    case_id: str
    sequence_length: int
    reference_length: int
    query_length: int
    target_similarity: float
    actual_similarity: float
    
    anchor_count: int
    anchor_bases: int
    anchor_coverage: float
    
    gap_count: int
    gap_bases: int
    
    banded_gap_count: int
    full_dp_gap_count: int
    
    adaptive_runtime: float
    baseline_runtime: float
    
    adaptive_memory: float
    baseline_memory: float
    
    adaptive_score: int
    baseline_score: int
    
    mutation_count_adaptive: int
    mutation_count_baseline: int
    
    mutation_correct: bool
    
    boundary_warning_count: int
    
    clustering_k: int
    band_width: int
    l_min: int
    
    speedup: float
    
    adaptive_work_proxy: int
    baseline_work_proxy: int
