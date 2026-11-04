import re
from playwright.sync_api import Page, expect, sync_playwright

BASE_URL = "https://practicesoftwaretesting.com"


def open_home_page(page: Page):
    page.goto(BASE_URL)
    expect(page).to_have_url(BASE_URL + "/")
    expect(page.get_by_role("heading", name="Products")).to_be_visible()


def search_product(page: Page, query: str, use_enter: bool = False):
    search = page.get_by_placeholder("Search products")
    search.fill(query)
    if use_enter:
        search.press("Enter")
    else:
        page.get_by_role("button", name="Search").click()
    expect(page.locator("h5")).to_contain_text(query)


def sort_products(page: Page, option: str):
    page.locator("select").select_option(label=option)


def add_first_product_to_cart(page: Page):
    page.locator("button").filter(has_text="Add to cart").first.click()


def open_cart(page: Page):
    page.get_by_role("link", name="Cart").click()
    expect(page).to_have_url(re.compile(r"basket|cart", re.I))


def remove_first_cart_item(page: Page):
    page.locator("button").filter(has_text="Remove").first.click()


def submit_contact_form(page: Page, first_name: str, last_name: str, email: str, subject: str, message: str):
    page.goto(BASE_URL + "/contact")
    page.get_by_label("First name").fill(first_name)
    page.get_by_label("Last name").fill(last_name)
    page.get_by_label("Email").fill(email)
    page.get_by_label("Subject").fill(subject)
    page.get_by_label("Message").fill(message)
    page.get_by_role("button", name="Send").click()


def test_search_by_clicking_search_button():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            open_home_page(page)
            search_product(page, "Pliers", use_enter=False)
        finally:
            browser.close()


def test_search_by_pressing_enter():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            open_home_page(page)
            search_product(page, "Pliers", use_enter=True)
        finally:
            browser.close()


def test_sort_by_price_low_to_high():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            open_home_page(page)
            sort_products(page, "Price: Low to High")
            expect(page.locator("select")).to_have_value("price-asc")
        finally:
            browser.close()


def test_sort_by_price_high_to_low():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            open_home_page(page)
            sort_products(page, "Price: High to Low")
            expect(page.locator("select")).to_have_value("price-desc")
        finally:
            browser.close()


def test_add_product_to_cart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            open_home_page(page)
            add_first_product_to_cart(page)
            expect(page.locator("text=Cart")).to_be_visible()
        finally:
            browser.close()


def test_remove_product_from_cart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            open_home_page(page)
            add_first_product_to_cart(page)
            open_cart(page)
            remove_first_cart_item(page)
            expect(page.locator("text=Your cart is empty")).to_be_visible()
        finally:
            browser.close()


def test_submit_valid_contact_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            submit_contact_form(page, "Jane", "Doe", "jane@example.com", "Product inquiry", "Need product details")
            expect(page.locator("text=Thanks for contacting us")).to_be_visible()
        finally:
            browser.close()


def test_submit_invalid_contact_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            submit_contact_form(page, "Jane", "Doe", "invalid-email", "Product inquiry", "Need product details")
            expect(page.locator("text=Please enter a valid email")).to_be_visible()
        finally:
            browser.close()

if __name__ == "__main__":
    test_search_by_clicking_search_button()
    test_search_by_pressing_enter()
    test_sort_by_price_low_to_high()
    test_sort_by_price_high_to_low()
    test_add_product_to_cart()
    test_remove_product_from_cart()
    test_submit_valid_contact_form()
    test_submit_invalid_contact_form()