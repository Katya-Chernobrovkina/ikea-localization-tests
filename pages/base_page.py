import re

# Matches a price line by its currency marker:
#   - leading $, €, £, ¥  (US, EU, UK, JP)
#   - trailing $, €, £, ¥
#   - trailing "kr" (Swedish krona spelled out)
#   - trailing ":-" (Swedish round-number shorthand, e.g. "249:-")
_PRICE_LINE_RE = re.compile(r'(?:^[$€£¥]|[$€£¥]$|\bkr$|:-$)', re.IGNORECASE)
# Accessibility label lines that duplicate the price text — skip these.
_PRICE_LABEL_RE = re.compile(r'^(Price|Preis|Regular|Sale|Save)\b', re.IGNORECASE)


def _extract_price_line(inner_text: str) -> str | None:
    """Return the first line from inner_text that looks like an actual price."""
    for line in inner_text.split('\n'):
        line = line.strip()
        if (line
                and _PRICE_LINE_RE.search(line)
                and re.search(r'\d', line)
                and len(line) < 25
                and not _PRICE_LABEL_RE.match(line)):
            return line
    return None


class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def accept_cookies(self):
        # IKEA uses different button selectors across regions and A/B tests
        selectors = [
            "[data-testid='cookie-accept-all-btn']",
            "button#onetrust-accept-btn-handler",
            "button[class*='accept-all']",
            "button:has-text('Accept all')",
            "button:has-text('Alle Cookies akzeptieren')",
            "button:has-text('Acceptera cookies')",
            "button:has-text('Tillåt alla')",
            "button:has-text('Acceptera alla')",
        ]
        for selector in selectors:
            try:
                btn = self.page.locator(selector).first
                if btn.is_visible(timeout=3000):
                    btn.click()
                    return
            except Exception:
                continue

    def wait_for_page_load(self):
        self.page.wait_for_load_state("load")
