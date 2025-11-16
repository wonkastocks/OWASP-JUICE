#!/usr/bin/env python3
"""
Check if Cloudflare WAF is blocking XSS attempts
"""

import requests
from urllib.parse import quote

print("="*60)
print("🔍 CHECKING CLOUDFLARE WAF BEHAVIOR")
print("="*60)

base_url = "https://juice3.wonkatech.org"

# Test various XSS payloads
test_payloads = [
    ("Plain text", "test"),
    ("Script tags", "<script>alert(1)</script>"),
    ("IMG onerror", "<img src=x onerror=alert(1)>"),
    ("Iframe javascript", "<iframe src='javascript:alert(1)'>"),
    ("SVG onload", "<svg onload=alert(1)>"),
    ("Body onload", "<body onload=alert(1)>"),
]

print("\nTesting various payloads through Cloudflare:\n")

for name, payload in test_payloads:
    encoded = quote(payload)
    url = f"{base_url}/rest/products/search?q={encoded}"
    
    try:
        r = requests.get(url, timeout=5, verify=False)
        
        # Check for Cloudflare blocking indicators
        cf_blocked = False
        if r.status_code == 403:
            cf_blocked = "Cloudflare Block (403)"
        elif "cf-ray" in r.headers and r.status_code == 500:
            cf_blocked = "Server Error (500)"
        elif "cf-ray" in r.headers and r.status_code == 200:
            # Check if response is empty or filtered
            if len(r.text) < 50:
                cf_blocked = "Filtered (empty response)"
            else:
                cf_blocked = "Passed through (200)"
        
        print(f"{name:20} → Status: {r.status_code}, CF: {cf_blocked}")
        
        # Check for Cloudflare challenge
        if "Cloudflare" in r.text and "Ray ID" in r.text:
            print(f"  ⚠️  Cloudflare challenge page detected!")
            
    except Exception as e:
        print(f"{name:20} → Error: {str(e)}")

print("\n" + "="*60)
print("💡 CLOUDFLARE WAF ANALYSIS")
print("="*60)

print("""
Based on the results above:

1. If you see 403 errors → Cloudflare WAF is blocking
2. If you see 500 errors → Application server is blocking
3. If you see 200 with data → Request passed through

CLOUDFLARE WAF SETTINGS TO CHECK:
==================================
1. Log into Cloudflare Dashboard
2. Go to Security → WAF
3. Check these settings:
   - Security Level (should be Low/Essentially Off for CTF)
   - Browser Integrity Check (disable for testing)
   - OWASP ModSecurity Core Rule Set (disable for XSS)
   - Managed Rules (disable XSS rules)

QUICK FIX - BYPASS CLOUDFLARE:
===============================
1. Add a "grey cloud" DNS record (no proxy):
   - juice-direct.wonkatech.org → 155.138.197.128 (DNS only)
   
2. Or use direct IP access:
   - http://155.138.197.128:3000 (if port is open)

3. Or create Page Rule in Cloudflare:
   - URL: juice3.wonkatech.org/*
   - Security Level: Off
   - WAF: Off
   - Browser Integrity Check: Off

THE REAL ISSUE:
===============
The 500 errors are likely from:
- Juice Shop application itself (intentional filtering)
- NOT Cloudflare (would be 403 or challenge page)

But Cloudflare COULD be sanitizing the payloads before
they reach your server, causing different behavior.
""")

if __name__ == "__main__":
    print("\nTo bypass Cloudflare completely:")
    print("1. Set DNS to 'DNS only' (grey cloud) in Cloudflare")
    print("2. Access via: http://juice3.wonkatech.org")
    print("3. Or set up juice-raw.wonkatech.org without proxy")