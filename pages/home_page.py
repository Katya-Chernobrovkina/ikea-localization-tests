import allure
from pages.base_page import BasePage


class HomePage(BasePage):

    @allure.step("Get <html lang> attribute")
    def get_html_lang(self) -> str:
        return self.page.locator("html").get_attribute("lang")

    @allure.step("Get nav item text containing '{expected_text}'")
    def get_nav_item_text(self, expected_text: str) -> str:
        nav_link = self.page.locator(f"nav a:has-text('{expected_text}')").first
        return nav_link.inner_text()
