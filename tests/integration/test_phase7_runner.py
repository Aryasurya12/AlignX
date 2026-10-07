import pytest
import os
from experiments.benchmark_generator import BenchmarkGenerator
from experiments.run_phase7 import run_experiment, get_correctness_class
from anchoralign.config import AnchorAlignConfig
from anchoralign.evaluation.baseline import full_sequence_align
from anchoralign.pipeline.orchestrator import run_pipeline

def test_benchmark_generator_deterministic():
    gen1 = BenchmarkGenerator(seed=42)
    gen2 = BenchmarkGenerator(seed=42)
    ds1 = gen1.generate_family_a(100)
    ds2 = gen2.generate_family_a(100)
    assert ds1.reference == ds2.reference
    assert ds1.query == ds2.query

def test_benchmark_generator_length():
    gen = BenchmarkGenerator(seed=42)
    ds = gen.generate_family_a(150)
    assert len(ds.reference) == 150

def test_correctness_class_exact():
    ref = "ACGT" * 10
    query = "ACGT" * 10
    config = AnchorAlignConfig(adaptive_band_enabled=True)
    res = run_pipeline(ref, query, config)
    b_ref, b_query, b_score, _, _ = full_sequence_align(ref, query, config)
    
    c_class = get_correctness_class(ref, query, res, b_score, b_ref, b_query)
    assert c_class == "Exact alignment match"

def test_correctness_class_invalid():
    # Force a dummy result to test invalid reconstruction
    ref = "ACGT"
    query = "ACGT"
    config = AnchorAlignConfig(adaptive_band_enabled=True)
    res = run_pipeline(ref, query, config)
    # Manually mangle
    res.final_alignment.aligned_reference = "AAAA"
    
    b_ref, b_query, b_score, _, _ = full_sequence_align(ref, query, config)
    c_class = get_correctness_class(ref, query, res, b_score, b_ref, b_query)
    assert c_class == "Invalid reconstruction"

def test_smoke_test_runner(tmp_path):
    gen = BenchmarkGenerator(seed=42)
    ds = gen.generate_family_a(100)
    config = AnchorAlignConfig(adaptive_band_enabled=True)
    df = run_experiment([ds], config, "test_run", tmp_path)
    
    assert len(df) == 1
    assert df.iloc[0]['dataset_id'] == "A_1"
    assert df.iloc[0]['family'] == "A_Easy"
    assert df.iloc[0]['correctness'] in ["Exact alignment match", "Equivalent optimal score"]
    assert "speedup" in df.columns
    assert df.iloc[0]['speedup'] > 0
