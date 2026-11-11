# One test case: search the products. It runs once for each word in the list.

import pytest
from playwright.sync_api import expect

from helpers import cleanup_browser, initialize_browser, open_website, search_product

@pytest.mark.parametrize("search_word", ["hammer", "pliers", "saw", "drill"])
def test_search_shows_only_matching_products(search_word):
    playwright, browser, page = initialize_browser()
    try:
        open_website(page)
        search_product(page, search_word)

        product_names = page.locator('[data-test="product-name"]')
        # print product names for debugging
        #print(product_names.all())
        expect(product_names.first).to_be_visible()
        expect(product_names.filter(has_not_text=search_word)).to_have_count(0)
    finally:
        cleanup_browser(playwright, browser)
