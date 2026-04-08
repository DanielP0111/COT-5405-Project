import unittest
from reverse_pairs_analysis import count_reverse_pairs_brute_force, count_reverse_pairs_merge_sort

class TestReversePairs(unittest.TestCase):
    def test_basic_cases(self):
        cases = [
            ([1, 3, 2, 3, 1], 4),
            ([2, 4, 1, 3, 5], 3),
            ([5, 4, 3, 2, 1], 10),
            ([1, 2, 3, 4, 5], 0),
            ([], 0),
            ([1], 0),
            ([2,1], 1)
        ]
        for arr, expected in cases:
            with self.subTest(arr=arr):
                self.assertEqual(count_reverse_pairs_brute_force(arr.copy()), expected)
                self.assertEqual(count_reverse_pairs_merge_sort(arr.copy()), expected)

if __name__ == '__main__':
    unittest.main()