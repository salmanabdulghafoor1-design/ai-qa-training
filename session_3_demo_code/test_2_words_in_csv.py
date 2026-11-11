# The same test case, with the words in a CSV file.
# Add a row to search_words.csv and you have a new test.

import csv
from pathlib import Path

import pytest
from playwright.sync_api import expect

from helpers import cleanup_browser, initialize_browser, open_website, search_product, read_search_words


@pytest.mark.parametrize("search_word", read_search_words("search_words.csv"))
def test_search_shows_only_matching_products(search_word):
    playwright, browser, page = initialize_browser()
    try:
        open_website(page)
        search_product(page, search_word)

        product_names = page.locator('[data-test="product-name"]')
        expect(product_names.first).to_be_visible()
        expect(product_names.filter(has_not_text=search_word)).to_have_count(0)
    finally:
        cleanup_browser(playwright, browser)
