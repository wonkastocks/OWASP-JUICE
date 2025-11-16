#!/usr/bin/env python3
"""
Check Privacy Policy challenges and their requirements
"""

import requests
import json

BASE_URL = "http://155.138.197.128:5000"

def check_privacy_challenges():
    """Check all privacy-related challenges"""
    
    session = requests.Session()
    
    print("🔍 Checking Privacy-Related Challenges")
    print("="*60)
    
    # Get all challenges
    r = session.get(f"{BASE_URL}/api/Challenges")
    
    if r.status_code == 200:
        challenges = r.json().get('data', [])
        
        # Find privacy-related challenges
        privacy_challenges = []
        for c in challenges:
            if 'privacy' in c.get('name', '').lower() or 'privacy' in c.get('key', '').lower():
                privacy_challenges.append(c)
                status = "✅" if c['solved'] else "❌"
                print(f"\n{status} {c['name']}")
                print(f"   Key: {c.get('key')}")
                print(f"   Category: {c.get('category')}")
                print(f"   Difficulty: {c.get('difficulty')}⭐")
                print(f"   Description: {c.get('description', 'N/A')}")
                if c.get('hint'):
                    print(f"   Hint: {c.get('hint')}")
                if not c['solved']:
                    print(f"   Tutorial Order: {c.get('tutorialOrder', 'N/A')}")
        
        print("\n" + "="*60)
        print(f"Found {len(privacy_challenges)} privacy-related challenges")
        
        # Specific check for the unsolved one
        for c in privacy_challenges:
            if not c['solved']:
                print(f"\n🎯 To solve '{c['name']}':")
                
                if 'privacyPolicyChallenge' in c.get('key', ''):
                    print("   1. Go to: http://155.138.197.128:5000")
                    print("   2. Look in the menu (Account -> Privacy & Security)")
                    print("   3. Or check the footer for 'Privacy Policy' link")
                    print("   4. Click and READ the privacy policy page")
                    print("   5. You may need to scroll to the bottom")
                    print("   6. Look for any buttons to acknowledge")
                
                elif 'privacyPolicyProofChallenge' in c.get('key', ''):
                    print("   This is a more advanced challenge")
                    print("   You need to prove you read the privacy policy")
                    print("   Look for specific information in the policy")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    check_privacy_challenges()