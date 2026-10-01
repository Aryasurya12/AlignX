import streamlit as st
import pandas as pd
from anchoralign.pipeline.orchestrator import run_pipeline
from anchoralign.config import AnchorAlignConfig

st.set_page_config(page_title="AnchorAlign", layout="wide")

st.title("AnchorAlign Phase 1 UI")
st.markdown("Adaptive Anchor-Guided DNA Sequence Alignment - Anchor Engine Prototype")

# Sidebar configuration
st.sidebar.header("Configuration")
l_min = st.sidebar.number_input("L_min (Minimum Match Length)", min_value=1, value=5)
algo = st.sidebar.selectbox("Anchor Algorithm", ["kmp", "rabin-karp"])
merge_threshold = st.sidebar.number_input("Merge Threshold", min_value=0, value=5)

# Main inputs
col1, col2 = st.columns(2)
with col1:
    st.subheader("Reference Sequence")
    ref_seq = st.text_area("Input Reference DNA", value="ACGTAACCGGTTACGTACGTAACCGGTT", height=150)

with col2:
    st.subheader("Query Sequence")
    query_seq = st.text_area("Input Query DNA", value="ACGTAACCGGTACGTACGTAACCGGTT", height=150)

if st.button("Run Pipeline"):
    if not ref_seq or not query_seq:
        st.warning("Please provide both sequences.")
    else:
        config = AnchorAlignConfig(
            L_min=l_min,
            anchor_algorithm=algo,
            anchor_merge_threshold=merge_threshold
        )
        
        with st.spinner("Running Anchor Engine..."):
            try:
                result = run_pipeline(ref_seq, query_seq, config)
                
                st.success("Pipeline executed successfully!")
                
                # Metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("Reference Length", result.reference_length)
                m2.metric("Query Length", result.query_length)
                m3.metric("Anchors Found", len(result.anchors))
                
                # Anchors Table
                if result.anchors:
                    st.subheader("Ordered Anchors")
                    anchor_data = []
                    for a in result.anchors:
                        anchor_data.append({
                            "Reference Start": a.reference_start,
                            "Reference End": a.reference_end,
                            "Query Start": a.query_start,
                            "Query End": a.query_end,
                            "Length": a.length,
                            "Algorithm": a.source_algorithm
                        })
                    df = pd.DataFrame(anchor_data)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No anchors found meeting the criteria.")
                    
            except Exception as e:
                st.error(f"Error during execution: {e}")
