# The API says which products match. Does the page show the same ones?
# The words come from search_words.csv, the same file the other tests use.

import pytest
from playwright.sync_api import expect

from helpers import (
    cleanup_api,
    cleanup_browser,
    initialize_api,
    initialize_browser,
    open_website,
    read_search_words,
    search_product,
)


@pytest.mark.parametrize("search_word", read_search_words("search_words.csv"))
def test_page_shows_the_products_the_api_finds(search_word):
    playwright, api = initialize_api()
    try:
        response = api.get("/products/search", params={"q": search_word})
        expect(response).to_be_ok()

        product_names_from_api = []
        for product in response.json()["data"]:
            product_names_from_api.append(product["name"])
    except Exception as e:
        print(f"Error occurred while fetching products from API: {e}")
    finally:
        cleanup_api(playwright, api)

    playwright, browser, page = initialize_browser()
    try:
        open_website(page)
        search_product(page, search_word)

        expect(page.locator('[data-test="product-name"]')).to_have_text(
            product_names_from_api
        )
    finally:
        cleanup_browser(playwright, browser)
