import time
import random
import matplotlib.pyplot as plt
import numpy as np

# Algorithm 1: Brute Force Approach
def count_reverse_pairs_brute_force(arr):
    """
    Count reverse pairs using brute force approach.
    
    This algorithm uses two nested loops to check every possible
    pair (i,j) where i < j. If arr[i] > arr[j], it's a reverse pair.
    
    Time Complexity: O(n^2) - Two nested loops over array
    Space Complexity: O(1) - Only uses counter variable
    
    Args:
        arr: List of integers
    
    Returns:
        int: Count of reverse pairs
    """
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count

# Algorithm 2: Modified Merge Sort
def count_reverse_pairs_merge_sort(arr):
    """
    Count reverse pairs using modified merge sort.
    
    This algorithm uses divide and conquer strategy. It recursively
    counts inversions in left half, right half, and cross-inversions
    during the merge step.
    
    Time Complexity: O(n log n) - Merge sort with inversion counting
    Space Complexity: O(n) - Temporary array for merging
    
    Args:
        arr: List of integers
    
    Returns:
        int: Count of reverse pairs
    """
    def merge_count(arr, temp_arr, left, mid, right):
        """
        Merge two sorted subarrays and count cross-inversions.
        """
        i = left    # Starting index of left subarray
        j = mid + 1 # Starting index of right subarray
        k = left    # Starting index to be sorted
        inv_count = 0
        
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp_arr[k] = arr[i]
                i += 1
            else:
                # There are (mid-i+1) inversions
                # All remaining elements in left subarray are greater than arr[j]
                temp_arr[k] = arr[j]
                inv_count += (mid - i + 1)
                j += 1
            k += 1
        
        # Copy remaining elements of left subarray
        while i <= mid:
            temp_arr[k] = arr[i]
            i += 1
            k += 1
        
        # Copy remaining elements of right subarray
        while j <= right:
            temp_arr[k] = arr[j]
            j += 1
            k += 1
        
        # Copy sorted subarray into original array
        for i in range(left, right + 1):
            arr[i] = temp_arr[i]
        
        return inv_count
    
    def merge_sort_count(arr, temp_arr, left, right):
        """
        Recursively divide array and count inversions.
        """
        inv_count = 0
        if left < right:
            mid = (left + right) // 2
            
            # Count inversions in left half
            inv_count += merge_sort_count(arr, temp_arr, left, mid)
            
            # Count inversions in right half
            inv_count += merge_sort_count(arr, temp_arr, mid + 1, right)
            
            # Count cross-inversions during merge
            inv_count += merge_count(arr, temp_arr, left, mid, right)
        
        return inv_count
    
    n = len(arr)
    temp_arr = [0] * n
    arr_copy = arr.copy()  # Make a copy to avoid modifying original
    return merge_sort_count(arr_copy, temp_arr, 0, n - 1)

# Timing function
def measure_time(algorithm, arr, num_runs=5):
    """
    Measure average execution time of an algorithm.
    
    Args:
        algorithm: Function to time
        arr: Input array
        num_runs: Number of times to run for averaging (default: 5)
    
    Returns:
        tuple: (mean_time_ms, std_dev_ms)
    """
    times = []
    for _ in range(num_runs):
        arr_copy = arr.copy()  # Create fresh copy for each run
        start = time.perf_counter()
        algorithm(arr_copy)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to milliseconds
    return np.mean(times), np.std(times)

# Generate test data
def generate_test_arrays(sizes, seed=42):
    """
    Generate random arrays for testing.
    
    Args:
        sizes: List of array sizes to generate
        seed: Random seed for reproducibility
    
    Returns:
        dict: Dictionary mapping size to random array
    """
    random.seed(seed)
    test_data = {}
    for size in sizes:
        # Generate random array with values between 1 and 10000
        test_data[size] = [random.randint(1, 10000) for _ in range(size)]
    return test_data

# Run experiments
def run_experiments():
    """
    Run timing experiments for both algorithms.
    
    Returns:
        tuple: (results_dict, large_results_dict)
    """
    # Test sizes - adjust based on your computer's performance
    # For brute force O(n^2), be careful with very large inputs
    sizes = [100, 500, 1000, 2000, 3000, 5000, 7500, 10000]
    
    # For merge sort, you can test larger sizes separately
    large_sizes = [20000, 50000, 75000, 100000]
    
    print("Generating test data...")
    test_data = generate_test_arrays(sizes)
    large_test_data = generate_test_arrays(large_sizes, seed=43)
    
    # Results storage
    results = {
        'sizes': [],
        'brute_force_times': [],
        'brute_force_std': [],
        'merge_sort_times': [],
        'merge_sort_std': []
    }
    
    print("\nRunning experiments for both algorithms...")
    print("=" * 60)
    for size in sizes:
        print(f"\nTesting size: {size}")
        arr = test_data[size]
        
        # Time brute force
        print("  Running brute force...")
        bf_time, bf_std = measure_time(count_reverse_pairs_brute_force, arr)
        
        # Time merge sort
        print("  Running merge sort...")
        ms_time, ms_std = measure_time(count_reverse_pairs_merge_sort, arr)
        
        results['sizes'].append(size)
        results['brute_force_times'].append(bf_time)
        results['brute_force_std'].append(bf_std)
        results['merge_sort_times'].append(ms_time)
        results['merge_sort_std'].append(ms_std)
        
        print(f"  Brute Force: {bf_time:.4f} ms (±{bf_std:.4f})")
        print(f"  Merge Sort:  {ms_time:.4f} ms (±{ms_std:.4f})")
    
    # Test merge sort on larger sizes
    print("\n" + "=" * 60)
    print("\nRunning experiments for merge sort on larger inputs...")
    print("=" * 60)
    large_results = {
        'sizes': [],
        'merge_sort_times': [],
        'merge_sort_std': []
    }
    
    for size in large_sizes:
        print(f"\nTesting size: {size}")
        arr = large_test_data[size]
        print("  Running merge sort...")
        ms_time, ms_std = measure_time(count_reverse_pairs_merge_sort, arr)
        
        large_results['sizes'].append(size)
        large_results['merge_sort_times'].append(ms_time)
        large_results['merge_sort_std'].append(ms_std)
        
        print(f"  Merge Sort: {ms_time:.4f} ms (±{ms_std:.4f})")
    
    return results, large_results

# Visualization functions
def plot_scalability(results, large_results):
    """
    Graph 1: Scalability comparison between both algorithms.
    Shows execution time vs array size.
    """
    plt.figure(figsize=(12, 7))
    
    # Plot both algorithms on common sizes
    plt.errorbar(results['sizes'], results['brute_force_times'], 
                 yerr=results['brute_force_std'], 
                 marker='o', label='Brute Force O(n²)', 
                 capsize=5, linewidth=2, markersize=8)
    
    plt.errorbar(results['sizes'], results['merge_sort_times'], 
                 yerr=results['merge_sort_std'], 
                 marker='s', label='Modified Merge Sort O(n log n)', 
                 capsize=5, linewidth=2, markersize=8)
    
    # Add merge sort large sizes
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
    plt.savefig('scalability_graph.png', dpi=300, bbox_inches='tight')
    print("  Saved: scalability_graph.png")
    plt.show()

def plot_theoretical_validation(results, large_results):
    """
    Graph 2: Theoretical complexity validation.
    Shows T(n)/n² for brute force and T(n)/(n log n) for merge sort.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Brute Force: T(n)/n²
    sizes = np.array(results['sizes'])
    bf_times = np.array(results['brute_force_times'])
    bf_normalized = bf_times / (sizes ** 2)
    
    ax1.plot(sizes, bf_normalized, marker='o', linewidth=2, markersize=8, color='C0')
    ax1.axhline(y=np.mean(bf_normalized), color='r', linestyle='--', 
                label=f'Average: {np.mean(bf_normalized):.2e}', linewidth=2)
    ax1.set_xlabel('Array Size (n)', fontsize=12)
    ax1.set_ylabel('T(n) / n²', fontsize=12)
    ax1.set_title('Brute Force: Normalized by n²', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Merge Sort: T(n)/(n log n)
    all_sizes = np.array(results['sizes'] + large_results['sizes'])
    all_ms_times = np.array(results['merge_sort_times'] + large_results['merge_sort_times'])
    ms_normalized = all_ms_times / (all_sizes * np.log2(all_sizes))
    
    ax2.plot(all_sizes, ms_normalized, marker='s', linewidth=2, markersize=8, color='C1')
    ax2.axhline(y=np.mean(ms_normalized), color='r', linestyle='--', 
                label=f'Average: {np.mean(ms_normalized):.2e}', linewidth=2)
    ax2.set_xlabel('Array Size (n)', fontsize=12)
    ax2.set_ylabel('T(n) / (n log n)', fontsize=12)
    ax2.set_title('Modified Merge Sort: Normalized by n log n', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('theoretical_validation.png', dpi=300, bbox_inches='tight')
    print("  Saved: theoretical_validation.png")
    plt.show()

def plot_growth_comparison(results):
    """
    Graph 3: Comparison with theoretical growth curves.
    Overlays actual performance with theoretical O(n²) and O(n log n).
    """
    plt.figure(figsize=(12, 7))
    
    sizes = np.array(results['sizes'])
    
    # Actual times
    plt.plot(sizes, results['brute_force_times'], 
             marker='o', label='Brute Force (Actual)', linewidth=2, markersize=8)
    plt.plot(sizes, results['merge_sort_times'], 
             marker='s', label='Merge Sort (Actual)', linewidth=2, markersize=8)
    
    # Theoretical curves (scaled to fit)
    # Scale factors determined by fitting to actual data
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
    plt.savefig('growth_comparison.png', dpi=300, bbox_inches='tight')
    print("  Saved: growth_comparison.png")
    plt.show()

# Verification function
def verify_algorithms():
    """
    Verify that both algorithms produce correct results.
    Tests with known inputs and expected outputs.
    """
    test_cases = [
        ([1, 3, 2, 3, 1], 4),   # Expected: 4 pairs
        ([2, 4, 1, 3, 5], 3),   # Expected: 3 pairs
        ([5, 4, 3, 2, 1], 10),  # Expected: 10 pairs (completely reversed)
        ([1, 2, 3, 4, 5], 0),   # Expected: 0 pairs (already sorted)
        ([1], 0),                # Expected: 0 pairs (single element)
        ([2, 1], 1),            # Expected: 1 pair
    ]
    
    print("=" * 60)
    print("VERIFYING ALGORITHM CORRECTNESS")
    print("=" * 60)
    
    all_passed = True
    for i, (arr, expected) in enumerate(test_cases):
        bf_result = count_reverse_pairs_brute_force(arr.copy())
        ms_result = count_reverse_pairs_merge_sort(arr.copy())
        
        bf_correct = bf_result == expected
        ms_correct = ms_result == expected
        match = bf_result == ms_result
        
        status = "✓ PASS" if (bf_correct and ms_correct and match) else "✗ FAIL"
        if not (bf_correct and ms_correct and match):
            all_passed = False
        
        print(f"\nTest {i+1}: {arr}")
        print(f"  Expected:     {expected}")
        print(f"  Brute Force:  {bf_result} {'✓' if bf_correct else '✗'}")
        print(f"  Merge Sort:   {ms_result} {'✓' if ms_correct else '✗'}")
        print(f"  Status:       {status}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("=" * 60 + "\n")
    
    return all_passed

# Main execution
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("REVERSE PAIRS ALGORITHM ANALYSIS")
    print("Kevin Pereda & Daniel Perera")
    print("COT 5405 - Design and Analysis of Algorithms")
    print("=" * 60 + "\n")
    
    # Step 1: Verify correctness
    if not verify_algorithms():
        print("ERROR: Algorithm verification failed. Please check implementation.")
        exit(1)
    
    # Step 2: Run experiments
    print("\nStarting performance experiments...")
    print("This may take several minutes...\n")
    results, large_results = run_experiments()
    
    # Step 3: Generate graphs
    print("\n" + "=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60 + "\n")
    
    print("Creating Graph 1: Scalability Comparison...")
    plot_scalability(results, large_results)
    
    print("\nCreating Graph 2: Theoretical Validation...")
    plot_theoretical_validation(results, large_results)
    
    print("\nCreating Graph 3: Growth Comparison...")
    plot_growth_comparison(results)
    
    print("\n" + "=" * 60)
    print("EXPERIMENTS COMPLETE!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - scalability_graph.png")
    print("  - theoretical_validation.png")
    print("  - growth_comparison.png")
    print("\nYou can now use these graphs in your report.")
    print("=" * 60 + "\n")
