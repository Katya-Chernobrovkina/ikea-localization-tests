import json
import allure
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright

LOCALES_PATH = Path(__file__).parent.parent / "config" / "locales.json"

with LOCALES_PATH.open(encoding="utf-8") as f:
    ALL_LOCALES = json.load(f)


def pytest_configure(config):
    config.addinivalue_line("markers", "locale: mark test with its target locale code")
    config.addinivalue_line("markers", "no_autouse_cookies: skip automatic cookie acceptance for this test")


@pytest.fixture(params=["de", "us"])
def locale(request):
    """Yields the locale config dict for each parametrized locale."""
    return {"key": request.param, **ALL_LOCALES[request.param]}


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture
def page(browser, locale):
    # Match Accept-Language to locale so server-side redirects behave correctly
    lang_header = locale["html_lang"]
    context = browser.new_context(
        locale=lang_header,
        extra_http_headers={"Accept-Language": f"{lang_header},{lang_header}-{locale['key'].upper()};q=0.9"},
    )
    page = context.new_page()

    # Apply stealth patches to reduce bot-detection fingerprinting
    try:
        from playwright_stealth import Stealth
        Stealth().use_sync(page)
    except (ImportError, AttributeError):
        try:
            from playwright_stealth import stealth_sync
            stealth_sync(page)
        except (ImportError, AttributeError):
            pass  # playwright-stealth is optional; tests still run without it

    yield page

    context.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot = page.screenshot()
            allure.attach(screenshot, name='failure_screenshot',
                          attachment_type=allure.attachment_type.PNG)


@pytest.fixture(autouse=True)
def attach_locale_parameter(locale):
    allure.dynamic.parameter('locale', locale['key'])


@pytest.fixture(autouse=True)
def accept_cookies_before_test(request, page, locale):
    """Navigate to base URL and dismiss cookie banner before every test.

    Tests marked with @pytest.mark.no_autouse_cookies skip this step so they
    can assert on the cookie banner themselves (e.g. TC-FT-02).
    """
    if request.node.get_closest_marker("no_autouse_cookies"):
        return
    from pages.base_page import BasePage

    base = BasePage(page)
    base.navigate(locale["base_url"])
    base.wait_for_page_load()
    base.accept_cookies()
