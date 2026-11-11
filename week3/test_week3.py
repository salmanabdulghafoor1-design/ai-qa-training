from decimal import Decimal

import pytest
from playwright.sync_api import Error as PlaywrightError, expect

from helpers import (
    API_URL,
    cleanup_api,
    cleanup_browser,
    initialize_api,
    initialize_browser,
    open_website,
    read_sort_cases,
    sort_products,
)


@pytest.mark.parametrize(
    "sort_case",
    read_sort_cases("data.csv"),
    ids=lambda sort_case: sort_case["sort_option"],
)
def test_sort_products(sort_case):
    if not sort_case["is_valid"]:
        api_playwright, api = initialize_api()
        try:
            response = api.get(
                "/products", params={"sort": sort_case["sort_value"]}
            )
            assert response.status >= 400, (
                f"API accepted invalid sort option {sort_case['sort_option']!r}"
            )
        finally:
            cleanup_api(api_playwright, api)

    playwright, browser, page = initialize_browser()
    try:
        open_website(page)
        sort_control = page.locator('[data-test="sort"]')
        if not sort_case["is_valid"]:
            with pytest.raises(PlaywrightError):
                sort_products(page, sort_case["sort_option"])
            return

        with page.expect_response(
            lambda response: (
                response.url.split("?")[0].rstrip("/") == f"{API_URL}/products"
            )
        ) as response_info:
            sort_products(page, sort_case["sort_option"])
        api_response = response_info.value
        assert api_response.status == 200, (
            f"API returned status {api_response.status} "
            f"for {sort_case['sort_option']}"
        )
        products = api_response.json()["data"]
        assert products, f"API returned no products for {sort_case['sort_option']}"
        for product in products:
            assert {"id", "name", "price", "co2_rating"} <= product.keys(), (
                f"API product is missing sorting fields: {product}"
            )

        if sort_case["sort_type"] == "name":
            api_values = [product["name"].casefold() for product in products]
        elif sort_case["sort_type"] == "price":
            api_values = [Decimal(str(product["price"])) for product in products]
        elif sort_case["sort_type"] == "co2":
            api_values = [product["co2_rating"] for product in products]
        else:
            pytest.fail(f"Unknown sort type in data.csv: {sort_case['sort_type']}")

        expect(sort_control).to_have_value(sort_case["sort_value"])
        page.wait_for_load_state("networkidle")

        if sort_case["sort_type"] == "name":
            ui_values = [
                name.casefold()
                for name in page.locator('[data-test="product-name"]').all_inner_texts()
            ]
        elif sort_case["sort_type"] == "price":
            ui_values = [
                Decimal(price.replace("$", "").replace(",", ""))
                for price in page.locator('[data-test="product-price"]').all_inner_texts()
            ]
        else:
            ui_values = [
                badge.locator(".active").inner_text().strip()
                for badge in page.locator(
                    '[data-test="co2-rating-badge"]'
                ).all()
            ]

        expected_values = sorted(
            ui_values, reverse=sort_case["direction"] == "desc"
        )
        assert ui_values == expected_values, (
            f"UI products were not sorted as {sort_case['sort_option']}: {ui_values}"
        )
        assert api_values == expected_values, (
            f"API products were not sorted as {sort_case['sort_option']}: {api_values}"
        )
        assert ui_values == api_values, (
            f"UI and API results differ for {sort_case['sort_option']}: "
            f"UI={ui_values}, API={api_values}"
        )
    finally:
        cleanup_browser(playwright, browser)
