# IKEA Localization Tests

Automated end-to-end test suite that verifies IKEA's website renders correctly across multiple locales — checking language, currency, units, and UI text for each region.

[![CI](https://github.com/Katya-Chernobrovkina/ikea-localization-tests/actions/workflows/tests.yml/badge.svg)](https://github.com/Katya-Chernobrovkina/ikea-localization-tests/actions/workflows/tests.yml)
[![Allure Report](https://img.shields.io/badge/Allure-Report-brightgreen)](https://Katya-Chernobrovkina.github.io/ikea-localization-tests/)

**Live Allure report:** https://Katya-Chernobrovkina.github.io/ikea-localization-tests/

---

## What this project tests

The suite validates IKEA's localization across two regions (Germany `de` and United States `us`):

| Area | What is verified |
|---|---|
| **Homepage** | `<html lang>` attribute and navigation bar language |
| **Product page** | Currency symbol, price format (decimal separator & symbol position), dimension units (`cm` vs `in`), add-to-cart button text |
| **Search results** | Currency symbol in result cards, results summary language |
| **Footer** | Copyright text, cookie consent button language |

Each test method runs **twice** — once per locale — giving 22 total test executions from 11 parametrized test cases.

---

## Tech stack

| Tool | Role |
|---|---|
| **Python 3.11** | Language |
| **Playwright** | Browser automation (Chromium) |
| **playwright-stealth** | Bypasses IKEA bot-detection |
| **pytest + pytest-playwright** | Test framework and runner |
| **Allure** | Interactive HTML test report with trend history |
| **GitHub Actions** | CI/CD — runs on every push to `main` and every Monday at 08:00 UTC |
| **GitHub Pages** | Hosts the live Allure report |

---

## How to run locally

**Prerequisites:** Python 3.11+, Git

```bash
# 1. Clone the repository
git clone https://github.com/Katya-Chernobrovkina/ikea-localization-tests.git
cd ikea-localization-tests

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Playwright browser (Chromium only)
python -m playwright install chromium

# 5. Run the full test suite
pytest

# 6. View the Allure report (requires Allure CLI installed)
allure serve allure-results
```

To run tests for a single locale only:

```bash
pytest -m de    # Germany only
pytest -m us    # United States only
```

---

## Project structure

```
ikea-localization-tests/
├── .github/
│   └── workflows/
│       └── tests.yml           # GitHub Actions CI pipeline
├── config/
│   └── locales.json            # Per-locale test data (URLs, currency, units, button text)
├── pages/                      # Page Object Model classes
│   ├── base_page.py
│   ├── home_page.py
│   ├── footer.py
│   ├── product_page.py
│   └── search_results_page.py
├── tests/
│   ├── conftest.py             # Fixtures: browser, page, locale parametrization
│   ├── test_footer.py
│   ├── test_homepage.py
│   ├── test_product_page.py
│   └── test_search_results.py
├── allure-results/             # Raw Allure artifacts (git-ignored)
├── debug_selectors.py          # Utility: probe live IKEA pages for DOM selectors
├── pytest.ini
└── requirements.txt
```

---

## Expanding to new countries

All locale-specific data lives in [`config/locales.json`](config/locales.json). To add a new region, append a new entry following the existing schema:

```json
{
  "locale_code": {
    "base_url": "https://www.ikea.com/<country>/<language>",
    "product_url": "<full URL to the Billy bookcase in this locale>",
    "currency_symbol": "€",
    "currency_position": "trailing",
    "decimal_separator": ",",
    "unit": "cm",
    "html_lang": "de-DE",
    "nav_keyword": "Produkte",
    "add_to_cart_text": "In den Warenkorb",
    "cookie_button_text": "Alle Cookies akzeptieren",
    "search_term": "sofa",
    "search_result_keyword": "Sofa"
  }
}
```

The `locale` fixture in `tests/conftest.py` reads this file at runtime and parametrizes every test automatically — no test code changes required.

---

> **Portfolio note:** This project was built as a portfolio piece to demonstrate test automation skills in the area of localization and internationalisation (i18n) testing. It showcases the Page Object Model pattern, data-driven parametrization, Allure reporting with CI integration, and anti-bot techniques needed to test real-world e-commerce sites.
