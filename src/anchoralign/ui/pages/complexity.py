import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from anchoralign.analysis.complexity import (
    compute_theoretical_complexity,
    generate_scaling_curves,
    compute_empirical_complexity,
)


def render():
    st.header("Algorithm Complexity & Big-O Visualizer")
    st.markdown(
        "Analyze the asymptotic and empirical time/space complexity differences between "
        "classical Needleman-Wunsch Full DP, Global Banded DP, and AlignX Adaptive Decomposition."
    )

    # 1. Theoretical Big-O Overview Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background-color: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; border-radius: 8px; padding: 16px;">
            <h4 style="margin: 0; color: #ef4444;">Needleman-Wunsch</h4>
            <p style="font-size: 1.3rem; font-weight: bold; margin: 8px 0;">O(N &times; M)</p>
            <p style="margin: 0; font-size: 0.85rem; color: #888;">Quadratic time & space. Evaluates every unreachable matrix cell regardless of homology.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background-color: rgba(245, 158, 11, 0.1); border: 1px solid #f59e0b; border-radius: 8px; padding: 16px;">
            <h4 style="margin: 0; color: #f59e0b;">Global Banded DP</h4>
            <p style="font-size: 1.3rem; font-weight: bold; margin: 8px 0;">O(N &times; W)</p>
            <p style="margin: 0; font-size: 0.85rem; color: #888;">Restricts DP to fixed diagonal band W. Susceptible to boundary clipping on large indels.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background-color: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: 8px; padding: 16px;">
            <h4 style="margin: 0; color: #10b981;">AlignX Decomposed</h4>
            <p style="font-size: 1.3rem; font-weight: bold; margin: 8px 0;">O(N + &sum; g<sub>i</sub> &times; W<sub>i</sub>)</p>
            <p style="margin: 0; font-size: 0.85rem; color: #888;">Linear exact anchoring + localized adaptive bands. Near-linear O(N) at high homology.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # 2. Empirical Execution Work-Saved Metrics (if active alignment session exists)
    st.subheader("Empirical Alignment Session Metrics")
    res = st.session_state.pipeline_result

    if res:
        emp = compute_empirical_complexity(
            ref_length=res.reference_length,
            query_length=res.query_length,
            actual_gap_alignments=res.alignments,
            anchors=res.anchors,
        )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Full DP Matrix Cells", f"{emp.full_dp_cells:,}")
        m2.metric("AlignX DP Cells Evaluated", f"{emp.alignx_cells:,}")
        m3.metric("Cells Skipped (Work Saved)", f"{emp.cells_saved:,}", delta=f"{emp.work_saved_pct}%")
        m4.metric("Theoretical Speedup", f"{emp.theoretical_speedup:.1f}x")

        # Visualizations of work saved
        vcol1, vcol2 = st.columns(2)
        with vcol1:
            # Donut chart: Evaluated vs Skipped
            fig, ax = plt.subplots(figsize=(5, 4))
            labels = ['Cells Evaluated', 'Cells Skipped (Saved)']
            sizes = [max(1, emp.alignx_cells), max(0, emp.cells_saved)]
            colors = ['#3b82f6', '#10b981']
            explode = (0.05, 0)
            
            wedges, texts, autotexts = ax.pie(
                sizes,
                explode=explode,
                labels=labels,
                autopct='%1.1f%%',
                startangle=140,
                colors=colors,
                textprops=dict(color="white"),
                wedgeprops=dict(width=0.4, edgecolor='none')
            )
            for at in autotexts:
                at.set_fontsize(11)
                at.set_weight('bold')
            ax.set_title("Matrix Evaluation Budget", color="white", fontsize=12)
            fig.patch.set_facecolor('#1e1e2e')
            ax.set_facecolor('#1e1e2e')
            st.pyplot(fig)
            plt.close(fig)

        with vcol2:
            # Bar chart: Cells evaluated comparison
            fig, ax = plt.subplots(figsize=(5, 4))
            strategies = ['Full DP (O(N*M))', 'Global Banded (W=100)', 'AlignX (Decomposed)']
            cell_counts = [emp.full_dp_cells, emp.banded_dp_cells, emp.alignx_cells]
            bar_colors = ['#ef4444', '#f59e0b', '#10b981']

            bars = ax.bar(strategies, cell_counts, color=bar_colors, width=0.5)
            ax.set_ylabel("Cells Evaluated (Log Scale)", color="white")
            ax.set_yscale('log')
            ax.tick_params(colors="white", which="both")
            ax.set_title("DP Cell Count Comparison", color="white", fontsize=12)
            fig.patch.set_facecolor('#1e1e2e')
            ax.set_facecolor('#1e1e2e')
            for spine in ax.spines.values():
                spine.set_color('#444')
            st.pyplot(fig)
            plt.close(fig)

        # Gap breakdown table
        if res.gaps and res.alignments:
            with st.expander("Per-Gap Cell Evaluation Breakdown"):
                gap_data = []
                for idx, (g, a) in enumerate(zip(res.gaps, res.alignments)):
                    g_cells = getattr(a, "cells_evaluated", 0)
                    g_full = (g.reference_length + 1) * (g.query_length + 1)
                    saved = max(0, g_full - g_cells)
                    gap_data.append({
                        "Gap #": idx + 1,
                        "Strategy": a.strategy,
                        "Band Width": a.band_width,
                        "Ref Len": g.reference_length,
                        "Query Len": g.query_length,
                        "DP Cells Evaluated": g_cells,
                        "Full DP Equivalent": g_full,
                        "Cells Saved": saved,
                    })
                st.dataframe(pd.DataFrame(gap_data), width='stretch')

    else:
        st.info("Run an alignment in **Sequence Alignment** to see empirical cell savings for your sequence!")

    st.divider()

    # 3. Interactive Asymptotic Scaling Simulator
    st.subheader("Interactive Asymptotic Scaling Simulator")
    st.markdown("Simulate how algorithms scale as sequence length increases from hundreds of base pairs to tens of thousands.")

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        sim_max_len = st.slider("Maximum Sequence Length (bp)", min_value=1000, max_value=50000, value=10000, step=1000)
    with sc2:
        sim_band_w = st.slider("Band Width (W)", min_value=10, max_value=200, value=50, step=10)
    with sc3:
        sim_homology = st.slider("Sequence Homology (%)", min_value=50, max_value=99, value=90, step=5)

    use_log_scale = st.checkbox("Logarithmic scale for cell count", value=True)

    curve_data = generate_scaling_curves(
        min_len=200,
        max_len=sim_max_len,
        points=25,
        band_width=sim_band_w,
        homology_ratio=sim_homology / 100.0,
    )
    df_curves = pd.DataFrame(curve_data)

    # Plot Scaling Curves
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    # Curve 1: Time / Cell Count
    ax1.plot(df_curves["length"], df_curves["Full DP O(N^2) Cells"], label="Full DP O(N²)", color="#ef4444", linewidth=2.5)
    ax1.plot(df_curves["length"], df_curves["Banded DP O(N*W) Cells"], label="Global Banded O(N×W)", color="#f59e0b", linewidth=2)
    ax1.plot(df_curves["length"], df_curves["AlignX Decomposed Cells"], label="AlignX Decomposed", color="#10b981", linewidth=2.5)
    ax1.set_xlabel("Sequence Length N (bp)", color="white")
    ax1.set_ylabel("Matrix Cells Evaluated" + (" (log)" if use_log_scale else ""), color="white")
    if use_log_scale:
        ax1.set_yscale("log")
    ax1.set_title("Time Complexity (DP Operations)", color="white", fontsize=11)
    ax1.tick_params(colors="white")
    ax1.legend(facecolor='#262626', edgecolor='none', labelcolor='white')
    ax1.grid(True, linestyle="--", alpha=0.3)
    for spine in ax1.spines.values():
        spine.set_color('#444')

    # Curve 2: Memory Footprint (MB)
    ax2.plot(df_curves["length"], df_curves["Full DP Memory (MB)"], label="Full DP Memory", color="#ef4444", linewidth=2.5)
    ax2.plot(df_curves["length"], df_curves["AlignX Memory (MB)"], label="AlignX Peak Memory", color="#10b981", linewidth=2.5)
    ax2.set_xlabel("Sequence Length N (bp)", color="white")
    ax2.set_ylabel("Memory Consumption (MB)", color="white")
    ax2.set_title("Space Complexity (Peak RAM)", color="white", fontsize=11)
    ax2.tick_params(colors="white")
    ax2.legend(facecolor='#262626', edgecolor='none', labelcolor='white')
    ax2.grid(True, linestyle="--", alpha=0.3)
    for spine in ax2.spines.values():
        spine.set_color('#444')

    fig.patch.set_facecolor('#1e1e2e')
    ax1.set_facecolor('#1e1e2e')
    ax2.set_facecolor('#1e1e2e')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    with st.expander("View Simulated Scaling Data Table"):
        st.dataframe(df_curves, width='stretch')
