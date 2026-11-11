# Week 3 test-generation prompt

Use the Week 2 sorting test and the `session_3_demo_code` tests as examples. Create a pytest-based Week 3 test suite for `https://practicesoftwaretesting.com`.

Requirements:

- Keep all reusable browser, API, CSV, search, and sort helpers in `helpers.py`. Carry over the supporting functions from `session_3_demo_code/helpers.py`.
- Use `pytest.mark.parametrize` to run a UI product-search test once for every `search_word` row in `data.csv`.
- Add a parameterized UI sorting test using the site's valid options, including name, price, and CO₂ rating in both directions. Reject invalid sort values.
- Add one API search test that checks a successful status, validates at least three fields (`id`, `name`, and `price`), and compares the API product names with the products displayed by the page.
- Keep the tests readable, use Playwright expectations for UI assertions, close browser/API resources in `finally` blocks, and do not submit any forms.

Run the suite from the repository root with:

```powershell
& '.\.venv\Scripts\python.exe' -m pytest .\week3 -v
```
