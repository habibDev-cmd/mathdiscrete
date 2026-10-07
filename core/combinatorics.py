"""Exact combinatorics calculations and lazy enumerators."""

from __future__ import annotations

import itertools
import math
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import TypeVar


Element = TypeVar("Element")


@dataclass
class CalculationResult:
    """Detailed calculation steps and the final integer result."""

    steps: list[str]
    result: int


class CombinatoricsSolver:
    """Calculate common combinatorics quantities and enumerate outcomes."""

    def permutation(self, n: int, r: int) -> CalculationResult:
        """Return the number of ordered selections with LaTeX working steps."""
        self._validate_selection(n, r)
        result = math.perm(n, r)
        expanded_terms = self._descending_product(n, r)
        steps = [
            r"P(n, r) = \frac{n!}{(n-r)!}",
            rf"P({n}, {r}) = \frac{{{n}!}}{{({n}-{r})!}} = "
            rf"\frac{{{n}!}}{{{n - r}!}}",
            rf"P({n}, {r}) = {expanded_terms} = {result}",
        ]
        return CalculationResult(steps=steps, result=result)

    def combination(self, n: int, r: int) -> CalculationResult:
        """Return the number of unordered selections with LaTeX working steps."""
        self._validate_selection(n, r)
        result = math.comb(n, r)
        numerator = self._descending_product(n, r)
        denominator = self._descending_product(r, r)
        steps = [
            r"C(n, r) = \frac{n!}{r!(n-r)!}",
            rf"C({n}, {r}) = \frac{{{n}!}}{{{r}!({n}-{r})!}} = "
            rf"\frac{{{n}!}}{{{r}!{n - r}!}}",
            rf"C({n}, {r}) = \frac{{{numerator}}}{{{denominator}}} = {result}",
        ]
        return CalculationResult(steps=steps, result=result)

    def permutations(self, n: int, r: int) -> CalculationResult:
        """Backward-compatible plural alias for :meth:`permutation`."""
        return self.permutation(n, r)

    def combinations(self, n: int, r: int) -> CalculationResult:
        """Backward-compatible plural alias for :meth:`combination`."""
        return self.combination(n, r)

    def factorial(self, n: int) -> int:
        """Return n factorial for a non-negative integer n."""
        self._validate_non_negative_integer(n, "n")
        return math.factorial(n)

    def pigeonhole_minimum(self, items: int, containers: int) -> int:
        """Return the minimum occupancy guaranteed in at least one container.

        The result is the ceiling of ``items / containers``. At least one
        container is required; zero items are allowed and return zero.
        """
        self._validate_non_negative_integer(items, "items")
        self._validate_non_negative_integer(containers, "containers", minimum=1)
        return (items + containers - 1) // containers

    def iter_permutations(
        self,
        values: Iterable[Element],
        r: int | None = None,
    ) -> Iterator[tuple[Element, ...]]:
        """Lazily yield ordered selections from values."""
        items = tuple(values)
        selection_size = len(items) if r is None else r
        self._validate_non_negative_integer(selection_size, "r")
        return itertools.permutations(items, selection_size)

    def iter_combinations(
        self,
        values: Iterable[Element],
        r: int,
    ) -> Iterator[tuple[Element, ...]]:
        """Lazily yield unordered selections from values."""
        self._validate_non_negative_integer(r, "r")
        return itertools.combinations(tuple(values), r)

    def _validate_selection(self, n: int, r: int) -> None:
        self._validate_non_negative_integer(n, "n")
        self._validate_non_negative_integer(r, "r")
        if r > n:
            raise ValueError("r must not be greater than n.")

    @staticmethod
    def _descending_product(value: int, count: int) -> str:
        """Format the first ``count`` descending factors starting at value."""
        if count == 0:
            return "1"
        return r" \times ".join(str(factor) for factor in range(value, value - count, -1))

    @staticmethod
    def _validate_non_negative_integer(
        value: int,
        name: str,
        minimum: int = 0,
    ) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value < minimum:
            raise ValueError(f"{name} must be at least {minimum}.")