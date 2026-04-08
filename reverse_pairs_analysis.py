import argparse
import csv
import os
import random
import time

#needed for plotting and numpy for mean, etc
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#These are imports needed to run the unit tests we created in test_reverse_pairs.py
import unittest
from tests import test_reverse_pairs 

# Use Agg backend for headless environments
matplotlib.use('Agg')

RESULTS_DIR_DEFAULT = 'results'

# Algorithm 1: Brute Force Approach
def count_reverse_pairs_brute_force(arr):
    # Check every pair (i, j) and make note of ones where i < j and a[i] > 2 * a[j]
    rev_pair_count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > 2 * arr[j]:
                rev_pair_count += 1
    return rev_pair_count

# Algorithm 2: Modified Merge Sort Approach
def count_reverse_pairs_merge_sort(arr):
    def merge_count(arr, temp_arr, left, mid, right):
        i = left
        j = mid + 1
        k = left
        rev_pair_count = 0

        # PASS 1: Count only (do NOT merge here)
        # Use two independent pointers to find pairs where arr[i] > 2 * arr[j]
        j_count = mid + 1  # Separate pointer so we don't disturb the merge
        for i in range(left, mid + 1):
            # Advance j_count while the 2x condition holds
            while j_count <= right and arr[i] > 2 * arr[j_count]:
                j_count += 1
            # All elements arr[mid+1..j_count-1] satisfy arr[i] > 2 * arr[x]
            rev_pair_count += (j_count - (mid + 1))

        # PASS 2: Merge only (standard merge, separate from counting for reverse pairs)
        # Below is just standard merging process foung in merge sort nothing super fancy
        i = left
        j = mid + 1
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp_arr[k] = arr[i]
                i += 1
            else:
                temp_arr[k] = arr[j]
                j += 1
            k += 1
        while i <= mid:
            temp_arr[k] = arr[i]
            i += 1
            k += 1
        while j <= right:
            temp_arr[k] = arr[j]
            j += 1
            k += 1
        for i in range(left, right + 1):
            arr[i] = temp_arr[i]

        return rev_pair_count
    
    # Recursively splits the array in half, sorts each half, and accumulates
    # reverse pair counts from the left half, right half, and cross paths
    def merge_sort_count(arr, temp_arr, left, right):
        rev_pair_count = 0
        if left < right:
            mid = (left + right) // 2
            rev_pair_count += merge_sort_count(arr, temp_arr, left, mid)
            rev_pair_count += merge_sort_count(arr, temp_arr, mid + 1, right)
            rev_pair_count += merge_count(arr, temp_arr, left, mid, right)
        return rev_pair_count

    n = len(arr)
    if n == 0:
        return 0
    temp_arr = [0] * n
    # Work on a copy so the original input array is not modified.
    arr_copy = arr.copy()
    return merge_sort_count(arr_copy, temp_arr, 0, n - 1)

# This function takes the algorithm the array we are testing it on and the amount of runs
# We want to run it 5 times to make sure result doesnt get skewed from a single fluke
def measure_time(algorithm, arr, num_runs=5):
    # Run multiple times and report mean/std for stability.
    times = []
    for _ in range(num_runs):
        arr_copy = arr.copy()
        start = time.perf_counter() #perf counter is higher precision than time.time
        algorithm(arr_copy) #run algorithm on copy of array so it always gets unsorted input
        end = time.perf_counter() # end timer 
        times.append((end - start) * 1000)  # ms
    return float(np.mean(times)), float(np.std(times)) # after all 5 runs we just want to return the average time and how much it varied across runs

# Generate test data
def generate_test_arrays(sizes, seed=42):
    # Fixed seed keeps experiments reproducible.
    random.seed(seed)
    test_data = {}
    for size in sizes:
        test_data[size] = [random.randint(1, 10000) for _ in range(size)]
    return test_data

# Run experiments
def run_experiments(num_runs=5, quick=False):
    # Quick mode uses smaller inputs for faster checks.
    if quick:
        sizes = [50, 200, 500, 1000]
        large_sizes = [2000]
    else:
        sizes = [100, 500, 1000, 2000, 3000, 5000, 7500, 10000]
        large_sizes = [20000, 50000, 75000, 100000]

    print("Generating test data...")
    test_data = generate_test_arrays(sizes)
    large_test_data = generate_test_arrays(large_sizes, seed=43)

    results = {
        'sizes': [],
        'brute_force_times': [],
        'brute_force_std': [],
        'merge_sort_times': [],
        'merge_sort_std': []
    }

    print("\nRunning experiments for both algorithms...")
    for size in sizes:
        print(f"Testing size: {size}")
        arr = test_data[size]
        bf_time, bf_std = measure_time(count_reverse_pairs_brute_force, arr, num_runs=num_runs)
        ms_time, ms_std = measure_time(count_reverse_pairs_merge_sort, arr, num_runs=num_runs)

        results['sizes'].append(size)
        results['brute_force_times'].append(bf_time)
        results['brute_force_std'].append(bf_std)
        results['merge_sort_times'].append(ms_time)
        results['merge_sort_std'].append(ms_std)

        print(f"  Brute Force: {bf_time:.4f} ms (±{bf_std:.4f})")
        print(f"  Merge Sort:  {ms_time:.4f} ms (±{ms_std:.4f})")

    large_results = {
        'sizes': [],
        'merge_sort_times': [],
        'merge_sort_std': []
    }

    print("\nRunning experiments for merge sort on larger inputs...")
    # Skip brute force here because O(n^2) is too slow at large n.
    for size in large_sizes:
        print(f"Testing size: {size}")
        arr = large_test_data[size]
        ms_time, ms_std = measure_time(count_reverse_pairs_merge_sort, arr, num_runs=num_runs)
        large_results['sizes'].append(size)
        large_results['merge_sort_times'].append(ms_time)
        large_results['merge_sort_std'].append(ms_std)
        print(f"  Merge Sort: {ms_time:.4f} ms (±{ms_std:.4f})")

    return results, large_results

# Visualization functions (save to results_dir)
def plot_scalability(results, large_results, results_dir):
    plt.figure(figsize=(12, 7))
    plt.errorbar(results['sizes'], results['brute_force_times'],
                 yerr=results['brute_force_std'],
                 marker='o', label='Brute Force O(n²)',
                 capsize=5, linewidth=2, markersize=8)
    plt.errorbar(results['sizes'], results['merge_sort_times'],
                 yerr=results['merge_sort_std'],
                 marker='s', label='Modified Merge Sort O(n log n)',
                 capsize=5, linewidth=2, markersize=8)
    if large_results['sizes']:
        plt.errorbar(large_results['sizes'], large_results['merge_sort_times'],
                     yerr=large_results['merge_sort_std'],
                     marker='s', color='C1', capsize=5,
                     linewidth=2, markersize=8, linestyle='--')
    plt.xlabel('Array Size (n)', fontsize=12)
    plt.ylabel('Execution Time (ms)', fontsize=12)
    plt.title('Scalability Comparison: Reverse Pairs Algorithms', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    out = os.path.join(results_dir, 'scalability_graph.png')
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {out}")

def plot_growth_comparison(results, results_dir):
    plt.figure(figsize=(12, 7))
    sizes = np.array(results['sizes'])
    plt.plot(sizes, results['brute_force_times'],
             marker='o', label='Brute Force (Actual)', linewidth=2, markersize=8)
    plt.plot(sizes, results['merge_sort_times'],
             marker='s', label='Merge Sort (Actual)', linewidth=2, markersize=8)
    # Fit simple constants so theoretical curves align in scale with measurements.
    c1 = results['brute_force_times'][-1] / (sizes[-1] ** 2)
    c2 = results['merge_sort_times'][-1] / (sizes[-1] * np.log2(sizes[-1]))
    theoretical_n2 = c1 * (sizes ** 2)
    theoretical_nlogn = c2 * (sizes * np.log2(sizes))
    plt.plot(sizes, theoretical_n2, '--',
             label='Theoretical O(n²)', linewidth=2, alpha=0.7)
    plt.plot(sizes, theoretical_nlogn, '--',
             label='Theoretical O(n log n)', linewidth=2, alpha=0.7)
    plt.xlabel('Array Size (n)', fontsize=12)
    plt.ylabel('Execution Time (ms)', fontsize=12)
    plt.title('Empirical vs Theoretical Complexity', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    out = os.path.join(results_dir, 'growth_comparison.png')
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {out}")

def save_results_csv(results, large_results, results_dir):
    out = os.path.join(results_dir, 'timing_results.csv')
    with open(out, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['size', 'brute_force_mean_ms', 'brute_force_std_ms',
                         'merge_sort_mean_ms', 'merge_sort_std_ms'])
        for i, size in enumerate(results['sizes']):
            writer.writerow([
                size,
                results['brute_force_times'][i],
                results['brute_force_std'][i],
                results['merge_sort_times'][i],
                results['merge_sort_std'][i]
            ])
        # Add large results in separate rows (merge sort only)
        writer.writerow([])
        writer.writerow(['large_size', 'merge_sort_mean_ms', 'merge_sort_std_ms'])
        for i, size in enumerate(large_results['sizes']):
            writer.writerow([
                size,
                large_results['merge_sort_times'][i],
                large_results['merge_sort_std'][i]
            ])
    print(f"  Saved: {out}")

def parse_args():
    parser = argparse.ArgumentParser(description='Reverse Pairs Algorithm Analysis')
    parser.add_argument('--results-dir', default=RESULTS_DIR_DEFAULT, help='Directory to save outputs')
    parser.add_argument('--quick', action='store_true', help='Run a quick (smaller) experiment set')
    parser.add_argument('--num-runs', type=int, default=5, help='Number of runs to average timings')
    parser.add_argument('--no-plot', action='store_true', help='Do not open plots (headless/CI)')
    parser.add_argument('--save-data', action='store_true', help='Save timing CSV data to results dir')
    return parser.parse_args()

# Run unit tests
def run_unit_tests():
    result = unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromModule(test_reverse_pairs)) #load unit test module from out test_reverse_pairs file
    if not result.wasSuccessful():
        print("ERROR: The unit tests failed. This means the algorithms did not correctly get the amount of reverse pairs. Revise algorithms and re run.")
        exit(1)  # Exit if tests fail


if __name__ == "__main__":
    args = parse_args()
    results_dir = args.results_dir
    # Create output folder if it does not exist.
    os.makedirs(results_dir, exist_ok=True)

    print("\n" + "=" * 60)
    print("REVERSE PAIRS ALGORITHM ANALYSIS")
    print("Kevin Pereda & Daniel Perera")
    print("COT 5405 - Design and Analysis of Algorithms")
    print("=" * 60 + "\n")
    
    # First, run the unit tests
    run_unit_tests()

    print("\nStarting performance experiments...")
    results, large_results = run_experiments(num_runs=args.num_runs, quick=args.quick)

    print("\nGENERATING VISUALIZATIONS")
    plot_scalability(results, large_results, results_dir)
    plot_growth_comparison(results, results_dir)

    if args.save_data:
        save_results_csv(results, large_results, results_dir)

    print("\nEXPERIMENTS COMPLETE!")
    print("\nGenerated files in:", results_dir)
    for fname in os.listdir(results_dir):
        print("  -", fname)
