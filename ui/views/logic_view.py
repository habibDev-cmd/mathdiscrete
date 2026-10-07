"""Streamlit view for propositional logic analysis."""

from __future__ import annotations

import streamlit as st
from sympy import latex

from core.logic import LogicSolverError, PropositionalLogic, TruthTableRow


def _format_truth_table_rows(
    rows: tuple[TruthTableRow, ...],
) -> list[dict[str, str]]:
    """Convert truth-table rows to display-ready T/F text values."""
    formatted_rows: list[dict[str, str]] = []
    for row in rows:
        assignment = row.assignment
        formatted_rows.append(
            {
                **{name: "T" if value else "F" for name, value in assignment.items()},
                "Result": "T" if row.result else "F",
            }
        )
    return formatted_rows


def render() -> None:
    """Render an expression input, its LaTeX form, and its truth table."""
    st.title("Propositional Logic")
    st.write("Enter a Boolean expression using `and`, `or`, `not`, and `^` for XOR.")

    with st.form("propositional_logic_form"):
        expression = st.text_input("Expression", value="(p and q) or not p")
        submitted = st.form_submit_button(
            "Generate truth table",
            type="primary",
            key="logic_submit",
        )

    if not submitted:
        return

    solver = PropositionalLogic()
    try:
        symbolic_expression, _ = solver.parse(expression)
        result = solver.truth_table(expression)
    except LogicSolverError as error:
        st.error(str(error))
        return

    st.subheader("Formula")
    st.latex(latex(symbolic_expression))
    st.metric("Classification", result.classification.value.title())

    st.subheader("Truth Table")
    rows = _format_truth_table_rows(result.rows)
    st.dataframe(
        rows,
        hide_index=True,
        width="stretch",
        alt="Truth table with T and F values for each variable assignment.",
    )