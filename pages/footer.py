import allure
from pages.base_page import BasePage


class FooterPage(BasePage):

    @allure.step("Get cookie consent button text")
    def get_cookie_accept_button_text(self) -> str:
        selectors = [
            "[data-testid='cookie-accept-all-btn']",
            "button#onetrust-accept-btn-handler",
            "button[class*='accept-all']",
            "button:has-text('Accept all')",
            "button:has-text('Alle Cookies akzeptieren')",
        ]
        for selector in selectors:
            btn = self.page.locator(selector).first
            if btn.is_visible(timeout=3000):
                return btn.inner_text()
        raise RuntimeError("Cookie consent button not found")

    @allure.step("Get footer text")
    def get_footer_text(self) -> str:
        return self.page.locator("footer").inner_text()
