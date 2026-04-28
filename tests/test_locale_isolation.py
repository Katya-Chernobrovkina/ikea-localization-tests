import json
from pathlib import Path

import allure

from pages.home_page import HomePage
from pages.product_page import ProductPage

LOCALES_PATH = Path(__file__).parent.parent / "config" / "locales.json"
with LOCALES_PATH.open(encoding="utf-8") as f:
    ALL_LOCALES = json.load(f)


@allure.feature("Locale Isolation")
class TestLocaleIsolation:
    """Cross-locale contamination checks.

    Each test navigates to one locale and verifies that content belonging to
    the other locales is absent. This catches a specific class of localization
    bug where the wrong locale's content leaks into a page (e.g. due to a CDN
    misconfiguration or a component not reading the locale context correctly).
    """

    @allure.story("Currency contamination")
    def test_wrong_currency_absent_from_price(self, page, locale):
        """TC-NL-01: Product price must not contain any other locale's currency symbol."""
        product = ProductPage(page)
        with allure.step(f"Navigate to {locale['billy_url']}"):
            product.navigate(locale["billy_url"])
            product.wait_for_page_load()
        price_text = product.get_price_text()
        for other_key, other_config in ALL_LOCALES.items():
            if other_key == locale["key"]:
                continue
            wrong_symbol = other_config["currency_symbol"]
            with allure.step(f"Assert '{wrong_symbol}' ({other_key}) is absent from '{price_text}'"):
                assert wrong_symbol not in price_text, (
                    f"Locale '{locale['key']}': found {other_key} currency "
                    f"'{wrong_symbol}' in price '{price_text}'"
                )

    @allure.story("Navigation language contamination")
    def test_wrong_nav_language_absent(self, page, locale):
        """TC-NL-03: Navigation must not contain any other locale's nav item text."""
        for other_key, other_config in ALL_LOCALES.items():
            if other_key == locale["key"]:
                continue
            wrong_nav = other_config["nav_item"]
            wrong_locator = page.locator(f"nav a:has-text('{wrong_nav}')")
            with allure.step(f"Assert nav link '{wrong_nav}' ({other_key}) is absent"):
                assert wrong_locator.count() == 0, (
                    f"Locale '{locale['key']}': found {other_key} nav text "
                    f"'{wrong_nav}' in navigation"
                )

    @allure.story("HTML lang contamination")
    def test_wrong_html_lang_absent(self, page, locale):
        """TC-NL-06: HTML lang attribute must not be set to another locale's language code."""
        home = HomePage(page)
        html_lang = home.get_html_lang()
        for other_key, other_config in ALL_LOCALES.items():
            if other_key == locale["key"]:
                continue
            wrong_lang = other_config["html_lang"]
            with allure.step(f"Assert html lang '{html_lang}' is NOT '{wrong_lang}' ({other_key})"):
                assert html_lang != wrong_lang, (
                    f"Locale '{locale['key']}': html lang '{html_lang}' "
                    f"belongs to locale '{other_key}'"
                )
