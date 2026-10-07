import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from anchoralign.pipeline.orchestrator import run_pipeline
from anchoralign.config import AnchorAlignConfig
from anchoralign.evaluation.baseline import full_sequence_align
from experiments.benchmark_generator import BenchmarkGenerator

def get_correctness_class(ref, query, res, b_score, b_ref, b_query):
    aln_ref = res.final_alignment.aligned_reference
    aln_query = res.final_alignment.aligned_query
    
    if aln_ref.replace('-', '') != ref or aln_query.replace('-', '') != query:
        return "Invalid reconstruction"
        
    score = res.final_alignment.score
    
    if score > b_score:
        return "Invalid score calculation"
    elif score < b_score:
        return "Valid but non-optimal alignment"
    else:
        if aln_ref == b_ref and aln_query == b_query:
            return "Exact alignment match"
        else:
            return "Equivalent optimal score"

def run_experiment(datasets, config, name, output_dir):
    results = []
    
    for ds in datasets:
        print(f"Running dataset: {ds.id} ({ds.family}) - Ref Length: {len(ds.reference)}")
        
        # Baseline Full DP
        start = time.perf_counter()
        b_ref, b_query, b_score, b_runtime, b_muts = full_sequence_align(ds.reference, ds.query, config)
        baseline_time = time.perf_counter() - start
        
        # AlignX
        start = time.perf_counter()
        res = run_pipeline(ds.reference, ds.query, config)
        alignx_time = time.perf_counter() - start
        
        c_class = get_correctness_class(ds.reference, ds.query, res, b_score, b_ref, b_query)
        
        retries = sum(a.decision_metadata.get('retry_count', 0) for a in res.alignments if a.decision_metadata)
        fallbacks = sum(1 for a in res.alignments if a.strategy == "full_dp_fallback")
        banded_dps = sum(1 for a in res.alignments if a.strategy == "banded_dp")
        
        results.append({
            "dataset_id": ds.id,
            "family": ds.family,
            "ref_length": len(ds.reference),
            "query_length": len(ds.query),
            "baseline_score": b_score,
            "alignx_score": res.final_alignment.score,
            "correctness": c_class,
            "baseline_runtime": baseline_time,
            "alignx_runtime": alignx_time,
            "speedup": baseline_time / max(alignx_time, 1e-9),
            "anchors": len(res.anchors),
            "gaps": len(res.gaps),
            "retries": retries,
            "fallbacks": fallbacks,
            "banded_dps": banded_dps
        })
        
    df = pd.DataFrame(results)
    
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, f"{name}.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved {csv_path}")
    
    return df

def plot_results(df, x_col, y_col, hue, title, output_path):
    plt.figure(figsize=(10, 6))
    for category in df[hue].unique():
        subset = df[df[hue] == category]
        plt.scatter(subset[x_col], subset[y_col], label=category, alpha=0.7)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Phase 7 Benchmark Runner")
    parser.add_argument("--smoke", action="store_true", help="Run a fast smoke test")
    parser.add_argument("--scale", action="store_true", help="Run full scaling experiments")
    args = parser.parse_args()
    
    gen = BenchmarkGenerator(seed=42)
    config = AnchorAlignConfig(adaptive_band_enabled=True, band_safety_margin=5)
    
    out_dir = os.path.join("experiments", "results")
    plot_dir = os.path.join("experiments", "plots")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(plot_dir, exist_ok=True)
    
    if args.smoke:
        print("Running Smoke Test...")
        datasets = [
            gen.generate_family_a(200),
            gen.generate_family_b(200),
            gen.generate_family_c(200)
        ]
        run_experiment(datasets, config, "phase7_smoke", out_dir)
    else:
        print("Running Core Benchmarks...")
        datasets = [
            gen.generate_family_a(500),
            gen.generate_family_b(500),
            gen.generate_family_c(500),
            gen.generate_family_d(500),
            gen.generate_family_e(500)
        ]
        df_core = run_experiment(datasets, config, "phase7_correctness", out_dir)
        
        if args.scale:
            print("Running Scaling Benchmarks...")
            scale_ds = gen.generate_family_f([500, 1000, 2000, 4000, 8000])
            df_scale = run_experiment(scale_ds, config, "phase7_scaling", out_dir)
            
            plot_results(df_scale, "ref_length", "alignx_runtime", "family", "AlignX Runtime vs Length", os.path.join(plot_dir, "phase7_scaling_runtime.png"))
            plot_results(df_scale, "ref_length", "speedup", "family", "AlignX Speedup vs Length", os.path.join(plot_dir, "phase7_scaling_speedup.png"))
