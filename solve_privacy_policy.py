#!/usr/bin/env python3
"""
Solve the Privacy Policy challenge on OWASP Juice Shop
This challenge requires reading the privacy policy
"""

import requests
import time

BASE_URL = "http://155.138.197.128:5000"

def solve_privacy_policy():
    """Solve the Privacy Policy challenge"""
    
    session = requests.Session()
    
    print("🎯 Solving Privacy Policy Challenge")
    print("="*60)
    
    # Method 1: Direct navigation to privacy policy page
    print("\n1️⃣ Accessing privacy policy page...")
    urls = [
        f"{BASE_URL}/#/privacy-security",
        f"{BASE_URL}/#/privacy",
        f"{BASE_URL}/#/privacy-policy",
        f"{BASE_URL}/privacy",
        f"{BASE_URL}/rest/privacy-policy"
    ]
    
    for url in urls:
        try:
            r = session.get(url)
            print(f"   Accessed: {url}")
            if r.status_code == 200:
                print(f"   ✅ Response OK")
            time.sleep(1)
        except:
            pass
    
    # Method 2: Try the privacy-security page with specific actions
    print("\n2️⃣ Accessing privacy-security page with actions...")
    
    # Navigate to the main privacy page
    r = session.get(f"{BASE_URL}/#/privacy-security")
    time.sleep(2)
    
    # Try various privacy-related endpoints
    privacy_endpoints = [
        "/rest/privacy-security",
        "/api/SecurityPolicies",
        "/api/PrivacyRequests",
        "/ftp/legal.md",
        "/assets/public/privacy.txt"
    ]
    
    for endpoint in privacy_endpoints:
        try:
            r = session.get(f"{BASE_URL}{endpoint}")
            if r.status_code == 200:
                print(f"   ✅ Found: {endpoint}")
        except:
            pass
    
    # Method 3: Login and access privacy policy
    print("\n3️⃣ Accessing with authentication...")
    
    # Login first (optional, but might trigger differently)
    login_data = {"email": "test@test.com", "password": "test123"}
    try:
        # Try to register/login
        reg_data = {
            "email": "privacy@test.com",
            "password": "test123",
            "passwordRepeat": "test123",
            "securityQuestion": {"id": 1},
            "securityAnswer": "test"
        }
        session.post(f"{BASE_URL}/api/Users", json=reg_data)
        session.post(f"{BASE_URL}/rest/user/login", json={"email": "privacy@test.com", "password": "test123"})
    except:
        pass
    
    # Access privacy page while logged in
    r = session.get(f"{BASE_URL}/#/privacy-security")
    
    # Check if challenge is solved
    print("\n4️⃣ Checking challenge status...")
    r = session.get(f"{BASE_URL}/api/Challenges")
    if r.status_code == 200:
        challenges = r.json().get('data', [])
        for c in challenges:
            if 'privacy' in c.get('name', '').lower() or 'privacy' in c.get('key', '').lower():
                if c['solved']:
                    print(f"   ✅ {c['name']} - SOLVED!")
                else:
                    print(f"   ❌ {c['name']} - Not solved yet")
    
    print("\n" + "="*60)
    print("📝 Manual Method:")
    print("1. Open browser: http://155.138.197.128:5000")
    print("2. Look for 'Privacy Policy' or 'Privacy & Security' in menu/footer")
    print("3. Click on it and read/scroll through the page")
    print("4. The challenge should trigger when you view the page")
    print("\n💡 Tips:")
    print("- Check the footer links")
    print("- Look in the Account menu")
    print("- Try URL: http://155.138.197.128:5000/#/privacy-security")
    print("- You may need to scroll to the bottom of the page")
    print("="*60)

if __name__ == "__main__":
    solve_privacy_policy()