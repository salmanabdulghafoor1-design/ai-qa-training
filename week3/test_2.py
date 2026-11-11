import pytest

from helpers import cleanup_api, initialize_api, read_sort_cases


@pytest.mark.parametrize(
    "sort_case",
    read_sort_cases("data.csv"),
    ids=lambda sort_case: sort_case["sort_option"],
)
def test_sort_products_api(sort_case):
    playwright, api = initialize_api()
    try:
        response = api.get("/products", params={"sort": sort_case["sort_value"]})

        if not sort_case["is_valid"]:
            assert response.status >= 400, (
                f"API accepted invalid sort option {sort_case['sort_option']!r}"
            )
            return

        assert response.status == 200, (
            f"API returned status {response.status} for {sort_case['sort_option']}"
        )
        products = response.json()["data"]
        assert products, f"API returned no products for {sort_case['sort_option']}"
        for product in products:
            assert {"id", "name", "price", "co2_rating"} <= product.keys(), (
                f"API product is missing sorting fields: {product}"
            )

        if sort_case["sort_type"] == "name":
            actual_values = [product["name"].casefold() for product in products]
        elif sort_case["sort_type"] == "price":
            actual_values = [float(product["price"]) for product in products]
        elif sort_case["sort_type"] == "co2":
            actual_values = [product["co2_rating"] for product in products]
        else:
            pytest.fail(f"Unknown sort type in data.csv: {sort_case['sort_type']}")

        expected_values = sorted(
            actual_values, reverse=sort_case["direction"] == "desc"
        )
        assert actual_values == expected_values, (
            f"API products were not sorted as {sort_case['sort_option']}: "
            f"{actual_values}"
        )
    finally:
        cleanup_api(playwright, api)
