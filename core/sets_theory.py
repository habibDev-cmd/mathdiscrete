"""Set operations for two or more iterable collections of hashable values."""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from itertools import product
from typing import TypeVar


Element = TypeVar("Element", bound=Hashable)


class SetTheorySolver:
    """Convert input collections to sets and expose common set operations.

    The solver snapshots each input during initialization. At least two input
    collections are required, but any individual collection may be empty.
    Difference is computed as the first set minus every subsequent set.
    Symmetric difference is applied successively across all input sets.
    """

    def __init__(self, *collections: Iterable[Element]) -> None:
        if len(collections) < 2:
            raise ValueError("At least two input collections are required.")

        self._sets = tuple(self._convert_to_frozenset(values) for values in collections)

    @property
    def sets(self) -> tuple[frozenset[Element], ...]:
        """Return the immutable set snapshots created from the inputs."""
        return self._sets

    def union(self) -> set[Element]:
        """Return the union of all input sets."""
        return set().union(*self._sets)

    def intersection(self) -> set[Element]:
        """Return elements present in every input set."""
        return set(self._sets[0]).intersection(*self._sets[1:])

    def difference(self) -> set[Element]:
        """Return the first set minus the union of all remaining sets."""
        return set(self._sets[0]).difference(*self._sets[1:])

    def symmetric_difference(self) -> set[Element]:
        """Return elements present in an odd number of input sets."""
        result: set[Element] = set()
        for values in self._sets:
            result.symmetric_difference_update(values)
        return result

    def cartesian_product(self) -> set[tuple[Element, ...]]:
        """Return the Cartesian product as a set of tuples."""
        return set(product(*self._sets))

    @staticmethod
    def _convert_to_frozenset(values: Iterable[Element]) -> frozenset[Element]:
        if isinstance(values, (str, bytes)):
            raise TypeError("Each input must be a collection, not a string or bytes value.")
        try:
            return frozenset(values)
        except TypeError as error:
            raise TypeError("Input elements must be hashable Python values.") from error