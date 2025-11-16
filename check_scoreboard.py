#!/usr/bin/env python3
"""
Check the scoreboard to see challenge status
"""

from playwright.sync_api import sync_playwright
import time

TARGET = "http://66.42.93.220:3000"

def check_scoreboard():
    """Check the scoreboard for challenge status"""
    
    print("📊 CHECKING SCOREBOARD")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser
        page = browser.new_page()
        
        # Navigate to scoreboard
        print("📍 Navigating to scoreboard...")
        page.goto(f"{TARGET}/#/score-board", wait_until="networkidle", timeout=30000)
        time.sleep(3)
        
        # Take screenshot
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/scoreboard_status.png", full_page=True)
        print("📸 Screenshot saved: scoreboard_status.png")
        
        # Look for Mass Dispel challenge
        print("\n🔍 Looking for Mass Dispel challenge status...")
        
        # Find all challenge rows
        challenge_rows = page.locator('mat-row, tr').all()
        print(f"   Found {len(challenge_rows)} challenge rows")
        
        # Look specifically for Mass Dispel
        mass_dispel_found = False
        for row in challenge_rows:
            try:
                text = row.inner_text()
                if 'Mass Dispel' in text:
                    print(f"\n   Found Mass Dispel row:")
                    print(f"   {text}")
                    
                    # Check if it has a checkmark or solved indicator
                    checkmark = row.locator('.fa-check, .solved-badge, [class*="solved"]').first
                    if checkmark.is_visible():
                        print("   ✅ Mass Dispel is marked as SOLVED (green checkmark)")
                    else:
                        print("   ❌ Mass Dispel is NOT marked as solved")
                    
                    mass_dispel_found = True
                    break
            except:
                pass
        
        if not mass_dispel_found:
            print("   Mass Dispel challenge not found in scoreboard")
        
        # Count solved challenges
        print("\n📊 Counting solved challenges...")
        solved_indicators = page.locator('.fa-check, .solved-badge, [class*="solved"]').all()
        print(f"   Total solved: {len(solved_indicators)}")
        
        # Get challenge categories
        print("\n📂 Challenge categories on scoreboard:")
        categories = page.locator('.challenge-category, mat-expansion-panel').all()
        for cat in categories[:5]:  # Show first 5 categories
            try:
                print(f"   - {cat.inner_text()[:50]}")
            except:
                pass
        
        browser.close()
    
    print("\n✅ Check complete. See scoreboard_status.png for full view")

if __name__ == "__main__":
    check_scoreboard()