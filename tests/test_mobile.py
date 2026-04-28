import allure
import pytest

from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.product_page import ProductPage

_MOBILE_VIEWPORT = {"width": 375, "height": 667}  # iPhone SE


@pytest.fixture
def mobile_page(browser, locale):
    """Browser page with a mobile (375×667) viewport, matching the locale."""
    lang_header = locale["html_lang"]
    context = browser.new_context(
        locale=lang_header,
        extra_http_headers={"Accept-Language": lang_header},
        viewport=_MOBILE_VIEWPORT,
    )
    page = context.new_page()
    try:
        from playwright_stealth import Stealth
        Stealth().use_sync(page)
    except (ImportError, AttributeError):
        try:
            from playwright_stealth import stealth_sync
            stealth_sync(page)
        except (ImportError, AttributeError):
            pass
    yield page
    context.close()


@allure.feature("Mobile Viewport")
@pytest.mark.no_autouse_cookies
class TestMobileViewport:
    """Verify key localization properties are correct on a mobile viewport.

    IKEA renders a separate mobile layout; these tests confirm the locale
    context is preserved when the responsive breakpoint changes.
    """

    @allure.story("HTML lang on mobile")
    def test_html_lang_matches_locale_on_mobile(self, mobile_page, locale):
        """TC-MB-01: HTML lang attribute is correct when viewed on a mobile viewport."""
        base = BasePage(mobile_page)
        with allure.step(f"Navigate to {locale['base_url']} on mobile"):
            base.navigate(locale["base_url"])
            base.wait_for_page_load()
            base.accept_cookies()
        home = HomePage(mobile_page)
        html_lang = home.get_html_lang()
        with allure.step(f"Assert html lang is '{locale['html_lang']}'"):
            assert html_lang == locale["html_lang"], (
                f"Mobile ({_MOBILE_VIEWPORT['width']}px): "
                f"expected lang '{locale['html_lang']}', got '{html_lang}'"
            )

    @allure.story("Currency symbol on mobile")
    def test_currency_symbol_correct_on_mobile(self, mobile_page, locale):
        """TC-MB-02: Currency symbol is correct on a product page viewed on mobile."""
        base = BasePage(mobile_page)
        with allure.step(f"Navigate to {locale['base_url']} on mobile"):
            base.navigate(locale["base_url"])
            base.wait_for_page_load()
            base.accept_cookies()
        product = ProductPage(mobile_page)
        with allure.step(f"Navigate to {locale['billy_url']}"):
            product.navigate(locale["billy_url"])
            product.wait_for_page_load()
        price_text = product.get_price_text()
        symbol = product.get_currency_symbol(price_text)
        with allure.step(f"Assert currency symbol is '{locale['currency_symbol']}'"):
            assert symbol == locale["currency_symbol"], (
                f"Mobile ({_MOBILE_VIEWPORT['width']}px): "
                f"expected '{locale['currency_symbol']}', got '{symbol}' from '{price_text}'"
            )
