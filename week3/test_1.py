from decimal import Decimal

import pytest
from playwright.sync_api import Error as PlaywrightError, expect

from helpers import (
    cleanup_browser,
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
    playwright, browser, page = initialize_browser()
    try:
        open_website(page)
        sort_control = page.locator('[data-test="sort"]')
        if not sort_case["is_valid"]:
            with pytest.raises(PlaywrightError):
                sort_products(page, sort_case["sort_option"])
            return

        sort_products(page, sort_case["sort_option"])
        expect(sort_control).to_have_value(sort_case["sort_value"])
        page.wait_for_load_state("networkidle")

        if sort_case["sort_type"] == "name":
            actual_values = [
                name.casefold()
                for name in page.locator('[data-test="product-name"]').all_inner_texts()
            ]
        elif sort_case["sort_type"] == "price":
            actual_values = [
                Decimal(price.replace("$", "").replace(",", ""))
                for price in page.locator('[data-test="product-price"]').all_inner_texts()
            ]
        elif sort_case["sort_type"] == "co2":
            actual_values = [
                badge.locator(".active").inner_text().strip()
                for badge in page.locator(
                    '[data-test="co2-rating-badge"]'
                ).all()
            ]
        else:
            pytest.fail(f"Unknown sort type in data.csv: {sort_case['sort_type']}")

        expected_values = sorted(
            actual_values, reverse=sort_case["direction"] == "desc"
        )
        assert actual_values == expected_values, (
            f"Products were not sorted as {sort_case['sort_option']}: {actual_values}"
        )
    finally:
        cleanup_browser(playwright, browser)
