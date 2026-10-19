import pytest
import time
from anchoralign.pipeline.timing import StageTimer, track_pipeline_resources, timed
from anchoralign.pipeline.orchestrator import run_pipeline
from anchoralign.config import AnchorAlignConfig


def test_stage_timer():
    timings = {}
    with StageTimer("test_stage", timings):
        time.sleep(0.005)
    assert "test_stage" in timings
    assert timings["test_stage"] >= 0.004


def test_track_pipeline_resources():
    with track_pipeline_resources() as (timings, memory_stats):
        # allocate some memory
        arr = [i for i in range(100000)]
        time.sleep(0.002)
    assert "total" in timings
    assert timings["total"] > 0
    assert "peak_kb" in memory_stats
    assert memory_stats["peak_kb"] > 0


def test_orchestrator_timings_and_memory():
    cfg = AnchorAlignConfig(L_min=5)
    res = run_pipeline("ATGCGATCGATCGATC", "ATGCGATCTATCGATC", cfg)
    assert "preprocessing" in res.timings
    assert "anchor_discovery" in res.timings
    assert "gap_alignment" in res.timings
    assert "total" in res.timings
    assert res.memory_peak_kb >= 0.0
