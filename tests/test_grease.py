import pytest

from chromhydra.hints.grease import greased_brand


@pytest.mark.parametrize(
    "major, expected",
    [
        (120, ("Not_A Brand", "8")),
        (124, ("Not-A.Brand", "99")),
        (131, ("Not_A Brand", "24")),
        (155, ("Not(A:Brand", "24")),
    ],
)
def test_matches_real_chrome(major, expected):
    assert greased_brand(major) == expected
