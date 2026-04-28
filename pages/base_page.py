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
