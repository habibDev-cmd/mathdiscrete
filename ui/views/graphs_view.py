"""Streamlit graph visualization and shortest-path view."""

from __future__ import annotations

import math
from collections.abc import Hashable
from numbers import Real

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

from core.graphs import GraphSolver


ParsedEdge = tuple[str, str] | tuple[str, str, float]


def _parse_edges(edge_text: str) -> list[ParsedEdge]:
    """Parse one comma-separated edge per line with an optional weight."""
    parsed_edges: list[ParsedEdge] = []
    for line_number, raw_line in enumerate(edge_text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue

        parts = [part.strip() for part in line.split(",")]
        if len(parts) not in (2, 3) or not parts[0] or not parts[1]:
            raise ValueError(
                f"Line {line_number} must use the format `Node A,Node B` "
                "or `Node A,Node B,Weight`."
            )

        source, target = parts[0], parts[1]
        if len(parts) == 2:
            parsed_edges.append((source, target))
            continue

        try:
            weight = float(parts[2])
        except ValueError as error:
            raise ValueError(f"Line {line_number} has a non-numeric edge weight.") from error
        if not math.isfinite(weight) or weight < 0:
            raise ValueError(f"Line {line_number} weight must be finite and non-negative.")
        parsed_edges.append((source, target, weight))

    if not parsed_edges:
        raise ValueError("Enter at least one edge to build a graph.")
    return parsed_edges


def _format_node(node: Hashable) -> str:
    """Convert a graph node to a display label."""
    return str(node)


def _draw_graph(
    graph: nx.Graph,
    highlighted_path: list[str] | None = None,
) -> plt.Figure:
    """Render a weighted graph and optionally emphasize a shortest path."""
    figure, axis = plt.subplots(figsize=(10, 6), layout="constrained")
    positions = nx.spring_layout(graph, seed=23, weight="weight")
    path = highlighted_path or []
    highlighted_nodes = set(path)
    highlighted_edges = set(zip(path, path[1:]))

    node_colors = [
        "#e66c4f" if node in highlighted_nodes else "#147d78"
        for node in graph.nodes
    ]
    edge_colors = [
        "#e66c4f"
        if (source, target) in highlighted_edges or (target, source) in highlighted_edges
        else "#8b9b98"
        for source, target in graph.edges
    ]
    edge_widths = [
        3.0
        if (source, target) in highlighted_edges or (target, source) in highlighted_edges
        else 1.5
        for source, target in graph.edges
    ]

    nx.draw_networkx_nodes(
        graph,
        positions,
        node_color=node_colors,
        node_size=1000,
        edgecolors="#173a39",
        linewidths=1.2,
        ax=axis,
    )
    nx.draw_networkx_labels(
        graph,
        positions,
        labels={node: _format_node(node) for node in graph.nodes},
        font_color="white",
        font_weight="bold",
        ax=axis,
    )
    nx.draw_networkx_edges(
        graph,
        positions,
        edge_color=edge_colors,
        width=edge_widths,
        ax=axis,
    )
    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=nx.get_edge_attributes(graph, "weight"),
        font_color="#273b39",
        ax=axis,
    )
    axis.set_axis_off()
    return figure


def render() -> None:
    """Render weighted graph input, visualization, and Dijkstra controls."""
    st.title("Graph Theory")
    st.write("Enter one edge per line as `A,B,5`. Weights are optional and default to 1.")

    edge_text = st.text_area(
        "Edges",
        value="A,B,5\nA,C,1\nC,B,1\nB,D,2",
        height=150,
        help="Use `Source,Target,Weight`; omit the weight for an unweighted edge.",
    )

    try:
        edges = _parse_edges(edge_text)
        solver = GraphSolver(edges)
    except (TypeError, ValueError) as error:
        st.error(str(error))
        return

    graph = nx.Graph()
    for edge in edges:
        source, target = edge[0], edge[1]
        weight = edge[2] if len(edge) == 3 else 1.0
        graph.add_edge(source, target, weight=weight)

    nodes = list(graph.nodes)
    st.subheader("Graph Visualization")
    figure = _draw_graph(graph)
    st.pyplot(figure, use_container_width=True)
    plt.close(figure)

    st.subheader("Shortest Path")
    source_column, target_column = st.columns(2)
    with source_column:
        source = st.selectbox("Start node", nodes, key="graph_start_node")
    with target_column:
        target = st.selectbox(
            "End node",
            nodes,
            index=min(1, len(nodes) - 1),
            key="graph_end_node",
        )

    if st.button("Find shortest path", type="primary"):
        result = solver.shortest_path(source, target)
        if result["status"] == "ok":
            path_text = " → ".join(_format_node(node) for node in result["path"])
            st.success(f"Shortest path: {path_text} · Total weight: {result['distance']:g}")
            highlighted_figure = _draw_graph(graph, result["path"])
            st.pyplot(highlighted_figure, use_container_width=True)
            plt.close(highlighted_figure)
        elif result["status"] == "no_path":
            st.warning("No path exists between the selected nodes.")
        else:
            st.error("One or both selected nodes are not present in the graph.")