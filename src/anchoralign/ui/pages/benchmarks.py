import streamlit as st
import pandas as pd
import os
from anchoralign.ui.components import get_experiment_files, get_plot_files

def render():
    st.header("Benchmark Lab")
    
    tab1, tab2 = st.tabs(["Phase 4 & 5 Experiments", "Phase 7 Evaluation"])
    
    with tab1:
        csv_files = [f for f in get_experiment_files() if not f.startswith("phase7_")]
        plot_files = get_plot_files()

        if not csv_files:
            st.warning("No experiment results found in `experiments/results/`.")
        else:
            selected_csv = st.selectbox("Select Experiment Dataset", csv_files)
            df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'experiments', 'results', selected_csv))
            st.dataframe(df)

        if plot_files:
            st.subheader("Generated Plots")
            selected_plot = st.selectbox("Select Plot", plot_files)
            st.image(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'experiments', 'plots', selected_plot))

    with tab2:
        phase7_files = [f for f in get_experiment_files() if f.startswith("phase7_")]
        
        if not phase7_files:
            st.info("No Phase 7 benchmark results found.")
        else:
            selected_p7 = st.selectbox("Select Phase 7 Benchmark Dataset", phase7_files)
            df_p7 = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'experiments', 'results', selected_p7))

            st.subheader("Benchmark Metrics")
            if 'family' in df_p7.columns:
                selected_family = st.multiselect("Filter by Dataset Family", df_p7['family'].unique(), default=df_p7['family'].unique())
                df_filtered = df_p7[df_p7['family'].isin(selected_family)]
            else:
                df_filtered = df_p7

            st.dataframe(df_filtered, use_container_width=True)

            c1, c2, c3 = st.columns(3)
            if 'correctness' in df_filtered.columns:
                exact_matches = sum(df_filtered['correctness'] == 'Exact alignment match')
                equiv_matches = sum(df_filtered['correctness'] == 'Equivalent optimal score')
                c1.metric("Exact Matches", exact_matches)
                c2.metric("Equivalent Optimal", equiv_matches)
                c3.metric("Failures", len(df_filtered) - exact_matches - equiv_matches)

            if 'speedup' in df_filtered.columns:
                st.metric("Average Speedup", f"{df_filtered['speedup'].mean():.2f}x")
