import pytest
from anchoralign.analysis.complexity import (
    compute_theoretical_complexity,
    generate_scaling_curves,
    compute_empirical_complexity,
)
from anchoralign.models.alignment import AlignmentResult
from anchoralign.models.gap import Gap


def test_compute_theoretical_complexity():
    metrics = compute_theoretical_complexity(1000, 1000, band_width=50, homology_ratio=0.9)
    assert metrics.full_dp_cells == 1001 * 1001
    assert metrics.alignx_cells < metrics.full_dp_cells
    assert metrics.cells_saved > 0
    assert metrics.work_saved_pct > 80.0
    assert metrics.theoretical_speedup > 1.0
    assert metrics.full_dp_memory_mb > metrics.alignx_memory_mb


def test_generate_scaling_curves():
    data = generate_scaling_curves(min_len=100, max_len=1000, points=5, band_width=20)
    assert len(data) >= 5
    assert data[0]["length"] == 100
    assert data[-1]["length"] >= 900
    # Quadratic growth check: Full DP cells should grow much faster than AlignX cells
    ratio_first = data[0]["Full DP O(N^2) Cells"] / max(1, data[0]["AlignX Decomposed Cells"])
    ratio_last = data[-1]["Full DP O(N^2) Cells"] / max(1, data[-1]["AlignX Decomposed Cells"])
    assert ratio_last >= ratio_first


def test_compute_empirical_complexity():
    # Gap with 100 cells evaluated
    al = AlignmentResult(
        aligned_reference="ACGT",
        aligned_query="ACGT",
        score=8.0,
        strategy="banded_dp",
        band_width=5,
        boundary_touched=False,
        cells_evaluated=120,
    )
    metrics = compute_empirical_complexity(
        ref_length=500,
        query_length=500,
        actual_gap_alignments=[al],
        anchors=[],
    )
    assert metrics.full_dp_cells == 501 * 501
    assert metrics.alignx_cells == 120
    assert metrics.cells_saved == (501 * 501) - 120
    assert metrics.work_saved_pct > 99.0
