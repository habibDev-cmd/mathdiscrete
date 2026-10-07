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

    assert solver.permutations(n, r) == expected_permutations
    assert solver.combinations(n, r) == expected_combinations