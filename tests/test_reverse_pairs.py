# Composed by Kevin Pereda and Daniel Perera
# This file is unit tests we created to use in reverse_pairs_analysis
# to make sure before we do any runtime testing the algorithms are finding the
# correct number of reverse pairs


import unittest  # import unittest so we can facilitate the creation of our unit tests

from reverse_pairs_analysis import (
    count_reverse_pairs_brute_force,
    count_reverse_pairs_merge_sort,
)


# This class defines a set of unit tests for the algorithms we wrote to solve reverse pairs problem
class TestReversePairs(unittest.TestCase):

    # Method contains several test cases. Each test case consists of an input array, followed by the number of expected reverse pairs would be found in that array
    def test_basic_cases(self):
        cases = [
            ([1, 3, 2, 3, 1], 2),   
            ([2, 4, 1, 3, 5], 1),  
            ([5, 4, 3, 2, 1], 4),   
            ([1, 2, 3, 4, 5], 0),    
            ([], 0),                 
            ([1], 0),    
        ]

        # Now that we have our list of cases we have to loop through it and run the tests
        # arr will contain arr and expected contains the expected value from cases list
        for arr, expected in cases:

            # This allows us to run test cases independantly even if one fails the next one will run
            with self.subTest(arr=arr):

                # assertEqual is a method defined by the unttest.Testcase class that checks if a == b if it isnt it will auto report it as failing

                # We pass in as an argument a copy of the array into our algorithms and see if the algorithm returns the correct pair count
                self.assertEqual(count_reverse_pairs_brute_force(arr.copy()), expected)
                self.assertEqual(count_reverse_pairs_merge_sort(arr.copy()), expected)


if __name__ == "__main__": # auto runs if it is ran from directly
    unittest.main() # runs all unit tests found in the file
