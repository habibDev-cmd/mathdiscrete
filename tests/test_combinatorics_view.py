from streamlit.testing.v1 import AppTest

COMBINATORICS_SCRIPT = "from ui.views.combinatorics import render\nrender()"


def test_permutation_form_displays_result() -> None:
    app = AppTest.from_string(COMBINATORICS_SCRIPT).run()

    app.button(key="selection_submit").click().run()

    assert not app.exception
    assert any("P(8, 3) = 336" in alert.value for alert in app.success)


def test_combination_form_displays_result() -> None:
    app = AppTest.from_string(COMBINATORICS_SCRIPT)
    app.session_state["counting_method"] = "Combination"
    app.run()

    app.button(key="selection_submit").click().run()

    assert not app.exception
    assert any("C(8, 3) = 56" in alert.value for alert in app.success)


def test_factorial_form_displays_result() -> None:
    app = AppTest.from_string(COMBINATORICS_SCRIPT).run()

    app.button(key="factorial_submit").click().run()

    assert not app.exception
    assert any("5! = 120" in alert.value for alert in app.success)


def test_pigeonhole_form_displays_guaranteed_minimum() -> None:
    app = AppTest.from_string(COMBINATORICS_SCRIPT).run()

    app.button(key="pigeonhole_submit").click().run()

    assert not app.exception
    assert any("holds **4** item(s)" in alert.value for alert in app.success)