"""Streamlit view for propositional logic analysis."""

from __future__ import annotations

import streamlit as st
from sympy import latex

from core.logic import LogicSolverError, PropositionalLogic


def render() -> None:
    """Render an expression input, its LaTeX form, and its truth table."""
    st.title("Propositional Logic")
    st.write("Enter a Boolean expression using `and`, `or`, `not`, and `^` for XOR.")

    with st.form("propositional_logic_form"):
        expression = st.text_input("Expression", value="(p and q) or not p")
        submitted = st.form_submit_button("Generate truth table", type="primary")

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
    rows = [
        {**row.assignment, "Result": row.result}
        for row in result.rows
    ]
    st.dataframe(rows, hide_index=True, use_container_width=True)