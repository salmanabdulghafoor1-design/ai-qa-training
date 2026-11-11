from playwright.sync_api import Page, sync_playwright

BASE_URL = "https://practicesoftwaretesting.com"


def find_first(page: Page, selectors):
    for selector in selectors:
        try:
            if page.locator(selector).count() > 0:
                return selector
        except Exception:
            pass
    return None


def find_search_input(page: Page):
    selectors = [
        "input[placeholder='Search products']",
        "input[type='search']",
        "input[aria-label*='Search']",
        "input[data-test*='search']",
        "input[id*='search']",
    ]
    return find_first(page, selectors)


def find_search_button(page: Page):
    selectors = [
        "[data-test='search-submit']",
        "button:has-text('Search')",
        "button[type='submit']",
        "button[id*='search']",
    ]
    return find_first(page, selectors)


def find_nav_categories(page: Page):
    selectors = [
        "[data-test='nav-categories']",
        "button:has-text('Categories')",
        "a:has-text('Categories')",
    ]
    return find_first(page, selectors)


def find_nav_hand_tools(page: Page):
    selectors = [
        "[data-test='nav-hand-tools']",
        "a:has-text('Hand Tools')",
        "button:has-text('Hand Tools')",
    ]
    return find_first(page, selectors)


def find_product_name(page: Page):
    selectors = [
        "[data-test='product-name']",
        "h5",
        "h3",
        "article .name",
    ]
    return find_first(page, selectors)


def find_product_price(page: Page):
    selectors = [
        "[data-test='unit-price']",
        "[data-test='product-price']",
        ".price",
    ]
    return find_first(page, selectors)


def find_add_to_cart_button(page: Page):
    selectors = [
        "[id='btn-add-to-cart']",
        "[data-test='add-to-cart']",
        "button:has-text('Add to cart')",
    ]
    return find_first(page, selectors)


def find_cart_quantity(page: Page):
    selectors = [
        "[data-test='cart-quantity']",
        "#cart-quantity",
        ".cart-quantity",
    ]
    return find_first(page, selectors)


def find_cart_link(page: Page):
    selectors = [
        "a[href*='basket']",
        "a[href*='cart']",
        "[data-test='cart-link']",
        "a:has-text('Cart')",
    ]
    return find_first(page, selectors)


def find_remove_button(page: Page):
    selectors = [
        "button:has-text('Remove')",
        "[data-test='remove-item']",
        "button[data-test*='remove']",
    ]
    return find_first(page, selectors)


def find_product_title(page: Page):
    selectors = [
        "[data-test='product-title']",
        "h1",
        "h2",
        "h3",
    ]
    return find_first(page, selectors)


def find_product_quantity(page: Page):
    selectors = [
        "[data-test='product-quantity']",
        ".product-quantity",
    ]
    return find_first(page, selectors)


def find_cart_total(page: Page):
    selectors = [
        "[data-test='cart-total']",
        ".cart-total",
    ]
    return find_first(page, selectors)


def find_line_price(page: Page):
    selectors = [
        "[data-test='line-price']",
        ".line-price",
    ]
    return find_first(page, selectors)


def find_contact_fields(page: Page, field_name):
    mapping = {
        "first_name": [
            "input[name='first_name']",
            "input[id='first-name']",
            "input[placeholder='First name']",
            "[data-test='first-name']",
            "input[aria-label*='First']",
        ],
        "last_name": [
            "input[name='last_name']",
            "input[id='last-name']",
            "input[placeholder='Last name']",
            "[data-test='last-name']",
            "input[aria-label*='Last']",
        ],
        "email": [
            "input[type='email']",
            "input[name='email']",
            "input[placeholder='Email']",
            "[data-test='email']",
            "input[aria-label*='Email']",
        ],
        "subject": [
            "input[name='subject']",
            "input[placeholder='Subject']",
            "[data-test='subject']",
            "input[aria-label*='Subject']",
        ],
        "message": [
            "textarea[name='message']",
            "textarea[placeholder='Message']",
            "[data-test='message']",
            "textarea[aria-label*='Message']",
        ],
    }
    return find_first(page, mapping.get(field_name, []))


def find_contact_submit(page: Page):
    selectors = [
        "button:has-text('Send')",
        "[data-test='contact-submit']",
        "button[type='submit']",
        "input[type='submit']",
    ]
    return find_first(page, selectors)


def print_all_locators(page: Page):
    page.goto(BASE_URL)

    locators = {
        "search_input": find_search_input(page),
        "search_button": find_search_button(page),
        "nav_categories": find_nav_categories(page),
        "nav_hand_tools": find_nav_hand_tools(page),
        "product_name": find_product_name(page),
        "product_price": find_product_price(page),
        "add_to_cart_button": find_add_to_cart_button(page),
        "cart_quantity": find_cart_quantity(page),
        "cart_link": find_cart_link(page),
    }

    page.goto(BASE_URL + "/contact")
    locators.update({
        "first_name": find_contact_fields(page, "first_name"),
        "last_name": find_contact_fields(page, "last_name"),
        "email": find_contact_fields(page, "email"),
        "subject": find_contact_fields(page, "subject"),
        "message": find_contact_fields(page, "message"),
        "contact_submit": find_contact_submit(page),
    })

    print("\n=== RESOLVED LOCATORS ===")
    for key, value in locators.items():
        print(f"{key}: {value}")
    print("=========================\n")


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            print_all_locators(page)
        finally:
            browser.close()