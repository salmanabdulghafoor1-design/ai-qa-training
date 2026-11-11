# Week 3 sorting test-generation prompt

Use the Week 2 sorting test and the `session_3_demo_code` helpers as examples. Create a pytest-based UI sorting suite for `https://practicesoftwaretesting.com`.

Requirements:

- Keep reusable browser, CSV, and sorting helpers in `helpers.py`.
- Put all valid and invalid sort option labels and the expected sort metadata in `data.csv`. Do not hardcode the valid or invalid option lists in Python.
- Use `pytest.mark.parametrize` so the same sorting test runs once for every CSV row.
- For valid options, verify the selected option and that product names, prices, or CO₂ ratings are in the expected order.
- For invalid options, verify the page's sort control rejects the option.
- Remove the Week 3 search tests and API search test.
- Close browser resources in `finally` blocks and do not submit any forms.

Run the suite from the repository root with:

```powershell
& '.\.venv\Scripts\python.exe' -m pytest .\week3 -v
```
