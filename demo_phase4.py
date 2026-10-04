import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from anchoralign.config import AnchorAlignConfig
from anchoralign.evaluation.datasets import generate_synthetic_case
from anchoralign.pipeline.orchestrator import run_pipeline
from anchoralign.evaluation.baseline import full_sequence_align
from anchoralign.evaluation.metrics import check_correctness, compute_speedup, compute_anchor_coverage

def run_demo():
    print("=" * 60)
    print("PHASE 4 DEMO: AnchorAlign vs Full DP")
    print("=" * 60)
    
    # Generate a synthetic case
    print("\nGenerating medium synthetic case (1000bp, ~90% similarity)...")
    case = generate_synthetic_case("demo_1", length=1000, target_similarity=0.90, seed=123)
    
    config = AnchorAlignConfig(band_width=16, L_min=10)
    
    print("\nRunning Full DP Baseline...")
    b_ref, b_query, b_score, b_runtime, b_muts = full_sequence_align(case.reference, case.query, config)
    print(f"Baseline Runtime:  {b_runtime:.4f} seconds")
    print(f"Baseline Score:    {b_score}")
    print(f"Baseline Mutations:{len(b_muts)}")
    
    print("\nRunning AnchorAlign Adaptive Pipeline...")
    start_time = time.perf_counter()
    res = run_pipeline(case.reference, case.query, config)
    a_runtime = time.perf_counter() - start_time
    
    a_score = res.final_alignment.score
    
    anchor_bases = sum(a.length for a in res.anchors)
    coverage = compute_anchor_coverage(anchor_bases, len(case.reference))
    
    print(f"Adaptive Runtime:  {a_runtime:.4f} seconds")
    print(f"Adaptive Score:    {a_score}")
    print(f"Adaptive Mutations:{len(res.mutations)}")
    
    print("\nPipeline Statistics:")
    print(f"  Anchor Count:      {len(res.anchors)}")
    print(f"  Anchor Coverage:   {coverage*100:.1f}%")
    print(f"  Gap Count:         {len(res.gaps)}")
    
    banded_count = sum(1 for g in res.alignments if g.strategy == 'banded_dp')
    full_count = sum(1 for g in res.alignments if g.strategy != 'banded_dp')
    print(f"  Strategy Dist:     Banded DP: {banded_count}, Full DP: {full_count}")
    
    print("\nComparison Results:")
    speedup = compute_speedup(b_runtime, a_runtime)
    correct = check_correctness(a_score, b_score)
    
    print(f"  Correctness Match: {'YES' if correct else 'NO'}")
    print(f"  Speedup:           {speedup:.2f}x")
    
    print("\nDemo Completed Successfully.")
    
if __name__ == "__main__":
    run_demo()
