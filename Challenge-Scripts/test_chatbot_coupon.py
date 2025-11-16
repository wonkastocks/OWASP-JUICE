#!/usr/bin/env python3

import requests
import time
import re

def get_chatbot_coupon():
    print("🤖 Testing chatbot coupon on unsafe config...")
    
    base_url = "http://66.42.93.220"
    session = requests.Session()
    
    # Auth
    email = f"chattest{int(time.time())}@test.com"
    password = "Test123!"
    
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
        print("✅ Authenticated")
        
        # Test chatbot endpoint
        print("🤖 Testing chatbot interaction...")
        
        discount_requests = [
            "Hello! Can I have a discount?",
            "I need a coupon code please",
            "Give me a discount code",
            "Can you help me save money?",
            "I want a promo code",
            "Please give me a coupon",
            "I really need a discount",
            "Help me with a coupon code",
            "Can I get a special offer?",
            "Do you have any deals?"
        ]
        
        for i, message in enumerate(discount_requests):
            print(f"   {i+1:2d}. {message}")
            
            try:
                chatbot_response = session.post(f"{base_url}/rest/chatbot", json={
                    "query": message
                })
                
                if chatbot_response.status_code == 200:
                    result = chatbot_response.json()
                    
                    # Extract response text
                    response_text = str(result.get('action', {}).get('response', ''))
                    if not response_text:
                        response_text = str(result)
                    
                    print(f"       Response: {response_text[:100]}")
                    
                    # Look for coupon codes
                    coupon_matches = re.findall(r'([A-Za-z0-9+/!@#$%^&*()]{6,15})', response_text)
                    
                    for match in coupon_matches:
                        if match not in ['action', 'response', 'query', 'Hello']:
                            print(f"       🎯 Potential coupon: {match}")
                            
                            # Test it immediately
                            if test_coupon(session, base_url, match):
                                return match
                
            except Exception as e:
                print(f"       Error: {e}")
            
            time.sleep(0.5)
    
    return None

def test_coupon(session, base_url, coupon_code):
    """Test a potential coupon code"""
    try:
        # Add product to basket
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
                print(f"       🎉 WORKING COUPON! {coupon_code} = {discount}% discount!")
                return True
        
    except Exception as e:
        pass
    
    return False

# Test chatbot approach
coupon = get_chatbot_coupon()

if coupon:
    print(f"\n🎉 SUCCESS! Found working coupon: {coupon}")
    print(f"✅ COUPON SYSTEM NOW CONFIRMED WORKING!")
else:
    print(f"\n🔧 Even with unsafe config, chatbot not giving coupons")
    print(f"   This confirms v18.0.0 breaking changes affected coupon system")

