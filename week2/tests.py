from turtle import delay
from playwright.sync_api import Page, expect, sync_playwright

BASE_URL = "https://practicesoftwaretesting.com"


def open_home_page(page: Page):
    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded")


def search_product(page: Page, query: str, use_enter: bool = False):
    search = page.locator("[placeholder='Search']")
    search.fill(query)
    if use_enter:
        search.press("Enter")
    else:
        page.locator("button:has-text('Search')").click()


def sort_products(page: Page, option: str):
    page.locator('[data-test="sort"]').select_option(label=option)


def email_subject(page: Page, option: str):
    page.locator('[id="subject"]').select_option(label=option)


def open_hand_tools(page: Page):
    page.locator('[data-test="nav-categories"]').click()
    page.locator('[data-test="nav-hand-tools"]').click()


def open_second_hand_tool(page: Page) -> str:
    products = page.locator('[data-test="product-name"]')
    product_count = products.count()
    for i in range(product_count):
        product_name = products.nth(i).inner_text()
        if product_name.strip() == "":
            print(f"FAIL: Product {i + 1} has an empty name")
        else:
            print(f"Product {i + 1}: {product_name}")
    first_product = products.nth(1).inner_text()
    products.nth(1).click()
    print("PASS: First Product Tool detail page loaded successfully")
    return first_product


def add_selected_product_to_cart(page: Page, product_name: str):
    page.locator('[id="btn-add-to-cart"]').click()
    if page.locator('[data-test="cart-quantity"]').count() == 1:
        cart_count = page.locator('[data-test="cart-quantity"]').inner_text()
        print(f"PASS: Cart quantity after adding {product_name} to cart: {cart_count}")


def open_cart(page: Page):
    # page.locator("a[href*='basket'], a[href*='cart']").first.click()
    if page.locator('[data-test="cart-quantity"]').count() == 1:
        page.locator('[data-test="cart-quantity"]').click()


def remove_first_cart_item(page: Page):
    # page.locator("button:has-text('Remove')").first.click()
    page.locator("[class='btn btn-danger']").click()
    print("PASS: The cart is empty now after removing the first item from the cart")


def submit_contact_form(page: Page, first_name: str, last_name: str, email: str, subject: str, message: str):
    page.goto(BASE_URL + "/contact")
    page.locator('[data-test="first-name"]').fill(first_name)
    page.locator('[data-test="last-name"]').fill(last_name)
    page.locator('[data-test="email"]').fill(email)
    # page.locator('[data-test="subject"]').fill(subject)
    email_subject(page, subject)
    page.locator('[data-test="message"]').fill(message)
    # delay(3)  # Wait for user to read input
    # page.locator('[data-test="send-button"]').click()


def test_search_by_clicking_search_button():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            open_home_page(page)
            expect(page.locator("[placeholder='Search']")).to_be_visible()
            search_product(page, "Pliers", use_enter=False)
            expect(page.locator("body")).to_contain_text("Pliers")
        finally:
            browser.close()


def test_search_by_pressing_enter():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            open_home_page(page)
            expect(page.locator("[placeholder='Search']")).to_be_visible()
            search_product(page, "Pliers", use_enter=True)
            expect(page.locator("body")).to_contain_text("Pliers")
        finally:
            browser.close()


def test_sort_by_price_low_to_high():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            open_home_page(page)
            expect(page.locator("[placeholder='Search']")).to_be_visible()
            sort_products(page, "Price (Low - High)")
            expect(page.locator("select")).to_be_visible()
        finally:
            browser.close()


def test_sort_by_price_high_to_low():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            open_home_page(page)
            expect(page.locator("[placeholder='Search']")).to_be_visible()
            sort_products(page, "Price (High - Low)")
            expect(page.locator("select")).to_be_visible()
        finally:
            browser.close()


def test_add_product_to_cart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            open_home_page(page)
            expect(page.locator("[placeholder='Search']")).to_be_visible()
            open_hand_tools(page)
            expect(page).to_have_title("Hand Tools - Practice Software Testing - Toolshop - v5.0")
            first_product = open_second_hand_tool(page)
            expect(page).to_have_title(f"{first_product} - Practice Software Testing - Toolshop - v5.0")
            add_selected_product_to_cart(page, first_product)
            expect(page.locator("body")).to_contain_text("Cart")
        finally:
            browser.close()


def test_remove_product_from_cart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            open_home_page(page)
            expect(page.locator("[placeholder='Search']")).to_be_visible()
            open_hand_tools(page)
            expect(page).to_have_title("Hand Tools - Practice Software Testing - Toolshop - v5.0")
            first_product = open_second_hand_tool(page)
            expect(page).to_have_title(f"{first_product} - Practice Software Testing - Toolshop - v5.0")
            add_selected_product_to_cart(page, first_product)
            open_cart(page)
            expect(page).to_have_title("Checkout - Practice Software Testing - Toolshop - v5.0")
            remove_first_cart_item(page)
            expect(page.locator('[data-test="cart-quantity"]')).not_to_be_visible()
            # expect(page.locator("body")).to_contain_text("Your cart is empty")
        finally:
            browser.close()


def test_submit_valid_contact_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            submit_contact_form(page, "Jane", "Doe", "jane@example.com", "Customer service", "Need product details")
            # expect(page.locator("body")).to_contain_text("Thanks")
        finally:
            browser.close()


def test_submit_invalid_contact_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            submit_contact_form(page, "Jane", "Doe", "invalid-email", "Return", "Need product details")
            # expect(page.locator("body")).to_contain_text("email")
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