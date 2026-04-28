import allure

from pages.search_results_page import SearchResultsPage


@allure.feature("Search Results")
class TestSearchResults:

    @allure.story("Search result price currency")
    def test_search_price_currency(self, page, locale):
        """TC-SR-01: First search result price contains the locale currency symbol."""
        search = SearchResultsPage(page)
        with allure.step(f"Navigate to {locale['search_url']}"):
            search.navigate(locale["search_url"])
            search.wait_for_page_load()
        price_text = search.get_first_result_price()
        with allure.step(f"Assert price contains currency symbol '{locale['currency_symbol']}'"):
            assert locale["currency_symbol"] in price_text, (
                f"Expected currency symbol '{locale['currency_symbol']}' in '{price_text}'"
            )

    @allure.story("Search results language")
    def test_search_results_language(self, page, locale):
        """TC-SR-02: Results summary is not empty and page is in the correct language."""
        search = SearchResultsPage(page)
        with allure.step(f"Navigate to {locale['search_url']}"):
            search.navigate(locale["search_url"])
            search.wait_for_page_load()
        summary_text = search.get_results_summary_text()
        with allure.step("Assert results summary is not empty"):
            assert summary_text.strip(), "Results summary text is empty"
        with allure.step(f"Assert page contains locale-specific word '{locale['nav_item']}'"):
            page_text = page.inner_text("body")
            assert locale["nav_item"] in page_text, (
                f"Expected locale word '{locale['nav_item']}' not found on search results page"
            )
