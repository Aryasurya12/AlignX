import streamlit as st
from anchoralign.ui.theme import apply_theme
from anchoralign.ui.components import initialize_session
from anchoralign.ui.pages import overview, alignment, baseline, explorer, mutations, insights, benchmarks, export

st.set_page_config(page_title="AlignX", layout="wide")

apply_theme()
initialize_session()

with st.sidebar:
    st.markdown("### Navigation")
    selection = st.radio("Go to", [
        "Overview",
        "Sequence Alignment",
        "Baseline Comparison",
        "Alignment Explorer",
        "Mutation Analysis",
        "Algorithm Insights",
        "Benchmark Lab",
        "Export & Reproducibility"
    ], label_visibility="collapsed")
    
    st.divider()
    st.markdown("### AlignX Studio")
    st.caption("Adaptive Anchor-Guided DNA Sequence Alignment")

if selection == "Overview":
    overview.render()
elif selection == "Sequence Alignment":
    alignment.render()
elif selection == "Baseline Comparison":
    baseline.render()
elif selection == "Alignment Explorer":
    explorer.render()
elif selection == "Mutation Analysis":
    mutations.render()
elif selection == "Algorithm Insights":
    insights.render()
elif selection == "Benchmark Lab":
    benchmarks.render()
elif selection == "Export & Reproducibility":
    export.render()
