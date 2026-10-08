import streamlit as st

def render():
    st.header("Baseline Comparison")
    
    if not st.session_state.pipeline_result:
        st.info("No alignment run is active. Please go to **Sequence Alignment** to run an alignment.")
        return

    if not st.session_state.baseline_result:
        st.info("No baseline comparison available. Return to **Sequence Alignment** and check 'Run Full DP Baseline for Comparison' before running.")
        return

    res = st.session_state.pipeline_result
    base = st.session_state.baseline_result
    
    st.markdown("### Performance Comparison")
    c1, c2, c3 = st.columns(3)
    
    rt_res = st.session_state.runtimes.get('pipeline', 0)
    rt_base = base.get('runtime', 0)
    
    c1.metric("AnchorAlign Runtime", f"{rt_res:.4f} s")
    c2.metric("Full DP Runtime", f"{rt_base:.4f} s")
    
    if rt_res > 0 and rt_base > 0:
        speedup = rt_base / rt_res
        c3.metric("Speedup", f"{speedup:.2f}x")
    else:
        c3.metric("Speedup", "N/A")
        
    st.markdown("### Correctness Verification")
    c4, c5 = st.columns(2)
    score_res = res.final_alignment.score
    score_base = base.get('score', 0)
    c4.metric("AnchorAlign Score", score_res)
    c5.metric("Full DP Score", score_base)
    
    if score_res == score_base:
        st.success("Optimal Score Verified: AnchorAlign reached the exact optimal alignment score.")
    else:
        st.warning("Score Divergence: AnchorAlign score differs from the Full DP optimal score.")
