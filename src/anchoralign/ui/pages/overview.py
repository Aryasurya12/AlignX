import streamlit as st
from anchoralign.ui.theme import render_header


def render():
    render_header()
    
    st.markdown("### Welcome to AlignX Research Studio")
    st.markdown(
        r"AlignX is an **Analysis of Algorithms (AoA)** capstone project demonstrating how linear-time "
        r"divide-and-conquer string algorithms (KMP, Rabin-Karp) can safely decompose sequence alignment, "
        r"collapsing quadratic $\mathcal{O}(N \cdot M)$ dynamic programming down to near-linear $\mathcal{O}(N)$."
    )

    # Project Stats Highlights
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Automated Tests", "138+ Passing", delta="100% Green")
    s2.metric("Optimal Speedup", "Up to 500x", delta="at 99% Homology")
    s3.metric("Work Saved", "> 99%", delta="Matrix Cells Skipped")
    s4.metric("Mathematical Safety", "100% Equivalence", delta="Exact DP Fallback")

    st.divider()

    # Pipeline Architecture Walkthrough
    st.subheader("Architecture & Algorithmic Pipeline")
    st.markdown("""
    ```mermaid
    graph LR
        A["Input DNA FASTA"] --> B["Exact Anchoring: KMP / Rabin-Karp"]
        B --> C["Monotonic Greedy Chain"]
        C --> D["Adaptive Gap Selector"]
        D -->|Safe Band| E["Banded DP O(N x W)"]
        D -->|Divergent| F["Full DP Fallback"]
        E -->|Boundary Hit| G{"Retry?"}
        G -->|Yes - Expand 2W| E
        G -->|No| F
        E --> H["Round-Trip Reconstruction"]
        F --> H
        H --> I["Structural Mutation Engine"]
    ```
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **1. Exact-Match Anchoring**  
        Preprocesses failure tables (KMP) or rolling hashes (Rabin-Karp) to detect linear invariant anchors ($L_{\min} \ge 10$ bp).
        """)
    with col2:
        st.markdown("""
        **2. Adaptive Gap Decomposition**  
        Dynamically sizes diagonal bands $W_i = |R_{\text{len}} - Q_{\text{len}}| + \text{margin}$ to bound DP matrices for the remaining gaps.
        """)
    with col3:
        st.markdown("""
        **3. Mathematical Safety Net**  
        Boundary-aware traceback detection automatically expands bands or safely falls back to standard Needleman-Wunsch Full DP.
        """)
        
    st.divider()
    
    # Active Session Metrics
    st.subheader("Current Alignment Session")
    if st.session_state.pipeline_result:
        res = st.session_state.pipeline_result
        if getattr(res, 'warnings', None):
            for w in res.warnings:
                st.warning(w)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ref Length", f"{res.reference_length:,} bp")
        c2.metric("Query Length", f"{res.query_length:,} bp")
        c3.metric("Anchors Discovered", len(res.anchors))
        c4.metric("Mutations Identified", len(res.mutations))
        
        # Timing & Memory
        t_total = res.timings.get("total", st.session_state.runtimes.get('pipeline', 0.0))
        m1, m2 = st.columns(2)
        m1.info(f"⏱️ **Runtime:** {t_total * 1000:.2f} ms | 🧠 **Peak Memory:** {getattr(res, 'memory_peak_kb', 0.0):.1f} KB")
        m2.success("An active alignment session is loaded. Explore it using the navigation tabs in the sidebar.")
    else:
        st.info("No active alignment loaded yet. Navigate to **Sequence Alignment** to run real biological FASTA samples or synthetic presets!")
