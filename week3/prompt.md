# Week 3 sorting test-generation prompt

Use the Week 2 sorting test and the `session_3_demo_code` helpers as examples. Create pytest-based UI and API sorting tests for `https://practicesoftwaretesting.com`.

Requirements:

- Keep reusable browser, API, CSV, and sorting helpers in `helpers.py`.
- Put all valid and invalid sort option labels and the expected sort metadata in `data.csv`. Do not hardcode the valid or invalid option lists in Python.
- Create `test_1.py` with the parameterized UI sorting test.
- Create `test_2.py` with the equivalent parameterized API sorting test.
- Keep both tests parameterized so each runs once for every CSV row.
- For valid options, verify product names, prices, or CO₂ ratings are in the expected order. For invalid options, verify they are rejected.
- Make `test_week3.py` exercise both levels and compare the API response used by the UI with the rendered products using assertions.
- Close browser and API resources in `finally` blocks and do not submit any forms.

Run the suite from the repository root with:

```powershell
& '.\.venv\Scripts\python.exe' -m pytest .\week3 -v
```
