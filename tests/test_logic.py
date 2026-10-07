import unittest

from core.logic import (
    LogicClassification,
    LogicSolverError,
    PropositionalLogicSolver,
)


class PropositionalLogicSolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.solver = PropositionalLogicSolver()

    def test_truth_table_classifies_tautology(self) -> None:
        result = self.solver.truth_table("p or not p")

        self.assertEqual(result.classification, LogicClassification.TAUTOLOGY)
        self.assertEqual(len(result.rows), 2)
        self.assertTrue(all(row.result for row in result.rows))

    def test_classifies_contradiction_and_contingency(self) -> None:
        self.assertEqual(
            self.solver.classify("p and not p"),
            LogicClassification.CONTRADICTION,
        )
        self.assertEqual(
            self.solver.classify("p and q"),
            LogicClassification.CONTINGENCY,
        )

    def test_rejects_calls_and_attribute_access(self) -> None:
        with self.assertRaises(LogicSolverError):
            self.solver.parse("__import__('os').system('false')")

    def test_enforces_variable_limit(self) -> None:
        solver = PropositionalLogicSolver(max_variables=2)

        with self.assertRaises(LogicSolverError):
            solver.truth_table("p and q and r")

    def test_rejects_empty_expression(self) -> None:
        with self.assertRaises(LogicSolverError):
            self.solver.truth_table("  ")


if __name__ == "__main__":
    unittest.main()
