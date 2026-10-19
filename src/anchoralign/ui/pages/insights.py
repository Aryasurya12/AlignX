import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def render():
    st.header("Explainable Algorithm Decision Inspector")
    if not st.session_state.pipeline_result:
        st.info("Run an alignment in **Sequence Alignment** to inspect algorithmic decisions, timings, and memory profiling.")
        return

    res = st.session_state.pipeline_result
    
    # 1. Pipeline Timing & Resource Instrumentation
    st.subheader("Pipeline Instrumentation & Resource Profile")
    timings = getattr(res, 'timings', {}) or {}
    peak_kb = getattr(res, 'memory_peak_kb', 0.0)
    curr_kb = getattr(res, 'memory_current_kb', 0.0)

    rc1, rc2, rc3 = st.columns(3)
    total_time = timings.get("total", st.session_state.runtimes.get('pipeline', 0.0))
    rc1.metric("Total Execution Time", f"{total_time * 1000:.2f} ms")
    rc2.metric("Peak Memory (tracemalloc)", f"{peak_kb:.1f} KB" if peak_kb < 1024 else f"{peak_kb / 1024:.2f} MB")
    rc3.metric("Current Memory Footprint", f"{curr_kb:.1f} KB")

    if timings:
        stage_items = [(k, v) for k, v in timings.items() if k != "total"]
        if stage_items:
            t_col1, t_col2 = st.columns([1, 1])
            with t_col1:
                # Stage timing table
                stage_df = pd.DataFrame([
                    {
                        "Pipeline Stage": k.replace("_", " ").title(),
                        "Duration (ms)": round(v * 1000, 3),
                        "% of Total": round((v / max(0.0001, total_time)) * 100, 1),
                    }
                    for k, v in stage_items
                ])
                st.dataframe(stage_df, use_container_width=True)

            with t_col2:
                # Horizontal bar chart for stage timings
                fig, ax = plt.subplots(figsize=(5, 3))
                stages = [k.replace("_", " ").title() for k, v in reversed(stage_items)]
                durations = [v * 1000 for k, v in reversed(stage_items)]
                bars = ax.barh(stages, durations, color="#3b82f6", height=0.6)
                ax.set_xlabel("Time (ms)", color="white")
                ax.set_title("Stage Duration Breakdown", color="white", fontsize=11)
                ax.tick_params(colors="white")
                fig.patch.set_facecolor('#1e1e2e')
                ax.set_facecolor('#1e1e2e')
                for spine in ax.spines.values():
                    spine.set_color('#444')
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

    st.divider()

    # 2. Gap Algorithm Decisions
    st.subheader("Gap Algorithm Decisions & Decision Traces")
    if not res.gaps:
        st.info("No gaps to inspect (sequences were identical or completely covered by exact anchors).")
    else:
        for i, (gap, align) in enumerate(zip(res.gaps, res.alignments)):
            with st.expander(f"Gap {i+1}: Ref [{gap.reference_start}:{gap.reference_end}] ({gap.reference_length} bp) vs Qry [{gap.query_start}:{gap.query_end}] ({gap.query_length} bp)"):
                md = align.decision_metadata or {}
                
                st.markdown("**Gap Features:**")
                st.write(f"- Length Difference: {abs(gap.reference_length - gap.query_length)} bp")
                st.write(f"- DP Cells Evaluated: {getattr(align, 'cells_evaluated', 0):,}")
                
                st.markdown("**Decision Trace:**")
                st.write(f"1. **Initial Strategy Decision**: `{md.get('decision_reason', 'N/A')}`")
                st.write(f"2. **Selected Band Width (W)**: {align.band_width}")
                st.write(f"3. **Retries Executed**: {md.get('retry_count', 0)}")
                st.write(f"4. **Boundary Touched**: `{align.boundary_touched}`")
                st.write(f"5. **Full DP Fallback Triggered**: `{md.get('fallback_used', False)}`")
                st.write(f"6. **Final Executed Strategy**: `{align.strategy}`")
                
                st.markdown("**Alignment Subproblem Result:**")
                st.code(f"Ref: {align.aligned_reference}\nQry: {align.aligned_query}")
