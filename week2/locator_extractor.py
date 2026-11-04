import re
from playwright.sync_api import Page, expect, sync_playwright

BASE_URL = "https://practicesoftwaretesting.com"


def inspect_page(page: Page):
    page.goto(BASE_URL)
    page.screenshot(path="page-home.png")

    snapshot = page.accessibility.snapshot()
    print("Accessibility snapshot:")
    print(snapshot)

    print(page.locator("body").inner_html()[:4000])

    print("Has Search input:", page.get_by_role("textbox").count())
    print("Has Search button:", page.get_by_role("button", name="Search").count())
    print("Has Cart link:", page.get_by_role("link", name=re.compile("cart", re.I)).count())


def inspect_contact_page(page: Page):
    page.goto(BASE_URL + "/contact")
    print("Contact accessibility snapshot:")
    print(page.accessibility.snapshot())

    for selector in [
        page.get_by_label("First name"),
        page.get_by_label("Last name"),
        page.get_by_label("Email"),
        page.get_by_label("Subject"),
        page.get_by_label("Message"),
        page.get_by_role("button", name="Send"),
    ]:
        print(selector, "exists:", selector.count())


def inspect_product_list(page: Page):
    page.goto(BASE_URL)
    page.locator("select").first.wait_for()

    print("Sort select count:", page.locator("select").count())
    print("Add to cart button count:", page.get_by_role("button", name="Add to cart").count())
    print("Product cards count:", page.locator("article, .product, .card").count())


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            inspect_page(page)
            inspect_contact_page(page)
            inspect_product_list(page)
        finally:
            browser.close()