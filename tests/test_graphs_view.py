import pytest

from ui.views.graphs_view import _parse_edges


def test_parse_weighted_and_unweighted_edges() -> None:
    assert _parse_edges("A,B,5\nB,C") == [("A", "B", 5.0), ("B", "C")]


def test_parse_edges_skips_blank_lines() -> None:
    assert _parse_edges("\n A, B, 2.5 \n\n") == [("A", "B", 2.5)]


@pytest.mark.parametrize("edge_text", ["A,B,-1", "A,B,inf", "A,B,weight"])
def test_parse_edges_rejects_invalid_weights(edge_text: str) -> None:
    with pytest.raises(ValueError):
        _parse_edges(edge_text)