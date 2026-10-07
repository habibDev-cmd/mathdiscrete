"""Main Streamlit entry point for the MathDiscrete application."""

from __future__ import annotations

from importlib import import_module, util
from types import ModuleType
from typing import Final

import streamlit as st


class MathDiscreteApplication:
    """Configure the application shell and route navigation to view modules."""

    VIEW_MODULES: Final[dict[str, str]] = {
        "Propositional Logic": "ui.views.logic_view",
        "Set Theory": "ui.views.sets_view",
        "Combinatorics": "ui.views.combinatorics",
        "Graph Theory": "ui.views.graphs_view",
    }

    def run(self) -> None:
        """Render the shared application shell and selected view."""
        st.set_page_config(
            page_title="MathDiscrete | Discrete Mathematics",
            page_icon="∴",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        st.sidebar.title("MathDiscrete")
        st.sidebar.caption("Discrete Mathematics Solver")
        selected_view = st.sidebar.radio("Navigation", tuple(self.VIEW_MODULES))

        self._render_view(selected_view)

    def _render_view(self, selected_view: str) -> None:
        module_name = self.VIEW_MODULES[selected_view]
        if util.find_spec(module_name) is None:
            st.title(selected_view)
            st.info(f"The {selected_view} view has not been implemented yet.")
            return

        view_module: ModuleType = import_module(module_name)
        render_view = getattr(view_module, "render", None)
        if not callable(render_view):
            st.error(f"The {selected_view} view must define a callable render() function.")
            return

        render_view()


def main() -> None:
    """Start the Streamlit application."""
    MathDiscreteApplication().run()


if __name__ == "__main__":
    main()