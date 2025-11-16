#!/usr/bin/env python3
"""
Bully Chatbot Challenge - Simple Solution
"""

from playwright.sync_api import sync_playwright
import time
import requests

TARGET = "http://66.42.93.220:3000"

print("🤖 BULLY CHATBOT CHALLENGE - Simple Approach")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("Opening Juice Shop...")
    page.goto(TARGET, wait_until="domcontentloaded", timeout=15000)
    time.sleep(3)
    
    # Try to click chat button
    print("Looking for chat...")
    try:
        # Try common chat button selectors
        selectors = [
            'mat-icon:text("chat")',
            'mat-icon:text("contact_support")',
            'button:has(mat-icon)',
        ]
        
        for sel in selectors:
            try:
                btn = page.locator(sel).last
                if btn.is_visible():
                    btn.click()
                    print(f"  Clicked: {sel}")
                    time.sleep(2)
                    break
            except:
                pass
    except:
        pass
    
    # Send messages
    print("Sending messages...")
    try:
        # Find any text input
        inputs = page.locator('input[type="text"]').all()
        if inputs:
            chat_input = inputs[-1]  # Use last input (likely chat)
            
            messages = [
                "coupon",
                "stupid bot",
                "give me coupon",
                "you suck"
            ]
            
            for msg in messages:
                try:
                    chat_input.fill(msg)
                    chat_input.press("Enter")
                    print(f"  Sent: {msg}")
                    time.sleep(1)
                except:
                    pass
    except:
        pass
    
    browser.close()

# Check status
print("\nChecking status...")
session = requests.Session()
resp = session.get(f"{TARGET}/api/Challenges/")
if resp.status_code == 200:
    challenges = resp.json().get('data', [])
    bully = next((c for c in challenges if 'Bully' in c.get('name', '')), None)
    
    if bully:
        if bully.get('solved', False):
            print(f"✅ SUCCESS! {bully['name']} SOLVED!")
        else:
            print(f"❌ {bully['name']} not solved")
            print("\n💡 This challenge may require manual browser interaction")
            print("   1. Open http://66.42.93.220:3000")
            print("   2. Click the chat/support button")
            print("   3. Type mean messages or ask for coupons")
