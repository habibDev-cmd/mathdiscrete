import pytest

from core import GraphSolver


@pytest.mark.parametrize(
    ("edges", "source", "target", "expected_path", "expected_distance"),
    [
        (
            [("A", "B", 5), ("A", "C", 1), ("C", "B", 1), ("B", "D", 2)],
            "A",
            "D",
            ["A", "C", "B", "D"],
            4.0,
        ),
        (
            [("S", "A", 2), ("S", "B", 5), ("A", "B", 1), ("B", "T", 2), ("A", "T", 8)],
            "S",
            "T",
            ["S", "A", "B", "T"],
            5.0,
        ),
        (
            [("1", "2", 0.5), ("1", "3", 2), ("2", "3", 0.5), ("3", "4", 1)],
            "1",
            "4",
            ["1", "2", "3", "4"],
            2.0,
        ),
    ],
)
def test_dijkstra_returns_shortest_weighted_path(
    edges: list[tuple[str, str, float]],
    source: str,
    target: str,
    expected_path: list[str],
    expected_distance: float,
) -> None:
    solver = GraphSolver(edges)

    result = solver.shortest_path(source, target)

    assert result["status"] == "ok"
    assert result["path"] == expected_path
    assert result["distance"] == expected_distance