"""Core mathematical solvers, independent of the user interface."""

from .logic import (
    LogicClassification,
    LogicSolverError,
    PropositionalLogic,
    PropositionalLogicSolver,
    TruthTableResult,
    TruthTableRow,
)
from .combinatorics import CalculationResult, CombinatoricsSolver
from .graphs import AdjacencyMatrixResult, GraphSolver, ShortestPathResult
from .sets_theory import SetTheorySolver

__all__ = [
    "AdjacencyMatrixResult",
    "CalculationResult",
    "CombinatoricsSolver",
    "GraphSolver",
    "LogicClassification",
    "LogicSolverError",
    "PropositionalLogic",
    "PropositionalLogicSolver",
    "SetTheorySolver",
    "ShortestPathResult",
    "TruthTableResult",
    "TruthTableRow",
]
