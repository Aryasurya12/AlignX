import os
import csv
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../results'))
PLOTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../plots'))

def setup_dirs():
    os.makedirs(PLOTS_DIR, exist_ok=True)

def read_csv(filename):
    path = os.path.join(RESULTS_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def plot_similarity_results():
    data = read_csv('similarity_results.csv')
    if not data: return
    
    similarities = [float(row['target_similarity']) for row in data]
    adaptive_runtimes = [float(row['adaptive_runtime']) for row in data]
    baseline_runtimes = [float(row['baseline_runtime']) for row in data]
    speedups = [float(row['speedup']) for row in data]
    
    # Plot 1: Runtime vs Similarity
    plt.figure()
    plt.scatter(similarities, adaptive_runtimes, label='Adaptive Runtime', alpha=0.7)
    plt.scatter(similarities, baseline_runtimes, label='Baseline Runtime', alpha=0.7)
    plt.xlabel('Target Similarity')
    plt.ylabel('Runtime (s)')
    plt.title('Runtime vs Similarity (500bp)')
    plt.legend()
    plt.savefig(os.path.join(PLOTS_DIR, 'runtime_vs_similarity.png'))
    plt.close()
    
    # Plot 2: Speedup vs Similarity
    plt.figure()
    plt.scatter(similarities, speedups, color='green')
    plt.xlabel('Target Similarity')
    plt.ylabel('Speedup (Baseline / Adaptive)')
    plt.title('Speedup vs Similarity (500bp)')
    plt.savefig(os.path.join(PLOTS_DIR, 'speedup_vs_similarity.png'))
    plt.close()

def plot_bandwidth_results():
    data = read_csv('band_width_results.csv')
    if not data: return
    
    bws = [int(row['band_width']) for row in data]
    runtimes = [float(row['adaptive_runtime']) for row in data]
    corrects = [1 if row['mutation_correct'] == 'True' else 0 for row in data]
    
    # Plot 6: Band width vs runtime
    plt.figure()
    plt.plot(bws, runtimes, marker='o')
    plt.xlabel('Band Width')
    plt.ylabel('Adaptive Runtime (s)')
    plt.title('Band Width vs Runtime')
    plt.savefig(os.path.join(PLOTS_DIR, 'bandwidth_vs_runtime.png'))
    plt.close()
    
    # Plot 5: Band width vs Correctness
    plt.figure()
    plt.plot(bws, corrects, marker='x', color='red')
    plt.xlabel('Band Width')
    plt.ylabel('Correctness (1=True, 0=False)')
    plt.title('Band Width vs Correctness')
    plt.savefig(os.path.join(PLOTS_DIR, 'bandwidth_vs_correctness.png'))
    plt.close()

def plot_lmin_results():
    data = read_csv('lmin_results.csv')
    if not data: return
    
    lmins = [int(row['l_min']) for row in data]
    anchor_counts = [int(row['anchor_count']) for row in data]
    runtimes = [float(row['adaptive_runtime']) for row in data]
    
    # Plot 7: L_min vs Anchor Count
    plt.figure()
    plt.plot(lmins, anchor_counts, marker='o', color='purple')
    plt.xlabel('L_min')
    plt.ylabel('Anchor Count')
    plt.title('L_min vs Anchor Count')
    plt.savefig(os.path.join(PLOTS_DIR, 'lmin_vs_anchor_count.png'))
    plt.close()
    
    # Plot 8: L_min vs Runtime
    plt.figure()
    plt.plot(lmins, runtimes, marker='o', color='orange')
    plt.xlabel('L_min')
    plt.ylabel('Adaptive Runtime (s)')
    plt.title('L_min vs Runtime')
    plt.savefig(os.path.join(PLOTS_DIR, 'lmin_vs_runtime.png'))
    plt.close()

def plot_scaling_results():
    data = read_csv('scaling_results.csv')
    if not data: return
    
    lengths = [int(row['sequence_length']) for row in data]
    a_runtimes = [float(row['adaptive_runtime']) for row in data]
    b_runtimes = [float(row['baseline_runtime']) for row in data]
    
    # Plot 10: Sequence Length vs Runtime
    plt.figure()
    plt.plot(lengths, a_runtimes, marker='o', label='Adaptive Runtime')
    plt.plot(lengths, b_runtimes, marker='x', label='Baseline Runtime')
    plt.xlabel('Sequence Length')
    plt.ylabel('Runtime (s)')
    plt.title('Sequence Length vs Runtime')
    plt.legend()
    plt.savefig(os.path.join(PLOTS_DIR, 'scaling_vs_runtime.png'))
    plt.close()
    
def plot_anchor_coverage():
    data = read_csv('anchor_coverage_results.csv')
    if not data: return
    
    cov = [float(row['anchor_coverage']) for row in data]
    runtimes = [float(row['adaptive_runtime']) for row in data]
    
    # Plot 4: Anchor Coverage vs Runtime
    plt.figure()
    plt.scatter(cov, runtimes, color='teal')
    plt.xlabel('Anchor Coverage')
    plt.ylabel('Adaptive Runtime (s)')
    plt.title('Anchor Coverage vs Runtime')
    plt.savefig(os.path.join(PLOTS_DIR, 'anchor_coverage_vs_runtime.png'))
    plt.close()

def main():
    setup_dirs()
    plot_similarity_results()
    plot_bandwidth_results()
    plot_lmin_results()
    plot_scaling_results()
    plot_anchor_coverage()
    print("Generated all plots in experiments/plots/")

if __name__ == '__main__':
    main()
