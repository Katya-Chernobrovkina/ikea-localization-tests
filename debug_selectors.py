"""
Run this script once to discover the real DOM selectors on live IKEA pages.
Usage:  python debug_selectors.py
Output is printed to stdout — copy it and share it to get selector fixes.
"""
import json
from playwright.sync_api import sync_playwright

PAGES = {
    "de_product": "https://www.ikea.com/de/de/p/billy-buecherregal-weiss-00263850/",
    "us_product": "https://www.ikea.com/us/en/p/billy-bookcase-white-20522046/",
    "de_search":  "https://www.ikea.com/de/de/search/?q=sofa",
    "us_search":  "https://www.ikea.com/us/en/search/?q=sofa",
}

COOKIE_SELECTORS = [
    "[data-testid='cookie-accept-all-btn']",
    "button#onetrust-accept-btn-handler",
    "button[class*='accept-all']",
    "button:has-text('Accept all')",
    "button:has-text('Alle Cookies akzeptieren')",
    "button:has-text('Ok')",
]

PROBE_JS = r"""() => {
    function attrs(el) {
        if (!el) return null;
        const a = {};
        for (const attr of el.attributes) a[attr.name] = attr.value;
        return { tag: el.tagName, text: (el.innerText || '').trim().slice(0, 120), attrs: a };
    }

    const out = {};

    // ── Price ────────────────────────────────────────────────────────────────
    const priceSelectors = [
        "[data-testid*='price']", "[data-ref*='price']", "[data-price]",
        "[itemprop='price']", "[class*='pip-price__integer']",
        "[class*='pip-price']", "[class*='price-module']",
    ];
    for (const s of priceSelectors) {
        const el = document.querySelector(s);
        if (el && el.offsetParent !== null) {
            out['price_selector_hit'] = s;
            out['price_element'] = attrs(el);
            break;
        }
    }
    // Fallback: find first short visible element whose text looks like a price
    if (!out['price_selector_hit']) {
        const priceRe = /^\s*[$€£¥]\s*\d|\d\s*[$€£¥]\s*$/;
        for (const el of document.querySelectorAll('span,p,div,strong')) {
            const t = (el.innerText || '').trim();
            if (t && priceRe.test(t) && t.length < 30 && el.offsetParent !== null) {
                out['price_text_fallback'] = t;
                out['price_fallback_element'] = attrs(el);
                break;
            }
        }
    }

    // ── Add-to-cart button ───────────────────────────────────────────────────
    const cartSelectors = [
        "button[data-ref='add-to-cart-btn']", "button[data-ref*='add-to-cart']",
        "button[data-ref*='cart']", "button[aria-label*='cart']",
        "button[aria-label*='Einkaufswagen']", "button[aria-label*='warenkorb']",
        "button:has-text('Add to cart')", "button:has-text('In den Einkaufswagen')",
    ];
    for (const s of cartSelectors) {
        let el;
        try { el = document.querySelector(s); } catch(e) { continue; }
        if (el && el.offsetParent !== null) {
            out['cart_selector_hit'] = s;
            out['cart_element'] = attrs(el);
            break;
        }
    }
    // Dump all visible buttons' text and attributes
    out['all_buttons'] = [];
    for (const b of document.querySelectorAll('button')) {
        if (b.offsetParent !== null) {
            out['all_buttons'].push(attrs(b));
            if (out['all_buttons'].length >= 10) break;
        }
    }

    // ── Dimensions ───────────────────────────────────────────────────────────
    const dimSelectors = [
        "[data-testid*='measurement']", "[data-testid*='dimension']",
        "[data-ref*='measurement']", "[aria-label*='imension']",
        "[aria-label*='Maße']",
    ];
    for (const s of dimSelectors) {
        const el = document.querySelector(s);
        if (el && el.offsetParent !== null) {
            out['dim_selector_hit'] = s;
            out['dim_element'] = attrs(el);
            break;
        }
    }
    // Fallback: find heading with "Maße" / "Measurements" and get its container
    for (const h of document.querySelectorAll('h2,h3,h4,dt,th,strong,b,span')) {
        const t = (h.innerText || '').trim().toLowerCase();
        if (['maße','measurements','dimensions','abmessungen','produktmaße'].includes(t)) {
            const container = h.closest('section,article,dl,table,div') || h.parentElement;
            out['dim_heading_text'] = h.innerText.trim();
            out['dim_heading_element'] = attrs(h);
            out['dim_container_text'] = (container.innerText || '').trim().slice(0, 300);
            out['dim_container_element'] = attrs(container);
            break;
        }
    }

    // ── Search results: price of first card ──────────────────────────────────
    const srPriceSelectors = [
        "[data-testid='search-result-price']", "[data-testid*='price']",
        "[data-ref*='price']", "[itemprop='price']", "[data-price]",
        "[class*='pip-price__integer']", "[class*='pip-price']",
    ];
    for (const s of srPriceSelectors) {
        const el = document.querySelector(s);
        if (el && el.offsetParent !== null) {
            out['sr_price_selector_hit'] = s;
            out['sr_price_element'] = attrs(el);
            break;
        }
    }

    // ── Search results: summary / count ─────────────────────────────────────
    const summarySelectors = [
        "[data-testid='search-results-count']", "[role='status']",
        "[aria-live='polite']", "[aria-live='assertive']",
        "[data-testid*='result']", "[data-testid*='count']",
    ];
    for (const s of summarySelectors) {
        const el = document.querySelector(s);
        if (el) {
            const t = (el.innerText || '').trim();
            if (t) {
                out['summary_selector_hit'] = s;
                out['summary_element'] = attrs(el);
                out['summary_text'] = t.slice(0, 200);
                break;
            }
        }
    }
    // Fallback: find element with a count pattern
    if (!out['summary_selector_hit']) {
        const countRe = /\d+\s+(result|Ergebnis|artikel|item|Treffer)/i;
        for (const el of document.querySelectorAll('p,span,div,h2,h3')) {
            const t = (el.innerText || '').trim();
            if (t && countRe.test(t) && t.length < 150 && el.offsetParent !== null) {
                out['summary_text_fallback'] = t;
                out['summary_fallback_element'] = attrs(el);
                break;
            }
        }
    }

    return out;
}"""


def accept_cookies(page):
    for sel in COOKIE_SELECTORS:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=2000):
                btn.click()
                page.wait_for_timeout(1500)
                return
        except Exception:
            continue


def probe_page(page, name, url):
    print(f"\n{'='*70}")
    print(f"  {name.upper()}  ->  {url}")
    print(f"{'='*70}")
    page.goto(url, wait_until="load")
    page.wait_for_timeout(3000)
    accept_cookies(page)
    page.wait_for_timeout(2000)

    final_url = page.url
    if final_url != url:
        print(f"  !! REDIRECTED TO: {final_url}")

    result = page.evaluate(PROBE_JS)
    print(json.dumps(result, indent=2, ensure_ascii=False))


with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    ctx = browser.new_context()
    pg = ctx.new_page()

    for name, url in PAGES.items():
        probe_page(pg, name, url)

    browser.close()

print("\nDone.")
