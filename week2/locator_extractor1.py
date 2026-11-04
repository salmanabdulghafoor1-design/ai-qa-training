import re
from playwright.sync_api import Page, sync_playwright

BASE_URL = "https://practicesoftwaretesting.com"


def find_first(page: Page, selectors):
    for selector in selectors:
        try:
            loc = page.locator(selector)
            if loc.count() > 0:
                return selector
        except Exception:
            pass
    return None


def find_search_input(page: Page):
    candidates = [
        "input[placeholder='Search products']",
        "input[placeholder*='Search']",
        "input[type='search']",
        "input[aria-label*='Search']",
        "input[data-test*='search']",
        "input[name*='search']",
        "input[name*='query']",
    ]
    found = find_first(page, candidates)
    if found:
        return found

    # role-based fallback
    for role_name in ["textbox", "searchbox"]:
        loc = page.get_by_role(role_name)
        if loc.count() > 0:
            return f"page.get_by_role('{role_name}')"

    return None


def find_search_button(page: Page):
    candidates = [
        "button:has-text('Search')",
        "button[type='submit']",
        "button[data-test*='search']",
        "button:has-text('Search products')",
    ]
    found = find_first(page, candidates)
    if found:
        return found

    loc = page.get_by_role("button", name=re.compile(r"search", re.I))
    if loc.count() > 0:
        return "page.get_by_role('button', name=re.compile(r'search', re.I))"

    return None


def find_sort_select(page: Page):
    loc = page.get_by_label(re.compile(r"sort", re.I))
    if loc.count() > 0:
        return "page.get_by_label(re.compile(r'sort', re.I))"

    candidates = [
        "select",
        "select[data-test*='sort']",
        "select[aria-label*='Sort']",
    ]
    found = find_first(page, candidates)
    if found:
        return found

    return None


def find_add_to_cart_button(page: Page):
    loc = page.get_by_role("button", name=re.compile(r"add to cart", re.I))
    if loc.count() > 0:
        return "page.get_by_role('button', name=re.compile(r'add to cart', re.I))"

    candidates = [
        "button:has-text('Add to cart')",
        "button[data-test*='add-to-cart']",
        "button[data-test*='add']",
    ]
    found = find_first(page, candidates)
    if found:
        return found

    return None


def find_cart_link(page: Page):
    loc = page.get_by_role("link", name=re.compile(r"cart|basket", re.I))
    if loc.count() > 0:
        return "page.get_by_role('link', name=re.compile(r'cart|basket', re.I))"

    candidates = [
        "a[href*='basket']",
        "a[href*='cart']",
        "a:has-text('Cart')",
        "a:has-text('Basket')",
    ]
    found = find_first(page, candidates)
    if found:
        return found

    return None


def find_remove_button(page: Page):
    loc = page.get_by_role("button", name=re.compile(r"remove", re.I))
    if loc.count() > 0:
        return "page.get_by_role('button', name=re.compile(r'remove', re.I))"

    candidates = [
        "button:has-text('Remove')",
        "button[data-test*='remove']",
    ]
    found = find_first(page, candidates)
    if found:
        return found

    return None


def find_contact_field(page: Page, field_name: str):
    mapping = {
        "first name": [
            "input[name='first_name']",
            "input[id*='first']",
            "input[placeholder*='First']",
            "input[aria-label*='First']",
        ],
        "last name": [
            "input[name='last_name']",
            "input[id*='last']",
            "input[placeholder*='Last']",
            "input[aria-label*='Last']",
        ],
        "email": [
            "input[type='email']",
            "input[name='email']",
            "input[placeholder*='Email']",
            "input[aria-label*='Email']",
        ],
        "subject": [
            "input[name='subject']",
            "input[placeholder*='Subject']",
            "input[aria-label*='Subject']",
        ],
        "message": [
            "textarea[name='message']",
            "textarea[placeholder*='Message']",
            "textarea[aria-label*='Message']",
        ],
    }

    # role-based label lookup first
    label_map = {
        "first name": re.compile(r"first\\s*name", re.I),
        "last name": re.compile(r"last\\s*name", re.I),
        "email": re.compile(r"email", re.I),
        "subject": re.compile(r"subject", re.I),
        "message": re.compile(r"message", re.I),
    }

    if field_name in label_map:
        loc = page.get_by_label(label_map[field_name])
        if loc.count() > 0:
            return f"page.get_by_label(re.compile(r'{label_map[field_name].pattern}', re.I))"

    for selector in mapping.get(field_name, []):
        loc = page.locator(selector)
        if loc.count() > 0:
            return selector

    return None


def find_contact_submit(page: Page):
    loc = page.get_by_role("button", name=re.compile(r"send", re.I))
    if loc.count() > 0:
        return "page.get_by_role('button', name=re.compile(r'send', re.I))"

    candidates = [
        "button:has-text('Send')",
        "button[type='submit']",
        "button[data-test*='send']",
    ]
    found = find_first(page, candidates)
    if found:
        return found

    return None


def extract_all_locators(page: Page):
    locators = {}

    page.goto(BASE_URL)

    locators["home_url"] = BASE_URL
    locators["search_input"] = find_search_input(page)
    locators["search_button"] = find_search_button(page)
    locators["sort_select"] = find_sort_select(page)
    locators["add_to_cart_button"] = find_add_to_cart_button(page)
    locators["cart_link"] = find_cart_link(page)

    page.goto(BASE_URL + "/contact")

    locators["first_name"] = find_contact_field(page, "first name")
    locators["last_name"] = find_contact_field(page, "last name")
    locators["email"] = find_contact_field(page, "email")
    locators["subject"] = find_contact_field(page, "subject")
    locators["message"] = find_contact_field(page, "message")
    locators["contact_submit"] = find_contact_submit(page)

    # cart page
    page.goto(BASE_URL)
    cart_link = find_cart_link(page)
    if cart_link:
        try:
            if "page.get_by_role" in cart_link:
                evaluator = eval(cart_link.split(" = ")[0]) if False else None
            # we just navigate directly to likely cart route
            page.goto(BASE_URL + "/basket")
            locators["remove_button"] = find_remove_button(page)
        except Exception:
            locators["remove_button"] = None
    else:
        locators["remove_button"] = None

    return locators


def print_all_locators(page: Page):
    locators = extract_all_locators(page)

    print("\n=== RESOLVED LOCATORS ===")
    for key, value in locators.items():
        print(f"{key}: {value}")
    print("=========================\n")


def test_search(page: Page):
    search_input = find_search_input(page)
    if not search_input:
        raise RuntimeError("Search input not found.")
    page.locator(search_input).fill("Pliers")
    button = find_search_button(page)
    if not button:
        raise RuntimeError("Search button not found.")
    page.locator(button).click()


def test_sort(page: Page):
    sort_select = find_sort_select(page)
    if not sort_select:
        raise RuntimeError("Sort selector not found.")
    page.locator(sort_select).select_option(label="Price: Low to High")


def test_add_to_cart(page: Page):
    button = find_add_to_cart_button(page)
    if not button:
        raise RuntimeError("Add to cart button not found.")
    page.locator(button).first.click()


def test_open_cart(page: Page):
    cart = find_cart_link(page)
    if not cart:
        raise RuntimeError("Cart link not found.")
    page.locator(cart).click()


def test_contact_form(page: Page):
    page.goto(BASE_URL + "/contact")
    for key, label in {
        "first_name": "First name",
        "last_name": "Last name",
        "email": "Email",
        "subject": "Subject",
        "message": "Message",
    }.items():
        loc = find_contact_field(page, key.replace("_", " "))
        if not loc:
            raise RuntimeError(f"{label} field not found.")
        page.locator(loc).fill("sample")


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            print_all_locators(page)
        finally:
            browser.close()