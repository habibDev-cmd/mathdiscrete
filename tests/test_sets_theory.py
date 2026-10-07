import unittest

import numpy as np

from core import SetTheorySolver


class SetTheorySolverTests(unittest.TestCase):
    def test_operations_with_two_inputs(self) -> None:
        solver = SetTheorySolver([1, 2, 3], [3, 4])

        self.assertEqual(solver.union(), {1, 2, 3, 4})
        self.assertEqual(solver.intersection(), {3})
        self.assertEqual(solver.difference(), {1, 2})
        self.assertEqual(solver.symmetric_difference(), {1, 2, 4})
        self.assertEqual(
            solver.cartesian_product(),
            {(1, 3), (1, 4), (2, 3), (2, 4), (3, 3), (3, 4)},
        )

    def test_accepts_numpy_arrays(self) -> None:
        solver = SetTheorySolver(np.array([1, 2]), np.array([2, 3]))

        self.assertEqual(solver.intersection(), {2})

    def test_handles_empty_collections(self) -> None:
        solver = SetTheorySolver([], [1, 2], [])

        self.assertEqual(solver.union(), {1, 2})
        self.assertEqual(solver.intersection(), set())
        self.assertEqual(solver.difference(), set())
        self.assertEqual(solver.symmetric_difference(), {1, 2})
        self.assertEqual(solver.cartesian_product(), set())

    def test_multi_input_difference_and_symmetric_difference(self) -> None:
        solver = SetTheorySolver([1, 2, 3, 4], [2, 3], [3, 4])

        self.assertEqual(solver.difference(), {1})
        self.assertEqual(solver.symmetric_difference(), {1, 3})

    def test_requires_at_least_two_collections(self) -> None:
        with self.assertRaises(ValueError):
            SetTheorySolver([1, 2])

    def test_rejects_unhashable_elements(self) -> None:
        with self.assertRaises(TypeError):
            SetTheorySolver([[1]], [2])


if __name__ == "__main__":
    unittest.main()