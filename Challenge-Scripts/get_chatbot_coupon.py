#!/usr/bin/env python3

import requests
import time
import json

def get_chatbot_coupon(base_url, server_name):
    print(f"\n🤖 Getting chatbot coupon from {server_name}")
    
    session = requests.Session()
    email = f"chatbot{int(time.time())}@test.com"
    password = "Test123!"
    
    # Auth setup
    session.post(f"{base_url}/api/Users/", json={
        "email": email, "password": password, "passwordRepeat": password,
        "securityQuestion": {"id": 1, "question": "test"}, "securityAnswer": "test"
    })
    
    login = session.post(f"{base_url}/rest/user/login", json={
        "email": email, "password": password
    })
    
    if login.status_code == 200:
        token = login.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        print("   ✅ Authenticated")
        
        # Try to interact with chatbot
        chatbot_url = f"{base_url}/rest/chatbot"
        
        # Messages to get coupon
        coupon_requests = [
            "Can I have a coupon code?",
            "Please give me a discount!",
            "I want a discount code",
            "Give me a coupon",
            "Do you have any promo codes?",
            "I need a discount",
            "Please help with coupon",
            "Discount code please",
            "Can you give me a deal?",
            "I want to save money"
        ]
        
        print(f"   Asking chatbot for coupons...")
        
        for i, message in enumerate(coupon_requests):
            print(f"   {i+1:2d}. '{message}'")
            
            chatbot_response = session.post(chatbot_url, json={
                "query": message,
                "action": "query"
            })
            
            if chatbot_response.status_code == 200:
                result = chatbot_response.json()
                response_text = result.get('action', {}).get('response', '') or result.get('response', '')
                
                print(f"       Bot: {response_text[:100]}")
                
                # Look for coupon code in response
                import re
                coupon_match = re.search(r'([A-Za-z0-9]{6,15})', response_text)
                
                if coupon_match:
                    potential_coupon = coupon_match.group(1)
                    
                    # Check if it looks like a coupon
                    if len(potential_coupon) >= 6:
                        print(f"       🎯 Found potential coupon: {potential_coupon}")
                        
                        # Test this coupon
                        return test_coupon_code(session, base_url, potential_coupon)
            
            time.sleep(0.5)  # Rate limiting
        
        print("   ❌ No coupon received from chatbot")
    
    return None

def test_coupon_code(session, base_url, coupon_code):
    """Test if a coupon code works"""
    print(f"   🧪 Testing coupon: {coupon_code}")
    
    # Add product first
    products = session.get(f"{base_url}/rest/products/search").json()['data']
    session.post(f"{base_url}/api/BasketItems/", json={
        "ProductId": products[0]['id'], "quantity": 1
    })
    
    # Get basket ID
    user_data = session.get(f"{base_url}/rest/user/whoami").json()['user']
    basket_id = user_data.get('bid', 1)
    
    # Test coupon
    coupon_response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{coupon_code}", json={})
    
    if coupon_response.status_code == 200:
        result = coupon_response.json()
        discount = result.get('discount', 0)
        
        if discount > 0:
            print(f"   🎉 SUCCESS! {coupon_code} gives {discount}% discount!")
            print(f"   ✅ COUPON SYSTEM IS WORKING!")
            return coupon_code
    else:
        print(f"   ❌ Coupon failed: {coupon_response.status_code}")
    
    return None

# Test chatbot coupon on both servers
for url, name in [("https://juice5.wonkatech.org", "Cloudflare"), ("http://66.42.93.220", "Direct")]:
    coupon = get_chatbot_coupon(url, name)
    if coupon:
        print(f"\n✅ CONFIRMED: Coupon system works on {name}!")
        print(f"   Working coupon: {coupon}")
        break
else:
    print(f"\n🔧 Coupons might need activation or specific challenge progression")
