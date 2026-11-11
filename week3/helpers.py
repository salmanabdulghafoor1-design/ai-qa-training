import csv
from pathlib import Path

from playwright.sync_api import Page, expect, sync_playwright

SHOP_URL = "https://practicesoftwaretesting.com"
API_URL = "https://api.practicesoftwaretesting.com"

SORT_OPTIONS = {
    "Name (A - Z)": "name,asc",
    "Name (Z - A)": "name,desc",
    "Price (High - Low)": "price,desc",
    "Price (Low - High)": "price,asc",
    "CO₂ Rating (A - E)": "co2_rating,asc",
    "CO₂ Rating (E - A)": "co2_rating,desc",
}


def initialize_browser():
    playwright = sync_playwright().start()
    browser = None
    try:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        return playwright, browser, page
    except Exception:
        cleanup_browser(playwright, browser)
        raise


def cleanup_browser(playwright, browser):
    try:
        if browser is not None:
            browser.close()
    finally:
        playwright.stop()


def initialize_api():
    playwright = sync_playwright().start()
    api = None
    try:
        api = playwright.request.new_context(base_url=API_URL)
        return playwright, api
    except Exception:
        cleanup_api(playwright, api)
        raise


def cleanup_api(playwright, api):
    try:
        if api is not None:
            api.dispose()
    finally:
        playwright.stop()


def open_website(page: Page):
    page.goto(SHOP_URL, wait_until="domcontentloaded")
    expect(page.locator('[data-test="product-name"]').first).to_be_visible()


def search_product(page: Page, search_word: str):
    page.locator('[data-test="search-query"]').fill(search_word)
    page.locator('[data-test="search-query"]').press("Enter")


def sort_option_value(option: str) -> str:
    try:
        return SORT_OPTIONS[option]
    except KeyError as error:
        raise ValueError(f"Unsupported sort option: {option}") from error


def sort_products(page: Page, option: str):
    page.locator('[data-test="sort"]').select_option(value=sort_option_value(option))


def read_search_words(csv_file_name: str):
    csv_path = Path(__file__).parent / csv_file_name
    search_words = []
    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        for row in csv.DictReader(csv_file):
            search_words.append(row["search_word"])
    return search_words
