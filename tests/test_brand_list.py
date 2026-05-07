import pytest

from chromhydra.hints.brand_list import brand_list


@pytest.mark.parametrize(
    "version, order",
    [
        ("120.0.6099.109", ["Not_A Brand", "Chromium", "Google Chrome"]),
        ("124.0.6367.60", ["Chromium", "Google Chrome", "Not-A.Brand"]),
        ("131.0.6778.86", ["Google Chrome", "Chromium", "Not_A Brand"]),
        ("155.0.8059.85", ["Google Chrome", "Chromium", "Not(A:Brand"]),
    ],
)
def test_order_matches_real_chrome(version, order):
    assert [item["brand"] for item in brand_list(version)] == order


def test_versions_match_captured_chrome_155():
    assert brand_list("155.0.8059.85") == [
        {"brand": "Google Chrome", "version": "155", "full_version": "155.0.8059.85"},
        {"brand": "Chromium", "version": "155", "full_version": "155.0.8059.85"},
        {"brand": "Not(A:Brand", "version": "24", "full_version": "24.0.0.0"},
    ]


def test_custom_product():
    assert "Brave" in [item["brand"] for item in brand_list("155.0.1.2", "Brave")]
