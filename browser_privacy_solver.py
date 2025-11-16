#!/usr/bin/env python3
"""
Browser automation to solve Privacy Policy challenge
Uses Playwright to actually navigate and interact with the page
"""

from playwright.sync_api import sync_playwright
import time

BASE_URL = "http://155.138.197.128:5000"

def solve_privacy_with_browser():
    """Use browser automation to solve Privacy Policy challenge"""
    
    print("🎯 Solving Privacy Policy Challenge with Browser Automation")
    print("="*60)
    
    with sync_playwright() as p:
        # Launch browser (headless=False to see what's happening)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print("\n1️⃣ Navigating to Juice Shop...")
            page.goto(BASE_URL)
            time.sleep(3)
            
            # Dismiss any welcome banner or cookie consent
            try:
                page.click("button:has-text('Dismiss')")
            except:
                pass
            
            try:
                page.click("[aria-label='Close Welcome Banner']")
            except:
                pass
            
            print("\n2️⃣ Looking for Privacy Policy link...")
            
            # Method 1: Try footer link
            try:
                page.click("a:has-text('Privacy')")
                print("   ✅ Clicked Privacy link in footer")
                time.sleep(2)
            except:
                # Method 2: Direct navigation
                print("   Navigating directly to privacy page...")
                page.goto(f"{BASE_URL}/#/privacy-security")
                time.sleep(3)
            
            print("\n3️⃣ Interacting with privacy page...")
            
            # Scroll through the page (often required to trigger the challenge)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            
            # Scroll back up
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(1)
            
            # Try to find and click any privacy-related buttons
            try:
                page.click("button:has-text('Accept')")
                print("   ✅ Clicked Accept button")
            except:
                pass
            
            try:
                page.click("mat-card:has-text('Privacy')")
                print("   ✅ Clicked Privacy card")
            except:
                pass
            
            # Check for success notification
            try:
                success = page.wait_for_selector(".cdk-overlay-container", timeout=5000)
                if success:
                    print("\n✅ Challenge notification appeared!")
            except:
                pass
            
            print("\n4️⃣ Checking scoreboard...")
            page.goto(f"{BASE_URL}/#/score-board")
            time.sleep(3)
            
            # Look for Privacy Policy challenge status
            try:
                privacy_elements = page.query_selector_all("mat-row:has-text('Privacy Policy')")
                for element in privacy_elements:
                    text = element.inner_text()
                    if "✓" in text or "solved" in text.lower():
                        print("   ✅ Privacy Policy challenge SOLVED!")
                    else:
                        print("   ❓ Privacy Policy status unclear")
            except:
                pass
            
        finally:
            browser.close()
    
    print("\n" + "="*60)
    print("📝 If not solved, try manually:")
    print("1. Open: http://155.138.197.128:5000/#/privacy-security")
    print("2. Read through the entire page")
    print("3. Scroll to the very bottom")
    print("4. Look for any 'Accept' or 'I have read' buttons")
    print("5. The challenge should trigger")
    print("="*60)

if __name__ == "__main__":
    try:
        solve_privacy_with_browser()
    except Exception as e:
        print(f"\n❌ Browser automation failed: {e}")
        print("\n💡 Alternative: Use Selenium or manual browsing")
        print("   pip install playwright")
        print("   playwright install chromium")