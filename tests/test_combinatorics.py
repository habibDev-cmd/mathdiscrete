import pytest

from core import CombinatoricsSolver


@pytest.mark.parametrize(
    ("n", "r", "expected_permutations", "expected_combinations"),
    [
        (5, 2, 20, 10),
        (6, 3, 120, 20),
        (8, 0, 1, 1),
    ],
)
def test_permutations_and_combinations(
    n: int,
    r: int,
    expected_permutations: int,
    expected_combinations: int,
) -> None:
    solver = CombinatoricsSolver()

    permutation = solver.permutation(n, r)
    combination = solver.combination(n, r)

    assert permutation.result == expected_permutations
    assert combination.result == expected_combinations
    assert len(permutation.steps) == 3
    assert len(combination.steps) == 3


def test_combination_steps_show_formula_substitution_and_expansion() -> None:
    result = CombinatoricsSolver().combination(5, 2)

    assert result.steps == [
        r"C(n, r) = \frac{n!}{r!(n-r)!}",
        r"C(5, 2) = \frac{5!}{2!(5-2)!} = \frac{5!}{2!3!}",
        r"C(5, 2) = \frac{5 \times 4}{2 \times 1} = 10",
    ]