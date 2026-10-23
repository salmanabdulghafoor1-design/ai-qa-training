from playwright.sync_api import expect, sync_playwright
import re

# Your test code goes here


BASE_URL = "https://practicesoftwaretesting.com"
first_product = None

def test_browse_category(page):
    page.goto(BASE_URL)
    page.locator('[data-test="nav-categories"]').click()
    page.locator('[data-test="nav-hand-tools"]').click()
    expect(page).to_have_title("Hand Tools - Practice Software Testing - Toolshop - v5.0")
    print("PASS: Hand Tools category page loaded successfully")
    product_count = page.locator('[data-test="product-name"]').count()
    if product_count > 0:
        print("PASS: Hand Tools category has at least one listed product")
        for i in range(product_count):
            product_name = page.locator('[data-test="product-name"]').nth(i).inner_text()
            if (product_name.strip() == ""):
                print(f"FAIL: Product {i + 1} has an empty name")
            else:
                print(f"Product {i + 1}: {product_name}")

def test_product_details(page):
    page.goto(BASE_URL)
    page.locator('[data-test="nav-categories"]').click()
    page.locator('[data-test="nav-hand-tools"]').click()
    expect(page).to_have_title("Hand Tools - Practice Software Testing - Toolshop - v5.0")
    print("PASS: Hand Tools category page loaded successfully")
    product_count = page.locator('[data-test="product-name"]').count()
    if product_count > 0:
        print("PASS: Hand Tools category has at least one listed product")
        for i in range(product_count):
            product_name = page.locator('[data-test="product-name"]').nth(i).inner_text()
            if (product_name.strip() == ""):
                print(f"FAIL: Product {i + 1} has an empty name")
            else:
                print(f"Product {i + 1}: {product_name}")
            if (i == 0):
                first_product = product_name
    page.locator('[data-test="product-name"]').nth(0).click()
    expect(page).to_have_title(f"{first_product} - Practice Software Testing - Toolshop - v5.0")
    print("PASS: First Product Tool detail page loaded successfully")
    expect(page.locator('[data-test="product-name"]')).to_have_text(first_product)
    print(f"PASS: Product name on detail page matches the first product name: {first_product}")
    expect(page.locator('[data-test="unit-price"]')).to_be_visible()
    print("PASS: Product unit price is displayed on the detail page")
    expect(page.locator('[id="btn-add-to-cart"]')).to_be_visible()
    print("PASS: Add to Cart button is visible on the detail page")

def test_add_to_cart(page):
    page.goto(BASE_URL)
    page.locator('[data-test="nav-categories"]').click()
    page.locator('[data-test="nav-hand-tools"]').click()
    expect(page).to_have_title("Hand Tools - Practice Software Testing - Toolshop - v5.0")
    print("PASS: Hand Tools category page loaded successfully")
    product_count = page.locator('[data-test="product-name"]').count()
    if product_count > 0:
        print("PASS: Hand Tools category has at least one listed product")
        for i in range(product_count):
            product_name = page.locator('[data-test="product-name"]').nth(i).inner_text()
            if (product_name.strip() == ""):
                print(f"FAIL: Product {i + 1} has an empty name")
            else:
                print(f"Product {i + 1}: {product_name}")
            if (i == 1):
                first_product = product_name
    page.locator('[data-test="product-name"]').nth(1).click()
    #expect(page).to_have_title(f"{first_product} - Practice Software Testing - Toolshop - v5.0")
    #print("PASS: First Product Tool detail page loaded successfully")
    #expect(page.locator('[data-test="product-name"]')).to_have_text(first_product)
    #print(f"PASS: Product name on detail page matches the first product name: {first_product}")
    #expect(page.locator('[data-test="unit-price"]')).to_be_visible()
    #print("PASS: Product unit price is displayed on the detail page")
    unit_price = page.locator('[data-test="unit-price"]').inner_text()
    print(f"PASS: Product unit price of {first_product} on detail page: {unit_price}")
    #expect(page.locator('[id="btn-add-to-cart"]')).to_be_visible()
    #print("PASS: Add to Cart button is visible on the detail page")
    page.locator('[id="btn-add-to-cart"]').click()
    if(page.locator('[data-test="cart-quantity"]').count() == 1):
        cart_count = page.locator('[data-test="cart-quantity"]').inner_text()
        print(f"PASS: Cart quantity after adding {first_product} to cart: {cart_count}")
    page.locator('[data-test="cart-quantity"]').click()
    expect(page).to_have_title("Checkout - Practice Software Testing - Toolshop - v5.0")
    print("PASS: Checkout page loaded successfully")
    expect(page.locator('[data-test="product-title"]')).to_have_text(first_product)
    print(f"PASS: Product name on checkout page matches the first product name: {first_product}")
    expect(page.locator('[data-test="product-quantity"]')).to_have_count(1)
    print("PASS: Product quantity on checkout page is 1")
    expect(page.locator('[data-test="cart-total"]')).to_have_text(re.compile(rf"\${unit_price}"))
    print(f"PASS: Cart total on checkout page matches the unit price of {first_product}: {unit_price}")
    expect(page.locator('[data-test="product-price"]')).to_have_text(re.compile(rf"\${unit_price}"))
    print(f"PASS: Product price on checkout page matches the unit price of {first_product}: {unit_price}")
    expect(page.locator('[data-test="line-price"]')).to_have_text(re.compile(rf"\${unit_price}"))
    print(f"PASS: Line price on checkout page matches the unit price of {first_product}: {unit_price}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        #test_browse_category(page)
        #test_product_details(page)
        test_add_to_cart(page)
        browser.close 

if __name__ == "__main__":
    main()