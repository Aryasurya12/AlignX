import os
import pandas as pd
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '../results')
PLOTS_DIR = os.path.join(os.path.dirname(__file__), '../plots')

def setup_dirs():
    os.makedirs(PLOTS_DIR, exist_ok=True)

def plot_safety_margin():
    path = os.path.join(RESULTS_DIR, 'safety_margin_results.csv')
    if not os.path.exists(path): return
    df = pd.read_csv(path)
    
    # Extract margin from case_id
    df['margin'] = df['case_id'].apply(lambda x: int(x.split('_')[1]))
    df = df.sort_values('margin')
    
    # Margin vs Runtime
    plt.figure(figsize=(8, 5))
    plt.plot(df['margin'], df['adaptive_runtime'], marker='o', label='Adaptive Band')
    plt.axhline(df['baseline_runtime'].mean(), color='r', linestyle='--', label='Baseline')
    plt.xlabel('Safety Margin')
    plt.ylabel('Runtime (s)')
    plt.title('Safety Margin vs Runtime')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(PLOTS_DIR, 'safety_margin_vs_runtime.png'))
    plt.close()
    
    # Margin vs Correctness
    plt.figure(figsize=(8, 5))
    plt.plot(df['margin'], df['mutation_correct'].astype(int), marker='s')
    plt.xlabel('Safety Margin')
    plt.ylabel('Correctness (1=True, 0=False)')
    plt.title('Safety Margin vs Correctness')
    plt.ylim(-0.1, 1.1)
    plt.grid(True)
    plt.savefig(os.path.join(PLOTS_DIR, 'safety_margin_vs_correctness.png'))
    plt.close()

def main():
    setup_dirs()
    plot_safety_margin()
    print("Generated Phase 5 plots.")

if __name__ == "__main__":
    main()
