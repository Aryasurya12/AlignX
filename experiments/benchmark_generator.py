import random
import json
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict, Any

@dataclass
class BenchmarkDataset:
    id: str
    family: str
    reference: str
    query: str
    seed: int
    parameters: Dict[str, Any]
    ground_truth_events: List[Dict[str, Any]]

class BenchmarkGenerator:
    def __init__(self, seed: int = 42):
        self.seed = seed
        self.rng = random.Random(seed)
        self.bases = ['A', 'C', 'G', 'T']
        
    def generate_random_sequence(self, length: int) -> str:
        return ''.join(self.rng.choices(self.bases, k=length))
        
    def generate_repetitive_sequence(self, length: int, motif: str) -> str:
        repeats = (length // len(motif)) + 1
        return (motif * repeats)[:length]

    def mutate_sequence(self, ref: str, sub_rate: float, ins_rate: float, del_rate: float, max_indel_len: int = 5) -> Tuple[str, List[Dict]]:
        query = []
        events = []
        i = 0
        ref_len = len(ref)
        
        while i < ref_len:
            r = self.rng.random()
            
            # Deletion
            if r < del_rate:
                del_len = self.rng.randint(1, max_indel_len)
                del_len = min(del_len, ref_len - i)
                events.append({
                    "type": "deletion",
                    "ref_start": i,
                    "ref_end": i + del_len,
                    "query_start": len(''.join(query)),
                    "query_end": len(''.join(query)),
                    "length": del_len
                })
                i += del_len
                continue
                
            # Insertion
            elif r < del_rate + ins_rate:
                ins_len = self.rng.randint(1, max_indel_len)
                inserted_bases = self.generate_random_sequence(ins_len)
                events.append({
                    "type": "insertion",
                    "ref_start": i,
                    "ref_end": i,
                    "query_start": len(''.join(query)),
                    "query_end": len(''.join(query)) + ins_len,
                    "length": ins_len,
                    "bases": inserted_bases
                })
                query.append(inserted_bases)
                # Note: does not consume reference base
                
            # Substitution
            elif r < del_rate + ins_rate + sub_rate:
                base = ref[i]
                choices = [b for b in self.bases if b != base]
                mutated = self.rng.choice(choices)
                events.append({
                    "type": "substitution",
                    "ref_start": i,
                    "ref_end": i + 1,
                    "query_start": len(''.join(query)),
                    "query_end": len(''.join(query)) + 1,
                    "ref_base": base,
                    "query_base": mutated
                })
                query.append(mutated)
                i += 1
                
            # Match
            else:
                query.append(ref[i])
                i += 1
                
        return ''.join(query), events

    def generate_family_a(self, length: int = 1000) -> BenchmarkDataset:
        # Easy: Sparse substitutions
        ref = self.generate_random_sequence(length)
        query, events = self.mutate_sequence(ref, sub_rate=0.01, ins_rate=0.0, del_rate=0.0)
        return BenchmarkDataset("A_1", "A_Easy", ref, query, self.seed, {"sub_rate": 0.01}, events)

    def generate_family_b(self, length: int = 1000) -> BenchmarkDataset:
        # Indel-heavy: long indels
        ref = self.generate_random_sequence(length)
        query, events = self.mutate_sequence(ref, sub_rate=0.0, ins_rate=0.02, del_rate=0.02, max_indel_len=10)
        return BenchmarkDataset("B_1", "B_Indel", ref, query, self.seed, {"ins_rate": 0.02, "del_rate": 0.02}, events)

    def generate_family_c(self, length: int = 1000) -> BenchmarkDataset:
        # Divergent: high mutation rate
        ref = self.generate_random_sequence(length)
        query, events = self.mutate_sequence(ref, sub_rate=0.1, ins_rate=0.05, del_rate=0.05, max_indel_len=3)
        return BenchmarkDataset("C_1", "C_Divergent", ref, query, self.seed, {"sub_rate": 0.1, "ins_rate": 0.05, "del_rate": 0.05}, events)
        
    def generate_family_d(self, length: int = 1000) -> BenchmarkDataset:
        # Repetitive
        ref = self.generate_repetitive_sequence(length, "ATGCATGC")
        query, events = self.mutate_sequence(ref, sub_rate=0.02, ins_rate=0.01, del_rate=0.01)
        return BenchmarkDataset("D_1", "D_Repetitive", ref, query, self.seed, {"motif": "ATGCATGC"}, events)
        
    def generate_family_e(self, length: int = 1000) -> BenchmarkDataset:
        # Localized hotspot
        ref = self.generate_random_sequence(length)
        hotspot_start = length // 2
        hotspot_end = hotspot_start + 100
        
        q1 = ref[:hotspot_start]
        q2, ev2 = self.mutate_sequence(ref[hotspot_start:hotspot_end], sub_rate=0.2, ins_rate=0.1, del_rate=0.1)
        q3 = ref[hotspot_end:]
        
        # Adjust coordinates for ev2
        for e in ev2:
            e['ref_start'] += hotspot_start
            e['ref_end'] += hotspot_start
            e['query_start'] += hotspot_start
            e['query_end'] += hotspot_start
            
        return BenchmarkDataset("E_1", "E_Localized", ref, q1 + q2 + q3, self.seed, {"hotspot": f"{hotspot_start}-{hotspot_end}"}, ev2)

    def generate_family_f(self, lengths: List[int]) -> List[BenchmarkDataset]:
        # Scaling
        datasets = []
        for l in lengths:
            ref = self.generate_random_sequence(l)
            query, events = self.mutate_sequence(ref, sub_rate=0.02, ins_rate=0.01, del_rate=0.01)
            datasets.append(BenchmarkDataset(f"F_{l}", "F_Scaling", ref, query, self.seed, {"length": l}, events))
        return datasets
