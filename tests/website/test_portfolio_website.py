import pytest
import urllib.request
import ssl
from playwright.sync_api import sync_playwright

URL = "https://sarveshworks.vercel.app"

def test_live_website_http_status():
    ctx = ssl.create_default_context()
    req = urllib.request.Request(URL, headers={"User-Agent": "Antigravity-QA/1.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        assert resp.getcode() == 200, f"Expected HTTP 200, got {resp.getcode()}"

def test_playwright_modal_interaction():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(URL, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(500)
        
        # Test Modal 1 (Titan)
        page.evaluate("() => window.openProjectModal(1)")
        page.wait_for_timeout(500)
        assert page.locator("#modal-project").is_visible(), "Modal did not open for Project 1"
        body_text = page.locator("#project-modal-body").inner_text()
        assert "Titan" in body_text, "Modal body missing Titan content"
        
        # Test Modal 2 (Universal Engine)
        page.evaluate("() => window.openProjectModal(2)")
        page.wait_for_timeout(500)
        assert page.locator("#modal-project").is_visible(), "Modal did not open for Project 2"
        body_text_2 = page.locator("#project-modal-body").inner_text()
        assert "Universal" in body_text_2, "Modal body missing Universal Engine content"

        # Test Modal 3 (Retail FP&A)
        page.evaluate("() => window.openProjectModal(3)")
        page.wait_for_timeout(500)
        assert page.locator("#modal-project").is_visible(), "Modal did not open for Project 3"
        body_text_3 = page.locator("#project-modal-body").inner_text()
        assert "Retail" in body_text_3, "Modal body missing Retail content"
        
        browser.close()
