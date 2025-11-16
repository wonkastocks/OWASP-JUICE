#!/usr/bin/env python3
"""
WAF Comparison Test - Cloudflare vs Direct Server
=================================================
Test if Cloudflare WAF is blocking coupon requests
"""

import requests
import time

def test_server(base_url, server_name):
    print(f"\n🔍 Testing {server_name}: {base_url}")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    })
    
    # Quick auth
    email = f"waftest{int(time.time())}@test.com"
    password = "Test123!"
    
    # Register
    register_response = session.post(f"{base_url}/api/Users/", json={
        "email": email,
        "password": password,
        "passwordRepeat": password,
        "securityQuestion": {"id": 1, "question": "test"},
        "securityAnswer": "test"
    })
    print(f"   Registration: {register_response.status_code}")
    
    # Login
    login_response = session.post(f"{base_url}/rest/user/login", json={
        "email": email,
        "password": password
    })
    
    if login_response.status_code == 200:
        token = login_response.json()['authentication']['token']
        session.headers['Authorization'] = f'Bearer {token}'
        print(f"   Login: ✅ Success")
        
        # Add product
        products = session.get(f"{base_url}/rest/products/search").json()['data']
        session.post(f"{base_url}/api/BasketItems/", json={
            "ProductId": products[0]['id'],
            "quantity": 1
        })
        
        # Get basket ID
        user_data = session.get(f"{base_url}/rest/user/whoami").json()['user']
        basket_id = user_data.get('bid', 1)
        
        # Test coupon API
        test_codes = ["TEST123", "INVALID", "' OR '1'='1' --"]
        
        for code in test_codes:
            coupon_response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{code}", json={})
            print(f"   Coupon '{code}': HTTP {coupon_response.status_code}")
            
            if coupon_response.status_code not in [404]:
                print(f"      Response: {coupon_response.text[:100]}")
    
    else:
        print(f"   Login failed: {login_response.status_code}")

# Test both servers
test_server("https://juice5.wonkatech.org", "Cloudflare (juice5)")
test_server("http://66.42.93.220", "Direct Server")
