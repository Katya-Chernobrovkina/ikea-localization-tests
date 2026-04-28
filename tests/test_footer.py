import allure
import pytest
from pages.footer import FooterPage


@allure.feature("Footer")
class TestFooter:

    @allure.story("Footer copyright text")
    def test_footer_text_present(self, page, locale):
        """TC-FT-01: Footer contains IKEA copyright notice on all locales."""
        footer = FooterPage(page)
        footer_text = footer.get_footer_text()
        with allure.step("Assert footer contains 'Inter IKEA Systems B.V.'"):
            assert "Inter IKEA Systems B.V." in footer_text, (
                f"Expected 'Inter IKEA Systems B.V.' in footer, got: {footer_text[:200]}"
            )

    @allure.story("Cookie consent language")
    @pytest.mark.no_autouse_cookies
    def test_cookie_consent_language(self, page, locale):
        """TC-FT-02: Cookie consent button text matches locale before cookies accepted."""
        footer = FooterPage(page)
        with allure.step(f"Navigate to {locale['base_url']} before accepting cookies"):
            footer.navigate(locale["base_url"])
        button_text = footer.get_cookie_accept_button_text()
        with allure.step(f"Assert cookie button contains '{locale['cookie_accept_text']}'"):
            assert locale["cookie_accept_text"] in button_text, (
                f"Expected '{locale['cookie_accept_text']}' in button text, got '{button_text}'"
            )
