import re

import allure

from pages.base_page import BasePage

# Reuse the same price-line extraction logic as the product page
_PRICE_LINE_RE = re.compile(r'(?:^[$€£¥]|[$€£¥]$)')
_PRICE_LABEL_RE = re.compile(r'^(Price|Preis|Regular|Sale|Save)\b', re.IGNORECASE)


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


class SearchResultsPage(BasePage):

    @allure.step("Get first search result price text")
    def get_first_result_price(self) -> str:
        # data-testid="plp-product-card" is on every product card on the search/PLP page.
        card = self.page.locator("[data-testid='plp-product-card']").first
        card.wait_for(state="visible", timeout=10000)
        price = _extract_price_line(card.inner_text())
        if price:
            return price
        raise RuntimeError(
            f"Price line not found in first product card. "
            f"URL: {self.page.url} | Title: {self.page.title()}"
        )

    @allure.step("Get search results summary text")
    def get_results_summary_text(self) -> str:
        # data-testid="plp-a11y-live" is a sr-only <p> that the React app
        # populates once search results arrive.  It is not visually visible so
        # we use text_content() instead of inner_text() / is_visible(), and we
        # wait reactively for the element to receive non-empty content.
        self.page.wait_for_function(
            """() => {
                const el = document.querySelector("[data-testid='plp-a11y-live']");
                return el && el.textContent.trim().length > 0;
            }""",
            timeout=15000,
        )
        loc = self.page.locator("[data-testid='plp-a11y-live']").first
        text = (loc.text_content() or "").strip()
        if text:
            return text
        raise RuntimeError(
            f"Results summary element is empty. "
            f"URL: {self.page.url} | Title: {self.page.title()}"
        )
