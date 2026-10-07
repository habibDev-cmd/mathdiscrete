"""Typed propositional logic solver built on SymPy Boolean expressions."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import Mapping

from sympy import And, Not, Or, Symbol, Xor, false, satisfiable, true
from sympy.logic.boolalg import Boolean


class LogicSolverError(ValueError):
    """Raised when a propositional expression is invalid or unsupported."""


class LogicClassification(str, Enum):
    """Exhaustive classification of a propositional expression."""

    TAUTOLOGY = "tautology"
    CONTRADICTION = "contradiction"
    CONTINGENCY = "contingency"


@dataclass(frozen=True, slots=True)
class TruthTableRow:
    """One variable assignment and its evaluated expression value."""

    assignment: Mapping[str, bool]
    result: bool


@dataclass(frozen=True, slots=True)
class TruthTableResult:
    """Truth table and classification for one expression."""

    expression: str
    variables: tuple[str, ...]
    rows: tuple[TruthTableRow, ...]
    classification: LogicClassification


class PropositionalLogicSolver:
    """Parse and analyze propositional expressions using a safe operator grammar.

    Supported syntax uses Python Boolean operators: ``and``, ``or``, ``not``,
    and ``^`` for exclusive OR. Parentheses and Boolean literals are allowed.
    Function calls, attribute access, comparisons, and other Python syntax are
    rejected before expression evaluation.
    """

    def __init__(self, max_variables: int = 8) -> None:
        if max_variables < 1:
            raise ValueError("max_variables must be at least 1.")
        self._max_variables = max_variables

    @property
    def max_variables(self) -> int:
        """Return the maximum variable count accepted for truth tables."""
        return self._max_variables

    def parse(self, expression: str) -> tuple[Boolean, tuple[str, ...]]:
        """Parse supported syntax into a SymPy expression and sorted variables."""
        if not expression.strip():
            raise LogicSolverError("Expression cannot be empty.")

        try:
            syntax_tree = ast.parse(expression, mode="eval")
        except SyntaxError as error:
            raise LogicSolverError("Expression syntax is invalid.") from error

        variable_names = tuple(
            sorted(
                {
                    node.id
                    for node in ast.walk(syntax_tree)
                    if isinstance(node, ast.Name)
                }
            )
        )
        if not variable_names:
            raise LogicSolverError("Expression must contain at least one variable.")
        if len(variable_names) > self._max_variables:
            raise LogicSolverError(
                f"Expression has {len(variable_names)} variables; "
                f"the configured maximum is {self._max_variables}."
            )

        symbols = {name: Symbol(name) for name in variable_names}
        return self._convert_node(syntax_tree.body, symbols), variable_names

    def truth_table(self, expression: str) -> TruthTableResult:
        """Build all truth assignments and classify the expression."""
        symbolic_expression, variable_names = self.parse(expression)
        rows = tuple(
            self._evaluate_row(symbolic_expression, variable_names, values)
            for values in product((False, True), repeat=len(variable_names))
        )
        classification = self._classify(symbolic_expression)
        return TruthTableResult(
            expression=expression,
            variables=variable_names,
            rows=rows,
            classification=classification,
        )

    def classify(self, expression: str) -> LogicClassification:
        """Classify an expression without materializing its truth table."""
        symbolic_expression, _ = self.parse(expression)
        return self._classify(symbolic_expression)

    def _convert_node(
        self,
        node: ast.expr,
        symbols: Mapping[str, Symbol],
    ) -> Boolean:
        if isinstance(node, ast.Name):
            return symbols[node.id]
        if isinstance(node, ast.Constant) and isinstance(node.value, bool):
            return true if node.value else false
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return Not(self._convert_node(node.operand, symbols))
        if isinstance(node, ast.BoolOp):
            operands = [self._convert_node(value, symbols) for value in node.values]
            if isinstance(node.op, ast.And):
                return And(*operands)
            if isinstance(node.op, ast.Or):
                return Or(*operands)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitXor):
            return Xor(
                self._convert_node(node.left, symbols),
                self._convert_node(node.right, symbols),
            )
        raise LogicSolverError(
            f"Unsupported syntax: {type(node).__name__}. "
            "Use variables with and, or, not, and ^ operators."
        )

    def _evaluate_row(
        self,
        expression: Boolean,
        variable_names: tuple[str, ...],
        values: tuple[bool, ...],
    ) -> TruthTableRow:
        assignment = dict(zip(variable_names, values, strict=True))
        substitutions = {
            Symbol(name): value for name, value in assignment.items()
        }
        evaluated = expression.subs(substitutions)
        if evaluated not in (true, false):
            raise LogicSolverError("Expression did not evaluate to a Boolean value.")
        return TruthTableRow(assignment=assignment, result=bool(evaluated))

    def _classify(self, expression: Boolean) -> LogicClassification:
        if satisfiable(expression) is False:
            return LogicClassification.CONTRADICTION
        if satisfiable(Not(expression)) is False:
            return LogicClassification.TAUTOLOGY
        return LogicClassification.CONTINGENCY


PropositionalLogic = PropositionalLogicSolver
