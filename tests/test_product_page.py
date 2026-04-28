import allure

from pages.product_page import ProductPage


@allure.feature("Product Page")
class TestProductPage:

    @allure.story("Currency symbol")
    def test_currency_symbol_correct(self, page, locale):
        """TC-PP-01: Currency symbol in price matches locale config."""
        product = ProductPage(page)
        with allure.step(f"Navigate to {locale['billy_url']}"):
            product.navigate(locale["billy_url"])
            product.wait_for_page_load()
        price_text = product.get_price_text()
        symbol = product.get_currency_symbol(price_text)
        with allure.step(f"Assert currency symbol is '{locale['currency_symbol']}'"):
            assert symbol == locale["currency_symbol"], (
                f"Expected symbol '{locale['currency_symbol']}', got '{symbol}' from '{price_text}'"
            )

    @allure.story("Price format")
    def test_price_format_correct(self, page, locale):
        """TC-PP-02: Price uses correct decimal separator and symbol position."""
        product = ProductPage(page)
        with allure.step(f"Navigate to {locale['billy_url']}"):
            product.navigate(locale["billy_url"])
            product.wait_for_page_load()
        price_text = product.get_price_text()
        with allure.step(f"Assert decimal separator '{locale['decimal_separator']}' in price"):
            if price_text.endswith(":-"):
                # Swedish round-number format (e.g. "699:-") has no decimal component.
                # The decimal separator (,) only appears when cents are shown ("699,50 kr").
                pass
            else:
                assert locale["decimal_separator"] in price_text, (
                    f"Expected decimal separator '{locale['decimal_separator']}' in '{price_text}'"
                )
        symbol = locale["currency_symbol"]
        stripped = price_text.strip()
        with allure.step(f"Assert symbol position is '{locale['symbol_position']}'"):
            if locale["symbol_position"] == "leading":
                assert stripped.startswith(symbol), (
                    f"Expected leading symbol '{symbol}' in '{stripped}'"
                )
            else:
                assert stripped.endswith(symbol), (
                    f"Expected trailing symbol '{symbol}' in '{stripped}'"
                )

    @allure.story("Dimensions unit")
    def test_dimensions_in_correct_units(self, page, locale):
        """TC-PP-03: Product dimensions text contains the locale unit."""
        product = ProductPage(page)
        with allure.step(f"Navigate to {locale['billy_url']}"):
            product.navigate(locale["billy_url"])
            product.wait_for_page_load()
        unit = product.get_dimension_unit()
        with allure.step(f"Assert dimension unit is '{locale['unit']}'"):
            assert unit == locale["unit"], (
                f"Expected unit '{locale['unit']}', got '{unit}'"
            )

    @allure.story("Add to cart button language")
    def test_add_to_cart_button_language(self, page, locale):
        """TC-PP-04: Add-to-cart button text matches locale config."""
        product = ProductPage(page)
        with allure.step(f"Navigate to {locale['billy_url']}"):
            product.navigate(locale["billy_url"])
            product.wait_for_page_load()
        button_text = product.get_add_to_cart_text()
        with allure.step(f"Assert button contains '{locale['add_to_cart_text']}'"):
            assert locale["add_to_cart_text"] in button_text, (
                f"Expected '{locale['add_to_cart_text']}' in '{button_text}'"
            )

