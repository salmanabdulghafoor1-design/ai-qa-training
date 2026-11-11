Create pytest-based UI and API sorting tests for https://practicesoftwaretesting.com.

- Keep reusable browser, API, CSV, and sorting helpers in `helpers.py`.
- Store valid and invalid sort option labels and expected sorting metadata in `data.csv`.
- Put the UI-only parameterized sorting test in `test_1.py` and the API-only parameterized test in `test_2.py`.
- In `test_week3.py`, test both levels and assert that the API response used by the UI matches the rendered products.
- Each test should run once for every CSV row, validate sorting for names, prices, or CO₂ ratings, and verify invalid values are rejected.
- Close browser and API resources in `finally` blocks and do not submit forms.
- Run the tests with `.venv\Scripts\python.exe -m pytest week3 -v`.
