"""Streamlit view for basic set operations."""

from __future__ import annotations

from collections.abc import Hashable

import streamlit as st

from core.sets_theory import SetTheorySolver


def _parse_values(value: str) -> list[str]:
    """Parse comma-separated input into trimmed, non-empty string values."""
    return [item.strip() for item in value.split(",") if item.strip()]


def _format_values(values: set[Hashable]) -> str:
    """Format set results in a stable order for readable Markdown output."""
    return ", ".join(f"`{value}`" for value in sorted(values, key=repr)) or "∅"


def render() -> None:
    """Render inputs for two sets and their requested operations."""
    st.title("Set Theory")
    st.write("Enter comma-separated values. Repeated values are treated as one set member.")

    with st.form("set_theory_form"):
        column_a, column_b = st.columns(2)
        with column_a:
            values_a = st.text_input("Set A", value="1, 2, 3")
        with column_b:
            values_b = st.text_input("Set B", value="2, 3, 4")
        submitted = st.form_submit_button("Calculate set operations", type="primary")

    if not submitted:
        return

    try:
        solver = SetTheorySolver(_parse_values(values_a), _parse_values(values_b))
        union = solver.union()
        intersection = solver.intersection()
        cartesian_product = solver.cartesian_product()
    except (TypeError, ValueError) as error:
        st.error(str(error))
        return

    st.subheader("Results")
    st.markdown(f"**Union (A ∪ B):** {{{_format_values(union)}}}")
    st.markdown(f"**Intersection (A ∩ B):** {{{_format_values(intersection)}}}")
    product_values = sorted(cartesian_product, key=repr)
    formatted_product = ", ".join(f"`({left}, {right})`" for left, right in product_values) or "∅"
    st.markdown(f"**Cartesian Product (A × B):** {formatted_product}")