# Reverse Pairs Algorithm Analysis


## 📋 Overview

This project presents an empirical comparison of two algorithms that solve the **Reverse Pairs Problem**: a brute force approach with O(n²) complexity and a modified merge sort with O(n log n) complexity. The study validates theoretical complexity predictions through systematic performance measurements.

**Course:** COT 5405 - Design and Analysis of Algorithms  
**Institution:** [University of Central Florida]  
**Authors:** Kevin Pereda & Daniel Perera  
**Date:** Spring 2026

## 🎯 Problem Definition

Given an array `arr[]`, count the number of pairs `(i, j)` such that:
- `i < j`
- `arr[i] > arr[j]`

**Example:**
Input:  [1, 3, 2, 3, 1]
Output: 4
Pairs: (1,4), (2,3), (2,4), (3,4)

## 🔬 Algorithms Implemented

### 1. Brute Force Approach
- **Time Complexity:** O(n²)
- **Space Complexity:** O(1)
- **Technique:** Nested loops

### 2. Modified Merge Sort
- **Time Complexity:** O(n log n)
- **Space Complexity:** O(n)
- **Technique:** Divide and Conquer
