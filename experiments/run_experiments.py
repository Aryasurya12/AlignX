import os
import sys
import time
import csv
import json
import argparse
from typing import List, Dict

# Add src to python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from anchoralign.config import AnchorAlignConfig
from anchoralign.pipeline.orchestrator import run_pipeline
from anchoralign.evaluation.baseline import full_sequence_align
from anchoralign.evaluation.datasets import generate_synthetic_case
from anchoralign.evaluation.metrics import check_correctness, compute_speedup, compute_anchor_coverage
from anchoralign.evaluation.models import ExperimentResult

RESULTS_DIR = os.path.join(os.path.dirname(__file__), 'results')
CONFIGS_DIR = os.path.join(os.path.dirname(__file__), 'configs')

def setup_dirs():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(CONFIGS_DIR, exist_ok=True)

def save_csv(results: List[ExperimentResult], filename: str):
    if not results:
        return
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].__dict__.keys())
        writer.writeheader()
        for r in results:
            writer.writerow(r.__dict__)
    print(f"Saved {path}")

def save_config(config_dict: dict, filename: str):
    path = os.path.join(CONFIGS_DIR, filename)
    with open(path, 'w') as f:
        json.dump(config_dict, f, indent=2)

def run_single_case(case, config: AnchorAlignConfig) -> ExperimentResult:
    # Baseline
    b_ref, b_query, b_score, b_runtime, b_muts = full_sequence_align(case.reference, case.query, config)
    
    # Adaptive
    start_time = time.perf_counter()
    try:
        res = run_pipeline(case.reference, case.query, config)
    except Exception as e:
        print(f"Pipeline failed on {case.case_id}: {e}")
        return None
    end_time = time.perf_counter()
    a_runtime = end_time - start_time
    
    # Extract Work Proxies
    a_work = 0
    banded_count = 0
    full_dp_count = 0
    for gap, align in zip(res.gaps, res.alignments):
        ref_len = gap.reference_end - gap.reference_start
        query_len = gap.query_end - gap.query_start
        if align.strategy == "banded_dp":
            banded_count += 1
            a_work += (ref_len + query_len) * config.band_width
        else:
            full_dp_count += 1
            a_work += ref_len * query_len
            
    b_work = len(case.reference) * len(case.query)
    
    anchor_bases = sum(a.length for a in res.anchors)
    gap_bases = sum((g.reference_end - g.reference_start) for g in res.gaps)
    
    is_correct = check_correctness(res.final_alignment.score, b_score)
    speedup = compute_speedup(b_runtime, a_runtime)
    coverage = compute_anchor_coverage(anchor_bases, len(case.reference))
    
    return ExperimentResult(
        case_id=case.case_id,
        sequence_length=len(case.reference),
        reference_length=len(case.reference),
        query_length=len(case.query),
        target_similarity=case.target_similarity,
        actual_similarity=case.actual_similarity,
        anchor_count=len(res.anchors),
        anchor_bases=anchor_bases,
        anchor_coverage=coverage,
        gap_count=len(res.gaps),
        gap_bases=gap_bases,
        banded_gap_count=banded_count,
        full_dp_gap_count=full_dp_count,
        adaptive_runtime=a_runtime,
        baseline_runtime=b_runtime,
        adaptive_memory=0.0, # Not implemented yet
        baseline_memory=0.0, # Not implemented yet
        adaptive_score=res.final_alignment.score,
        baseline_score=b_score,
        mutation_count_adaptive=len(res.mutations),
        mutation_count_baseline=len(b_muts),
        mutation_correct=is_correct,
        boundary_warning_count=len(res.warnings),
        clustering_k=config.clustering_k,
        band_width=config.band_width,
        l_min=config.L_min,
        speedup=speedup,
        adaptive_work_proxy=a_work,
        baseline_work_proxy=b_work
    )

def run_similarity_sweep():
    print("Running Similarity Sweep...")
    results = []
    similarities = [0.99, 0.95, 0.90, 0.85, 0.80]
    config = AnchorAlignConfig()
    
    for sim in similarities:
        for seed in range(3): # 3 repetitions
            case = generate_synthetic_case(f"sim_{sim}_{seed}", 500, sim, seed=seed)
            res = run_single_case(case, config)
            if res: results.append(res)
            
    save_csv(results, 'similarity_results.csv')
    save_config({'experiment': 'similarity', 'similarities': similarities, 'reps': 3, 'length': 500}, 'sim_config.json')

def run_bandwidth_sweep():
    print("Running Bandwidth Sweep...")
    results = []
    bandwidths = [0, 1, 2, 4, 8, 16, 32]
    
    for bw in bandwidths:
        config = AnchorAlignConfig(band_width=bw)
        case = generate_synthetic_case(f"bw_{bw}", 500, 0.90, seed=42)
        res = run_single_case(case, config)
        if res: results.append(res)
        
    save_csv(results, 'band_width_results.csv')
    
def run_lmin_sweep():
    print("Running L_min Sweep...")
    results = []
    lmins = [3, 5, 8, 10, 15, 20]
    
    for lmin in lmins:
        config = AnchorAlignConfig(L_min=lmin)
        case = generate_synthetic_case(f"lmin_{lmin}", 500, 0.90, seed=42)
        res = run_single_case(case, config)
        if res: results.append(res)
        
    save_csv(results, 'lmin_results.csv')

def run_clustering_sweep():
    print("Running Clustering Sweep...")
    results = []
    ks = [0, 1, 2, 3, 5, 10]
    
    for k in ks:
        config = AnchorAlignConfig(clustering_k=k)
        case = generate_synthetic_case(f"k_{k}", 500, 0.90, seed=42)
        res = run_single_case(case, config)
        if res: results.append(res)
        
    save_csv(results, 'clustering_results.csv')

def run_scaling():
    print("Running Scaling Experiment...")
    results = []
    lengths = [500, 1000, 2000, 5000]
    config = AnchorAlignConfig()
    
    for length in lengths:
        case = generate_synthetic_case(f"len_{length}", length, 0.95, seed=42)
        res = run_single_case(case, config)
        if res: results.append(res)
        
    save_csv(results, 'scaling_results.csv')

def run_anchor_coverage():
    print("Running Anchor Coverage Sweep...")
    # Generate cases that naturally have different coverage
    results = []
    similarities = [0.99, 0.90, 0.80]
    lmins = [5, 10, 15]
    for sim in similarities:
        for lmin in lmins:
            config = AnchorAlignConfig(L_min=lmin)
            case = generate_synthetic_case(f"cov_{sim}_{lmin}", 1000, sim, seed=42)
            res = run_single_case(case, config)
            if res: results.append(res)
            
    save_csv(results, 'anchor_coverage_results.csv')

def main():
    setup_dirs()
    run_similarity_sweep()
    run_bandwidth_sweep()
    run_lmin_sweep()
    run_clustering_sweep()
    run_scaling()
    run_anchor_coverage()
    print("All experiments completed.")

if __name__ == "__main__":
    main()
