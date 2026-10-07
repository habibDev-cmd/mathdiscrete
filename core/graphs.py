"""NetworkX-backed graph construction and analysis."""

from __future__ import annotations

import math
from collections.abc import Hashable, Iterable
from numbers import Real
from typing import Generic, Literal, TypeVar, TypedDict

import networkx as nx


Node = TypeVar("Node", bound=Hashable)


class AdjacencyMatrixResult(TypedDict, Generic[Node]):
    """Adjacency matrix together with the node order used for its rows."""

    nodes: list[Node]
    matrix: list[list[float]]
    directed: bool


class ShortestPathResult(TypedDict, Generic[Node]):
    """Structured result for one Dijkstra shortest-path query."""

    status: Literal["ok", "no_path", "missing_node"]
    source: Node
    target: Node
    path: list[Node]
    distance: float | None


class GraphSolver(Generic[Node]):
    """Build and analyze a simple weighted or unweighted graph.

    Each edge must be a two-item tuple ``(source, target)`` or a three-item
    tuple ``(source, target, weight)``. Unweighted edges receive weight 1.
    Parallel edges are not represented because the underlying graph is simple.
    """

    def __init__(
        self,
        edges: Iterable[tuple[Node, Node] | tuple[Node, Node, Real]],
        directed: bool = False,
    ) -> None:
        self._graph: nx.Graph | nx.DiGraph = nx.DiGraph() if directed else nx.Graph()
        for index, edge in enumerate(edges):
            if len(edge) not in (2, 3):
                raise ValueError(
                    f"Edge at index {index} must contain two nodes and an optional weight."
                )

            source, target = edge[0], edge[1]
            weight = self._normalize_weight(edge[2]) if len(edge) == 3 else 1.0
            try:
                self._graph.add_edge(source, target, weight=weight)
            except TypeError as error:
                raise TypeError(f"Nodes in edge {index} must be hashable.") from error

    @property
    def is_directed(self) -> bool:
        """Return whether this solver contains a directed graph."""
        return self._graph.is_directed()

    def adjacency_matrix(self) -> AdjacencyMatrixResult[Node]:
        """Return the adjacency matrix and the matching node ordering."""
        nodes = list(self._graph.nodes)
        matrix = nx.to_numpy_array(
            self._graph,
            nodelist=nodes,
            weight="weight",
            dtype=float,
        ).tolist()
        return {
            "nodes": nodes,
            "matrix": matrix,
            "directed": self._graph.is_directed(),
        }

    def shortest_path(self, source: Node, target: Node) -> ShortestPathResult[Node]:
        """Find a minimum-weight path using Dijkstra's algorithm.

        The result has status ``missing_node`` if either endpoint is absent,
        ``no_path`` if both nodes exist but are disconnected, and ``ok`` when a
        path is found. The distance is ``None`` when there is no path.
        """
        if source not in self._graph or target not in self._graph:
            return {
                "status": "missing_node",
                "source": source,
                "target": target,
                "path": [],
                "distance": None,
            }

        try:
            distance, path = nx.single_source_dijkstra(
                self._graph,
                source=source,
                target=target,
                weight="weight",
            )
        except nx.NetworkXNoPath:
            return {
                "status": "no_path",
                "source": source,
                "target": target,
                "path": [],
                "distance": None,
            }

        return {
            "status": "ok",
            "source": source,
            "target": target,
            "path": path,
            "distance": float(distance),
        }

    def is_tree(self) -> bool:
        """Return whether the graph is undirected, connected, and acyclic."""
        if self._graph.is_directed() or self._graph.number_of_nodes() == 0:
            return False
        return nx.is_connected(self._graph) and nx.is_forest(self._graph)

    @staticmethod
    def _normalize_weight(weight: Real) -> float:
        if isinstance(weight, bool) or not isinstance(weight, Real):
            raise TypeError("Edge weights must be real numbers.")
        try:
            normalized_weight = float(weight)
        except (OverflowError, ValueError) as error:
            raise ValueError("Edge weights must be finite non-negative numbers.") from error
        if not math.isfinite(normalized_weight) or normalized_weight < 0:
            raise ValueError("Edge weights must be finite non-negative numbers.")
        return normalized_weight