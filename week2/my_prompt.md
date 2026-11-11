#prompt to extract locators from live page using playwright mcp
Use the Playwright MCP tools to:
1. Open my application URL: https://practicesoftwaretesting.com/
2. Navigate to the pages mentioned in week2/tests.py file.
3. Inspect the actual rendered DOM and accessibility snapshot.
4. Identify the controls as referenced in week2/tests.py file.
5. Generate reliable Playwright Python locators for these elements.
6. Verify each locator uniquely identifies its intended element.
7. Return production-ready Python code using data-test and ids wherever appropriate. Examples: page.locator('[data-test="cart-quantity"]')   expect(page).to_have_title("Checkout - Practice Software Testing - Toolshop - v5.0")   
8. Do not guess locators. Inspect the live page first. 
9. Now generate a Python Playwright locator repository snippet.
a. For every locator:
- Explain the locator strategy.
- Check locator.count() == 1.
- Check visibility and enabled state where applicable.
- Avoid XPath and brittle CSS selectors.
- Use meaningful Python variable names.
- Do not interact with the application yet.
10. Return the code in a format I can directly add to my existing Python automation project.