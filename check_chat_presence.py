#!/usr/bin/env python3
"""
Check if chat functionality exists on the Juice Shop website
"""

from playwright.sync_api import sync_playwright
import time

TARGET = "http://66.42.93.220:3000"

print("🔍 CHECKING FOR CHAT FUNCTIONALITY")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("📍 Loading Juice Shop...")
    page.goto(TARGET, wait_until="networkidle", timeout=30000)
    time.sleep(5)  # Wait for any dynamic content
    
    # Take a full page screenshot
    page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/full_page_check.png", full_page=True)
    print("📸 Full page screenshot saved")
    
    # Look for any chat-related elements
    print("\n🔍 Searching for chat elements...")
    
    # Get all button elements
    buttons = page.locator('button').all()
    print(f"   Found {len(buttons)} buttons total")
    
    # Check for chat-related buttons
    chat_found = False
    for i, button in enumerate(buttons):
        try:
            text = button.inner_text()
            aria = button.get_attribute('aria-label') or ''
            tooltip = button.get_attribute('mattooltip') or ''
            
            if any(word in (text + aria + tooltip).lower() for word in ['chat', 'support', 'help', 'contact']):
                print(f"   Button {i}: Text='{text}', Aria='{aria}', Tooltip='{tooltip}'")
                chat_found = True
        except:
            pass
    
    # Look for mat-icons
    print("\n🔍 Searching for mat-icon elements...")
    icons = page.locator('mat-icon').all()
    print(f"   Found {len(icons)} mat-icons")
    
    for icon in icons:
        try:
            text = icon.inner_text()
            if any(word in text.lower() for word in ['chat', 'support', 'help', 'contact', 'message']):
                print(f"   Icon found: {text}")
                chat_found = True
        except:
            pass
    
    # Check page source for chat references
    print("\n🔍 Checking page source for chat references...")
    page_source = page.content()
    
    chat_indicators = [
        'chatbot', 'chat-button', 'support-chat', 'live-chat',
        'tawk.to', 'intercom', 'zendesk', 'freshchat', 'crisp',
        '/chatbot', 'ChatbotComponent'
    ]
    
    for indicator in chat_indicators:
        if indicator.lower() in page_source.lower():
            print(f"   Found reference to: {indicator}")
            chat_found = True
    
    # Check for iframes (chat widgets often in iframes)
    print("\n🔍 Checking for iframes...")
    iframes = page.locator('iframe').all()
    print(f"   Found {len(iframes)} iframes")
    
    for iframe in iframes:
        try:
            src = iframe.get_attribute('src') or ''
            if 'chat' in src.lower() or 'support' in src.lower():
                print(f"   Chat iframe found: {src}")
                chat_found = True
        except:
            pass
    
    # Navigate to specific chatbot route
    print("\n🔍 Checking /chatbot route...")
    page.goto(f"{TARGET}/#/chatbot", wait_until="domcontentloaded", timeout=15000)
    time.sleep(3)
    
    # Take screenshot of chatbot page
    page.screenshot(path="/Users/walterbarr_1/sql-injection-lab/chatbot_route.png")
    print("📸 Chatbot route screenshot saved")
    
    # Check if chatbot page has content
    chatbot_content = page.content()
    if 'chat' in chatbot_content.lower():
        print("   ✅ Chatbot route exists and has content")
        
        # Look for input fields on chatbot page
        inputs = page.locator('input').all()
        print(f"   Found {len(inputs)} input fields on chatbot page")
    else:
        print("   ❌ Chatbot route may not be functional")
    
    browser.close()

if chat_found:
    print("\n✅ Chat functionality indicators found")
else:
    print("\n⚠️ No obvious chat functionality found")
    print("\n💡 Possibilities:")
    print("   1. Chat feature may be disabled in this instance")
    print("   2. Chat button might only appear for logged-in users")
    print("   3. Chat functionality might be at a specific route like /#/chatbot")

print("\n📊 Check screenshots:")
print("   - full_page_check.png: Full page view")
print("   - chatbot_route.png: Direct chatbot route")
