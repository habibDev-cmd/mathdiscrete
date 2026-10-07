"""Streamlit tools for common combinatorics calculations."""

from __future__ import annotations

import streamlit as st

from core.combinatorics import CombinatoricsSolver


def render() -> None:
    """Render permutation, combination, factorial, and pigeonhole tools."""
    st.title("Combinatorics")
    st.write("Calculate exact counting quantities for finite sets and selections.")

    solver = CombinatoricsSolver()
    permutation_tab, factorial_tab, pigeonhole_tab = st.tabs(
        ["Permutations and combinations", "Factorial", "Pigeonhole principle"]
    )

    with permutation_tab:
        st.subheader("Selections from a finite set")
        st.latex(r"P(n,r)=\frac{n!}{(n-r)!}\qquad C(n,r)=\frac{n!}{r!(n-r)!}")
        with st.form("combinatorics_selection_form"):
            method = st.selectbox(
                "Counting method",
                ["Permutation", "Combination"],
                key="counting_method",
            )
            n = st.number_input("Number of available items (n)", min_value=0, value=8, step=1)
            r = st.number_input("Number selected (r)", min_value=0, value=3, step=1)
            submitted = st.form_submit_button(
                "Calculate",
                type="primary",
                key="selection_submit",
            )

        if submitted:
            try:
                result = (
                    solver.permutations(int(n), int(r))
                    if method == "Permutation"
                    else solver.combinations(int(n), int(r))
                )
            except (TypeError, ValueError) as error:
                st.error(str(error))
            else:
                notation = "P" if method == "Permutation" else "C"
                st.success(f"{notation}({int(n)}, {int(r)}) = {result:,}")

    with factorial_tab:
        st.subheader("Factorial")
        st.latex(r"n! = n\times(n-1)\times\cdots\times2\times1,\qquad 0!=1")
        with st.form("combinatorics_factorial_form"):
            factorial_n = st.number_input(
                "Non-negative integer (n)",
                min_value=0,
                max_value=1000,
                value=5,
                step=1,
            )
            factorial_submitted = st.form_submit_button(
                "Calculate factorial",
                type="primary",
                key="factorial_submit",
            )

        if factorial_submitted:
            try:
                result = solver.factorial(int(factorial_n))
            except (TypeError, ValueError) as error:
                st.error(str(error))
            else:
                st.success(f"{int(factorial_n)}! = {result:,}")

    with pigeonhole_tab:
        st.subheader("Pigeonhole principle")
        st.latex(r"\left\lceil\frac{N}{M}\right\rceil")
        st.caption("With N items placed into M non-empty containers, at least one contains this many items.")
        with st.form("combinatorics_pigeonhole_form"):
            items = st.number_input("Number of items (N)", min_value=0, value=10, step=1)
            containers = st.number_input(
                "Number of containers (M)",
                min_value=1,
                value=3,
                step=1,
            )
            pigeonhole_submitted = st.form_submit_button(
                "Find guaranteed minimum",
                type="primary",
                key="pigeonhole_submit",
            )

        if pigeonhole_submitted:
            try:
                minimum = solver.pigeonhole_minimum(int(items), int(containers))
            except (TypeError, ValueError) as error:
                st.error(str(error))
            else:
                st.success(
                    f"At least one container holds **{minimum}** item(s) "
                    f"when {int(items)} items are placed into {int(containers)} containers."
                )