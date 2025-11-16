#!/usr/bin/env python3

import requests
import time

def get_chatbot_coupon_and_enable(base_url):
    print(f"🤖 Attempting to get chatbot coupon to enable system...")
    print(f"Target: {base_url}")
    
    session = requests.Session()
    email = f"enabler{int(time.time())}@test.com"
    password = "Test123!"
    
    # Auth
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
        
        # Navigate to chatbot page first
        print("🤖 Interacting with chatbot...")
        
        # More persistent chatbot interaction
        coupon_requests = [
            "Hello", "Hi there", "I need help",
            "Can I have a coupon?", "I want a discount", "Give me a coupon code",
            "Please give me a discount!", "I need a promo code", "Do you have coupons?",
            "Discount please", "I want to save money", "Give me a deal",
            "Coupon code please", "I want a coupon", "Help me with discount",
            "Please help with coupon", "I really need a discount", "Come on, just one coupon",
            "Pretty please with sugar on top", "I'll be your best friend", "Just a small discount?",
        ]
        
        for i, message in enumerate(coupon_requests):
            print(f"   {i+1:2d}/20: {message}")
            
            # Try different chatbot endpoints
            for chatbot_url in [f"{base_url}/rest/chatbot", f"{base_url}/api/chatbot"]:
                try:
                    chatbot_response = session.post(chatbot_url, json={
                        "query": message
                    })
                    
                    if chatbot_response.status_code == 200:
                        result = chatbot_response.json()
                        
                        # Extract response text
                        response_text = ""
                        if isinstance(result, dict):
                            response_text = (result.get('action', {}).get('response', '') or 
                                           result.get('response', '') or
                                           result.get('answer', '') or 
                                           str(result))
                        else:
                            response_text = str(result)
                        
                        print(f"       Bot: {response_text[:80]}...")
                        
                        # Look for coupon codes in response
                        import re
                        
                        # Pattern for coupon codes
                        coupon_patterns = [
                            r'([A-Za-z0-9]{6,15})',  # Generic alphanumeric
                            r'([A-Z0-9]{6,12})',     # Caps and numbers
                            r'([a-z85!@#$%^&*()]{6,12})',  # z85 characters
                        ]
                        
                        for pattern in coupon_patterns:
                            matches = re.findall(pattern, response_text)
                            for match in matches:
                                if len(match) >= 6 and match not in ['challenge', 'discount', 'message']:
                                    print(f"       🎯 Potential coupon found: {match}")
                                    
                                    # Test this coupon immediately
                                    if test_coupon(session, base_url, match):
                                        return match
                        
                        break  # If one endpoint works, don't try others
                
                except Exception as e:
                    continue
            
            time.sleep(0.3)  # Rate limiting
            
            # Show progress
            if i >= 15:  # After 15 attempts, get more aggressive
                break
        
        print("   ❌ No valid coupon received from chatbot")
    
    return None

def test_coupon(session, base_url, coupon_code):
    """Quick coupon test"""
    try:
        # Ensure we have products in basket
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
                print(f"       ✅ COUPON SYSTEM NOW ENABLED!")
                return True
        
    except Exception as e:
        pass
    
    return False

# Test the restarted container
success = get_chatbot_coupon_and_enable("http://155.138.197.128:3005")

if success:
    print(f"\n🎉 SUCCESS! Coupon system is now working!")
else:
    print(f"\n🔧 Coupon system still not responding")
    print(f"   This may be a v18.0.0 breaking change")
    print(f"   Or require specific Juice Shop version/configuration")

