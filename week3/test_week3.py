from decimal import Decimal

import pytest
from playwright.sync_api import expect

from helpers import (
    SORT_OPTIONS,
    cleanup_api,
    cleanup_browser,
    initialize_api,
    initialize_browser,
    open_website,
    read_search_words,
    search_product,
    sort_option_value,
    sort_products,
)

INVALID_SORT_OPTIONS = ("Unsupported sort", "Price ascending")


@pytest.mark.parametrize("search_word", read_search_words("data.csv"))
def test_search_shows_matching_products(search_word):
    playwright, browser, page = initialize_browser()
    try:
        open_website(page)
        search_product(page, search_word)

        product_names = page.locator('[data-test="product-name"]')
        expect(product_names.first).to_be_visible()
        expect(product_names.filter(has_not_text=search_word)).to_have_count(0)
    finally:
        cleanup_browser(playwright, browser)


@pytest.mark.parametrize("sort_option", SORT_OPTIONS)
def test_sort_products_by_valid_option(sort_option):
    playwright, browser, page = initialize_browser()
    try:
        open_website(page)
        sort_products(page, sort_option)

        sort_control = page.locator('[data-test="sort"]')
        expect(sort_control).to_have_value(SORT_OPTIONS[sort_option])
        page.wait_for_load_state("networkidle")

        if sort_option.startswith("Name"):
            actual_values = [
                name.casefold()
                for name in page.locator('[data-test="product-name"]').all_inner_texts()
            ]
            expected_values = sorted(
                actual_values, reverse=sort_option.endswith("(Z - A)")
            )
        elif sort_option.startswith("Price"):
            actual_values = [
                Decimal(price.replace("$", "").replace(",", ""))
                for price in page.locator('[data-test="product-price"]').all_inner_texts()
            ]
            expected_values = sorted(
                actual_values, reverse=sort_option.endswith("(High - Low)")
            )
        else:
            actual_values = [
                badge.locator(".active").inner_text().strip()
                for badge in page.locator(
                    '[data-test="co2-rating-badge"]'
                ).all()
            ]
            expected_values = sorted(
                actual_values, reverse=sort_option.endswith("(E - A)")
            )

        assert actual_values == expected_values, (
            f"Products were not sorted as {sort_option}: {actual_values}"
        )
    finally:
        cleanup_browser(playwright, browser)


@pytest.mark.parametrize("sort_option", INVALID_SORT_OPTIONS)
def test_sort_option_rejects_invalid_values(sort_option):
    with pytest.raises(ValueError, match="Unsupported sort option"):
        sort_option_value(sort_option)


@pytest.mark.parametrize("search_word", read_search_words("data.csv"))
def test_search_api_matches_products_shown_on_page(search_word):
    playwright, api = initialize_api()
    try:
        response = api.get("/products/search", params={"q": search_word})
        assert response.status == 200, (
            f"API returned status {response.status} for search '{search_word}'"
        )

        products = response.json()["data"]
        assert products, f"No API products found for '{search_word}'"

        api_names = []
        for product in products:
            assert {"id", "name", "price"} <= product.keys(), (
                f"API product is missing id, name, or price: {product}"
            )
            assert isinstance(product["id"], str), "product id should be text"
            assert isinstance(product["name"], str), "product name should be text"
            assert isinstance(product["price"], (int, float)), (
                "product price should be numeric"
            )
            assert search_word.casefold() in product["name"].casefold(), (
                f"'{product['name']}' doesn't match '{search_word}'"
            )
            api_names.append(product["name"])
    finally:
        cleanup_api(playwright, api)

    playwright, browser, page = initialize_browser()
    try:
        open_website(page)
        search_product(page, search_word)

        page_names = page.locator('[data-test="product-name"]')
        expect(page_names).to_have_text(api_names)
    finally:
        cleanup_browser(playwright, browser)
