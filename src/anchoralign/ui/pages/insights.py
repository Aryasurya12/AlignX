import streamlit as st

def render():
    st.header("Explainable Algorithm Decision Inspector")
    if not st.session_state.pipeline_result:
        st.info("Run an alignment to inspect decisions.")
        return

    res = st.session_state.pipeline_result
    
    st.subheader("Pipeline Timings")
    timings = getattr(res, 'timings', {})
    if timings:
        c1, c2 = st.columns(2)
        with c1:
            for k, v in timings.items():
                st.write(f"- **{k}**: {v*1000:.2f} ms")
        with c2:
            st.metric("Total Runtime", f"{st.session_state.runtimes.get('pipeline', 0):.4f} s")
    else:
        st.write("No granular timings recorded.")

    st.subheader("Gap Algorithm Decisions")
    if not res.gaps:
        st.info("No gaps to inspect.")
    else:
        for i, (gap, align) in enumerate(zip(res.gaps, res.alignments)):
            with st.expander(f"Gap {i+1}: Ref [{gap.reference_start}:{gap.reference_end}] vs Qry [{gap.query_start}:{gap.query_end}]"):
                md = align.decision_metadata or {}
                
                st.markdown("**Gap Features:**")
                st.write(f"- Length Difference: {abs((gap.reference_end - gap.reference_start) - (gap.query_end - gap.query_start))}")
                
                st.markdown("**Decision Trace:**")
                st.write(f"1. **Initial Strategy**: `{md.get('decision_reason', 'N/A')}`")
                st.write(f"2. **Selected Band Width**: {align.band_width}")
                st.write(f"3. **Retries Executed**: {md.get('retry_count', 0)}")
                st.write(f"4. **Boundary Touched**: {align.boundary_touched}")
                st.write(f"5. **Full DP Fallback Triggered**: {md.get('fallback_used', False)}")
                st.write(f"6. **Final Executed Strategy**: `{align.strategy}`")
                
                st.markdown("**Alignment Result:**")
                st.code(f"Ref: {align.aligned_reference}\\nQry: {align.aligned_query}")
