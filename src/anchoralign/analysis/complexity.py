"""Algorithm Complexity Analysis and Big-O Computation Module for AlignX.

Provides theoretical and empirical asymptotic metrics comparing:
- Classical Full DP: O(N * M) time, O(N * M) space
- Global Banded DP: O(N * W) time, O(N * W) space
- AlignX Decomposed Alignment: O(N + Sum(Gap_i * W_i)) time, O(max(Gap_i * W_i)) space
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional


@dataclass
class ComplexityMetrics:
    """Detailed complexity comparison metrics for an alignment."""
    ref_length: int
    query_length: int
    full_dp_cells: int
    banded_dp_cells: int
    alignx_cells: int
    cells_saved: int
    work_saved_pct: float
    theoretical_speedup: float
    full_dp_memory_mb: float
    alignx_memory_mb: float
    memory_savings_factor: float


def compute_theoretical_complexity(
    n: int,
    m: int,
    band_width: int = 50,
    homology_ratio: float = 0.95
) -> ComplexityMetrics:
    """
    Compute theoretical asymptotic complexity metrics for given sequence lengths.

    Args:
        n: Reference length
        m: Query length
        band_width: Band parameter W
        homology_ratio: Fraction of sequence covered by exact anchors (0.0 to 1.0)
    """
    full_dp_cells = (n + 1) * (m + 1)

    # Global banded DP evaluates ~(2W + 1) * min(n, m) cells
    w = max(1, min(band_width, max(n, m)))
    banded_cells = min(full_dp_cells, (2 * w + 1) * min(n, m))

    # AlignX: exact anchors take O(1) DP cells (0 matrix cells).
    # Gaps represent (1 - homology_ratio) of the sequence.
    gap_residues = max(1, int(max(n, m) * (1.0 - homology_ratio)))
    # Gaps are partitioned into smaller subproblems.
    # Suppose average gap is distributed across k chunks (e.g. 5 chunks)
    k_gaps = max(1, int(gap_residues / 30))
    avg_gap_len = max(1, gap_residues // k_gaps)
    gap_band = min(w, avg_gap_len)
    alignx_gap_cells = k_gaps * min((avg_gap_len + 1) ** 2, (2 * gap_band + 1) * (avg_gap_len + 1))
    alignx_cells = min(full_dp_cells, alignx_gap_cells)

    cells_saved = full_dp_cells - alignx_cells
    work_saved_pct = (cells_saved / full_dp_cells * 100.0) if full_dp_cells > 0 else 0.0
    theoretical_speedup = (full_dp_cells / max(1, alignx_cells))

    # Memory: 8 bytes per matrix cell (float/int64)
    BYTES_PER_CELL = 8
    full_dp_memory_mb = (full_dp_cells * BYTES_PER_CELL) / (1024 * 1024)
    # AlignX only holds the largest active gap matrix in memory at one time
    max_gap_cells = (2 * gap_band + 1) * (avg_gap_len + 1)
    alignx_memory_mb = (max_gap_cells * BYTES_PER_CELL) / (1024 * 1024)
    memory_savings_factor = (full_dp_memory_mb / max(0.0001, alignx_memory_mb))

    return ComplexityMetrics(
        ref_length=n,
        query_length=m,
        full_dp_cells=full_dp_cells,
        banded_dp_cells=banded_cells,
        alignx_cells=alignx_cells,
        cells_saved=cells_saved,
        work_saved_pct=round(work_saved_pct, 2),
        theoretical_speedup=round(theoretical_speedup, 2),
        full_dp_memory_mb=round(full_dp_memory_mb, 4),
        alignx_memory_mb=round(alignx_memory_mb, 4),
        memory_savings_factor=round(memory_savings_factor, 1),
    )


def generate_scaling_curves(
    min_len: int = 100,
    max_len: int = 10000,
    points: int = 25,
    band_width: int = 50,
    homology_ratio: float = 0.90
) -> List[Dict[str, Any]]:
    """
    Generate Big-O scaling dataset across varying sequence lengths for plotting.
    """
    step = max(50, (max_len - min_len) // (points - 1))
    data: List[Dict[str, Any]] = []

    for n in range(min_len, max_len + 1, step):
        metrics = compute_theoretical_complexity(n, n, band_width=band_width, homology_ratio=homology_ratio)
        data.append({
            "length": n,
            "Full DP O(N^2) Cells": metrics.full_dp_cells,
            "Banded DP O(N*W) Cells": metrics.banded_dp_cells,
            "AlignX Decomposed Cells": metrics.alignx_cells,
            "Cells Saved": metrics.cells_saved,
            "Work Saved (%)": metrics.work_saved_pct,
            "Speedup (x)": metrics.theoretical_speedup,
            "Full DP Memory (MB)": metrics.full_dp_memory_mb,
            "AlignX Memory (MB)": metrics.alignx_memory_mb,
        })

    return data


def compute_empirical_complexity(
    ref_length: int,
    query_length: int,
    actual_gap_alignments: List[Any],
    anchors: List[Any],
) -> ComplexityMetrics:
    """
    Calculate exact empirical cell counts from actual pipeline execution results.
    """
    full_dp_cells = (ref_length + 1) * (query_length + 1)

    # Sum cells actually evaluated in all gaps
    alignx_cells = 0
    for al in actual_gap_alignments:
        cells = getattr(al, "cells_evaluated", None)
        if cells is not None and cells > 0:
            alignx_cells += cells
        else:
            # Fallback estimation if cell counter not present
            w = getattr(al, "band_width", 0)
            ref_sub = len(getattr(al, "aligned_reference", "").replace("-", ""))
            qry_sub = len(getattr(al, "aligned_query", "").replace("-", ""))
            if al.strategy == "banded_dp" and w > 0:
                alignx_cells += min((ref_sub + 1) * (qry_sub + 1), (2 * w + 1) * (ref_sub + 1))
            else:
                alignx_cells += (ref_sub + 1) * (qry_sub + 1)

    # Banded global estimate (assuming global band of 100)
    w_global = 100
    banded_cells = min(full_dp_cells, (2 * w_global + 1) * min(ref_length, query_length))

    cells_saved = max(0, full_dp_cells - alignx_cells)
    work_saved_pct = (cells_saved / full_dp_cells * 100.0) if full_dp_cells > 0 else 0.0
    theoretical_speedup = (full_dp_cells / max(1, alignx_cells))

    BYTES_PER_CELL = 8
    full_dp_memory_mb = (full_dp_cells * BYTES_PER_CELL) / (1024 * 1024)
    # Max single gap allocation
    max_gap_cells = max([getattr(al, "cells_evaluated", 1) for al in actual_gap_alignments], default=1)
    alignx_memory_mb = (max_gap_cells * BYTES_PER_CELL) / (1024 * 1024)
    memory_savings_factor = (full_dp_memory_mb / max(0.0001, alignx_memory_mb))

    return ComplexityMetrics(
        ref_length=ref_length,
        query_length=query_length,
        full_dp_cells=full_dp_cells,
        banded_dp_cells=banded_cells,
        alignx_cells=alignx_cells,
        cells_saved=cells_saved,
        work_saved_pct=round(work_saved_pct, 2),
        theoretical_speedup=round(theoretical_speedup, 2),
        full_dp_memory_mb=round(full_dp_memory_mb, 4),
        alignx_memory_mb=round(alignx_memory_mb, 4),
        memory_savings_factor=round(memory_savings_factor, 1),
    )
