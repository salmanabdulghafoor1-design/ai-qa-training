import csv
from pathlib import Path

from playwright.sync_api import Page, expect, sync_playwright

SHOP_URL = "https://practicesoftwaretesting.com"
API_URL = "https://api.practicesoftwaretesting.com"


def initialize_browser():
    playwright = sync_playwright().start()
    browser = None
    try:
        browser = playwright.chromium.launch(headless=False)
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


def sort_products(page: Page, option: str):
    page.locator('[data-test="sort"]').select_option(label=option)


def read_sort_cases(csv_file_name: str):
    csv_path = Path(__file__).parent / csv_file_name
    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        return [
            {
                **row,
                "is_valid": row["is_valid"].strip().lower() == "true",
            }
            for row in csv.DictReader(csv_file)
        ]
