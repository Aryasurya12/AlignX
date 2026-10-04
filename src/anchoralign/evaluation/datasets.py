import random
from typing import List, Dict, Any
from .models import GroundTruthCase

def generate_synthetic_case(
    case_id: str,
    length: int,
    target_similarity: float,
    seed: int = 42,
    sub_prop: float = 0.6,
    ins_prop: float = 0.2,
    del_prop: float = 0.2
) -> GroundTruthCase:
    random.seed(seed)
    bases = ['A', 'C', 'G', 'T']
    
    # Generate random reference
    reference = ''.join(random.choice(bases) for _ in range(length))
    
    num_mutations = int(length * (1.0 - target_similarity))
    
    # Simple probability distribution
    # Sub: sub_prop, Ins: ins_prop, Del: del_prop
    total_prop = sub_prop + ins_prop + del_prop
    sub_p = sub_prop / total_prop
    ins_p = ins_prop / total_prop
    
    query_list = list(reference)
    mutations_expected = []
    
    # Apply mutations from right to left to avoid coordinate shifting issues during generation
    mutation_indices = sorted(random.sample(range(length), min(num_mutations, length)), reverse=True)
    
    for idx in mutation_indices:
        rand_val = random.random()
        orig_base = query_list[idx]
        if rand_val < sub_p:
            # Substitution
            new_base = random.choice([b for b in bases if b != orig_base])
            query_list[idx] = new_base
            mutations_expected.append({"type": "SUBSTITUTION", "ref_pos": idx, "ref_seq": orig_base, "query_seq": new_base})
        elif rand_val < sub_p + ins_p:
            # Insertion
            new_base = random.choice(bases)
            query_list.insert(idx, new_base)
            mutations_expected.append({"type": "INSERTION", "ref_pos": idx, "ref_seq": "", "query_seq": new_base})
        else:
            # Deletion
            del query_list[idx]
            mutations_expected.append({"type": "DELETION", "ref_pos": idx, "ref_seq": orig_base, "query_seq": ""})
            
    query = ''.join(query_list)
    actual_similarity = 1.0 - (len(mutations_expected) / length) if length > 0 else 1.0
    
    # Sort mutations left to right for easier comparison
    mutations_expected.sort(key=lambda x: x["ref_pos"])
    
    return GroundTruthCase(
        case_id=case_id,
        reference=reference,
        query=query,
        expected_mutations=mutations_expected,
        expected_mutation_count=len(mutations_expected),
        target_similarity=target_similarity,
        actual_similarity=actual_similarity,
        generation_parameters={
            "seed": seed,
            "length": length,
            "sub_prop": sub_prop,
            "ins_prop": ins_prop,
            "del_prop": del_prop
        }
    )
