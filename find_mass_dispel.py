#!/usr/bin/env python3
"""
Find and solve Mass Dispel challenge on the scoreboard
"""

from playwright.sync_api import sync_playwright
import time

TARGET = "http://66.42.93.220:3000"

def find_and_solve_mass_dispel():
    """Find Mass Dispel on scoreboard and solve it"""
    
    print("🔍 FINDING MASS DISPEL CHALLENGE")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser
        page = browser.new_page()
        
        # Navigate to scoreboard
        print("📍 Navigating to scoreboard...")
        page.goto(f"{TARGET}/#/score-board", wait_until="networkidle", timeout=30000)
        time.sleep(3)
        
        # Dismiss cookie consent if present
        print("🍪 Dismissing cookie consent...")
        try:
            cookie_btn = page.locator('button:has-text("dismiss"), a:has-text("Me want it"), button:has-text("Me want it")').first
            if cookie_btn.is_visible():
                cookie_btn.click()
                print("   ✅ Dismissed cookie consent")
                time.sleep(1)
        except:
            pass
        
        # Expand all categories to find Mass Dispel
        print("\n📂 Expanding challenge categories...")
        
        # Click on Miscellaneous category since Mass Dispel is likely there
        categories = [
            "Miscellaneous",
            "Shenanigans", 
            "Brute Force",
            "All"
        ]
        
        for cat in categories:
            try:
                cat_button = page.locator(f'button:has-text("{cat}"), mat-panel-title:has-text("{cat}")').first
                if cat_button.is_visible():
                    cat_button.click()
                    print(f"   Clicked {cat} category")
                    time.sleep(1)
            except:
                pass
        
        # Scroll to find Mass Dispel
        print("\n🔍 Searching for Mass Dispel challenge...")
        
        # Scroll down the page to load all challenges
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        
        # Look for Mass Dispel
        mass_dispel = page.locator('text="Mass Dispel"').first
        if mass_dispel.is_visible():
            print("   ✅ Found Mass Dispel challenge!")
            
            # Check if it has a checkmark (solved)
            parent = mass_dispel.locator('..')
            checkmark = parent.locator('.fa-check, .solved-icon, [class*="solved"]').first
            
            if checkmark.is_visible():
                print("   ✅ Mass Dispel is already marked as SOLVED (green)")
            else:
                print("   ❌ Mass Dispel is NOT solved (no checkmark)")
                
                # Check for hint button
                hint_btn = parent.locator('button:has-text("Hint"), .hint-button').first
                if hint_btn.is_visible():
                    print("   💡 Hint button found - challenge is available to solve")
        else:
            print("   ❌ Mass Dispel not visible on current view")
            
            # Try searching for it
            search_box = page.locator('input[type="search"], input[placeholder*="Search"]').first
            if search_box.is_visible():
                print("\n   🔍 Using search to find Mass Dispel...")
                search_box.fill("Mass Dispel")
                time.sleep(2)
                
                # Check if it appears now
                mass_dispel = page.locator('text="Mass Dispel"').first
                if mass_dispel.is_visible():
                    print("   ✅ Found Mass Dispel via search!")
        
        # Take screenshot
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/mass_dispel_status.png", full_page=True)
        print("\n📸 Screenshot saved: mass_dispel_status.png")
        
        # Now try to solve it if not solved
        if mass_dispel.is_visible():
            parent = mass_dispel.locator('..')
            checkmark = parent.locator('.fa-check, .solved-icon').first
            
            if not checkmark.is_visible():
                print("\n🎯 Attempting to solve Mass Dispel...")
                print("   Mass Dispel requires dismissing multiple notifications at once")
                
                # Open multiple challenges in new tabs to trigger notifications
                print("   Opening multiple challenge pages...")
                
                # Challenges that will trigger notifications when solved
                easy_challenges = [
                    f"{TARGET}/#/administration",  # Admin Section
                    f"{TARGET}/#/web3",  # Web3 Sandbox  
                    f"{TARGET}/assets/public/images/uploads/%F0%9F%98%BC-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg",  # Missing Encoding
                ]
                
                # Open each in rapid succession
                for url in easy_challenges:
                    page.goto(url, wait_until="domcontentloaded", timeout=3000)
                    time.sleep(0.5)
                
                # Wait for notifications
                time.sleep(2)
                
                # Now press ESC to dismiss all at once
                print("   Pressing ESC to dismiss all notifications...")
                page.keyboard.press("Escape")
                
                print("   ✅ Attempted to solve Mass Dispel")
        
        browser.close()
    
    print("\n✅ Check complete")

if __name__ == "__main__":
    find_and_solve_mass_dispel()