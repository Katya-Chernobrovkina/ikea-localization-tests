import allure
from pages.home_page import HomePage


@allure.feature("Homepage")
class TestHomepage:

    @allure.story("HTML language attribute")
    def test_html_lang_matches_locale(self, page, locale):
        """TC-HP-01: HTML lang attribute matches the expected locale value."""
        home = HomePage(page)
        actual_lang = home.get_html_lang()
        with allure.step(f"Assert lang='{locale['html_lang']}'"):
            assert actual_lang == locale["html_lang"], (
                f"Expected html lang '{locale['html_lang']}', got '{actual_lang}'"
            )

    @allure.story("Navigation language")
    def test_navigation_language(self, page, locale):
        """TC-HP-02: Navigation bar contains the expected locale nav item."""
        home = HomePage(page)
        nav_text = home.get_nav_item_text(locale["nav_item"])
        with allure.step(f"Assert nav item contains '{locale['nav_item']}'"):
            assert locale["nav_item"] in nav_text, (
                f"Expected nav item '{locale['nav_item']}' not found, got '{nav_text}'"
            )
