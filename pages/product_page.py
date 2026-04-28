import re

import allure

from pages.base_page import BasePage

# IKEA's Skapa design system stamps data-skapa on its components.
# The price module always starts with "price-module@" regardless of version number.
_PRICE_MODULE = "[data-skapa^='price-module']"

# A price line starts with a currency symbol (leading) or ends with one (trailing),
# contains at least one digit, is short enough to exclude product descriptions,
# and must NOT start with a label word like "Price" / "Preis" (sr-only duplicate text).
_PRICE_LINE_RE = re.compile(r'(?:^[$€£¥]|[$€£¥]$)')
_PRICE_LABEL_RE = re.compile(r'^(Price|Preis)\b', re.IGNORECASE)


def _extract_price_line(inner_text: str) -> str | None:
    for line in inner_text.split('\n'):
        line = line.strip()
        if (line
                and _PRICE_LINE_RE.search(line)
                and re.search(r'\d', line)
                and len(line) < 20
                and not _PRICE_LABEL_RE.match(line)):
            return line
    return None


class ProductPage(BasePage):

    @allure.step("Get price text from product page")
    def get_price_text(self) -> str:
        loc = self.page.locator(_PRICE_MODULE).first
        loc.wait_for(state="visible", timeout=10000)
        price = _extract_price_line(loc.inner_text())
        if price:
            return price
        raise RuntimeError(
            f"Price line not found in price module. "
            f"URL: {self.page.url} | Title: {self.page.title()}"
        )

    @allure.step("Extract currency symbol from price text")
    def get_currency_symbol(self, price_text: str) -> str:
        return re.sub(r'[\d\s.,\u00a0\u202f]', '', price_text).strip()

    @allure.step("Get dimension unit from product page")
    def get_dimension_unit(self) -> str:
        # The product subtitle inside the price module contains dimensions,
        # e.g. "80x28x202 cm" (DE) or "31 1/2x11x79 1/2 \"" (US).
        loc = self.page.locator(_PRICE_MODULE).first
        loc.wait_for(state="visible", timeout=10000)
        text = loc.inner_text()
        if re.search(r'\d+\s*cm\b', text):
            return "cm"
        if re.search(r'\d\s*"', text) or re.search(r'\d+\s*in\b', text):
            return "in"
        raise RuntimeError(
            f"Dimension unit not found in price module text. "
            f"URL: {self.page.url} | Title: {self.page.title()}"
        )

    @allure.step("Get add-to-cart button text")
    def get_add_to_cart_text(self) -> str:
        # The buy section renders below the product gallery; scroll past it so
        # React mounts the add-to-cart widget before we start querying.
        self.page.evaluate("window.scrollTo(0, 1500)")
        selectors = [
            "button:has-text('Add to bag')",
            "button:has-text('In den Warenkorb')",
            "button:has-text('Add to cart')",
            "button:has-text('In den Einkaufswagen')",
            "button[data-ref='add-to-cart-btn']",
            "button[aria-label*='Add to bag']",
            "button[aria-label*='Warenkorb']",
        ]
        for selector in selectors:
            try:
                btn = self.page.locator(selector).first
                if btn.is_visible(timeout=6000):
                    text = btn.inner_text().strip()
                    if not text:
                        text = (btn.get_attribute("aria-label") or "").strip()
                    if text:
                        return text.strip()
            except Exception:
                continue
        raise RuntimeError(
            f"Add to cart button not found. "
            f"URL: {self.page.url} | Title: {self.page.title()}"
        )
