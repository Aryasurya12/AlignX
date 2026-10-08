import streamlit as st
from anchoralign.ui.theme import render_header

def render():
    render_header()
    
    st.markdown("### Welcome to AlignX Research Studio")
    st.write("AlignX combines exact-match anchor discovery with adaptive dynamic programming to align long sequences rapidly and accurately.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**1. Exact-match anchoring**<br/>Uses KMP/Rabin-Karp to decompose sequences.", unsafe_allow_html=True)
    with col2:
        st.markdown("**2. Adaptive gap alignment**<br/>Dynamically chooses banded or full DP.", unsafe_allow_html=True)
    with col3:
        st.markdown("**3. Mutation classification**<br/>Identifies substitutions, insertions, deletions.", unsafe_allow_html=True)
        
    st.divider()
    
    st.markdown("### Current Session Metrics")
    if st.session_state.pipeline_result:
        res = st.session_state.pipeline_result
        if getattr(res, 'warnings', None):
            for w in res.warnings:
                st.warning(w)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ref Length", res.reference_length)
        c2.metric("Query Length", res.query_length)
        c3.metric("Anchors", len(res.anchors))
        c4.metric("Mutations", len(res.mutations))
        st.success("An active alignment session is loaded. Explore it using the sidebar.")
    else:
        st.info("No active alignment. Go to **Sequence Alignment** to begin.")
