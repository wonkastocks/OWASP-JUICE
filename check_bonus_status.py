#!/usr/bin/env python3
"""
Check the actual status of the Bonus Payload challenge
"""

import requests
import json

BASE_URL = "http://155.138.197.128:5000"

def check_challenge_status():
    """Check all challenges and specifically look for bonus payload"""
    
    session = requests.Session()
    
    print("🔍 Checking Challenge Status\n")
    print("="*60)
    
    # Get all challenges
    r = session.get(f"{BASE_URL}/api/Challenges")
    
    if r.status_code == 200:
        challenges = r.json()['data']
        
        # Stats
        total = len(challenges)
        solved = len([c for c in challenges if c['solved']])
        
        print(f"📊 Overall: {solved}/{total} challenges solved\n")
        
        # Look for XSS and bonus challenges
        print("🎯 XSS & Bonus Challenges:")
        print("-"*60)
        
        xss_challenges = []
        for c in challenges:
            if 'xss' in c.get('key', '').lower() or 'bonus' in c.get('name', '').lower() or c.get('category') == 'XSS':
                xss_challenges.append(c)
                status = "✅" if c['solved'] else "❌"
                print(f"{status} {c['name']}")
                print(f"   Key: {c.get('key')}")
                print(f"   Category: {c.get('category')}")
                print(f"   Difficulty: {c.get('difficulty')}⭐")
                if not c['solved']:
                    print(f"   Description: {c.get('description', 'N/A')[:100]}...")
                    hint = c.get('hint')
                    if hint:
                        print(f"   Hint: {hint}")
                print()
        
        # Check for the specific bonus payload challenge
        bonus_challenge = None
        for c in challenges:
            if c.get('key') == 'xssBonusChallenge' or 'bonus payload' in c.get('name', '').lower():
                bonus_challenge = c
                break
        
        if bonus_challenge:
            print("="*60)
            print("🎁 BONUS PAYLOAD CHALLENGE DETAILS:")
            print("="*60)
            print(json.dumps(bonus_challenge, indent=2))
            
            if not bonus_challenge['solved']:
                print("\n⚠️ Challenge is NOT solved despite SoundCloud player appearing!")
                print("\n🔧 Possible issues:")
                print("1. The challenge detection might be looking for a specific event")
                print("2. The payload might need to be entered in a specific way")
                print("3. There might be a timing issue with the challenge detection")
                
                print("\n💡 Try these alternatives:")
                print("1. Refresh the page and try again")
                print("2. Log in first, then inject the payload")
                print("3. Try injecting through different input fields")
                print("4. Check browser console for any errors")
        
        # Also check continue code
        print("\n🔐 Checking for continue code...")
        r2 = session.get(f"{BASE_URL}/rest/continue-code/apply/bonus")
        r3 = session.post(f"{BASE_URL}/rest/continue-code", json={"continueCode": "xss-bonus"})
        
    else:
        print(f"❌ Failed to get challenges: {r.status_code}")
    
    print("\n="*60)
    print("🔗 Direct links to try:")
    print(f"1. Search with payload: {BASE_URL}/#/search")
    print(f"2. Score board: {BASE_URL}/#/score-board")
    print(f"3. Admin panel: {BASE_URL}/#/administration")

if __name__ == "__main__":
    check_challenge_status()