from core.logic import PropositionalLogic
from ui.views.logic_view import _format_truth_table_rows


LOGIC_SCRIPT = "from ui.views.logic_view import render\nrender()"


def test_truth_table_display_uses_text_values() -> None:
    result = PropositionalLogic().truth_table("p and q")

    rows = _format_truth_table_rows(result.rows)

    assert rows == [
        {"p": "F", "q": "F", "Result": "F"},
        {"p": "F", "q": "T", "Result": "F"},
        {"p": "T", "q": "F", "Result": "F"},
        {"p": "T", "q": "T", "Result": "T"},
    ]


def test_rendered_dataframe_contains_text_values() -> None:
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_string(LOGIC_SCRIPT).run()
    app.button(key="logic_submit").click().run()

    assert not app.exception
    displayed_values = app.dataframe[0].value.to_numpy().flatten()
    assert set(displayed_values) == {"T", "F"}