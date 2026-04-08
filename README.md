# Reverse Pairs Algorithm Analysis

## Overview

This project presents a comparison of two algorithms that solve the **Reverse Pairs Problem**: a brute force approach with O(n²) complexity and a modified merge sort with O(n log n) complexity.

**Course:** COT 5405 - Design and Analysis of Algorithms  
**School:** [University of Central Florida]  
**Authors:** Kevin Pereda & Daniel Perera  
**Date:** Spring 2026

## Problem Definition

Given an array `arr[]`, count the number of pairs `(i, j)` such that:

- `i < j`
- `arr[i] > 2 * arr[j]`

**Example:**
Input: [1, 3, 2, 3, 1]
Output: 2
Pairs: (3, 1) (3, 1)

## Algorithms Implemented

### 1. Brute Force Approach

- **Time Complexity:** O(n²)
- **Space Complexity:** O(1)
- **Technique:** Nested loops

### 2. Modified Merge Sort

- **Time Complexity:** O(n log n)
- **Space Complexity:** O(n)
- **Technique:** Divide and Conquer

## Python Version

- **Python 3.10 or 3.11**

# Install dependencies (recommended inside a virtualenv)

pip install -r requirements.txt

# Quick verification (fast)

python reverse_pairs_analysis.py --quick --save-data

# Full experiments (may take minutes)

python reverse_pairs_analysis.py --num-runs 5 --save-data

# Outputs are saved under the `results/` directory:

- scalability_graph.png
- growth_comparison.png
- timing_results.csv
