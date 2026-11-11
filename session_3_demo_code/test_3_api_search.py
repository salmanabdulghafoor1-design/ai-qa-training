# The same search, asked of the API directly with Playwright. No browser, so it is quick.
# The words come from search_words.csv, the same file the page test uses.

import pytest
from playwright.sync_api import expect

from helpers import cleanup_api, initialize_api, read_search_words


@pytest.mark.parametrize("search_word", read_search_words("search_words.csv"))
def test_search_api_returns_only_matching_products(search_word):
    playwright, api = initialize_api()
    try:
        response = api.get("/products/search", params={"q": search_word})
        expect(response).to_be_ok()

        products = response.json()["data"]
        assert len(products) > 0, f"no products found for '{search_word}'"

        for product in products:
            has_fields = "name" in product and "price" in product
            assert has_fields, f"missing a field: {product}"
            name = product["name"]
            price = product["price"]

            assert isinstance(name, str), "name should be text"
            assert isinstance(price, (int, float)), "price should be a number"

            matches_search_word = search_word.strip().lower() in name.lower()
            assert matches_search_word, f"'{name}' doesn't match '{search_word}'"
    finally:
        cleanup_api(playwright, api)
