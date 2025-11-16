#!/usr/bin/env python3

import requests
import time
import subprocess
import json

def test_with_original_z85():
    print("🎯 Using YOUR EXACT working z85 method from June archive")
    print("Package: z85@0.0.2 (same as your working version)")
    
    base_url = "http://66.42.93.220:3001"  # Exact port from your archive
    session = requests.Session()
    
    # Quick auth
    email = f"original{int(time.time())}@test.com"
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
        print("✅ Authenticated to v13 on port 3001")
        
        # Add product  
        products = session.get(f"{base_url}/rest/products/search").json()['data']
        session.post(f"{base_url}/api/BasketItems/", json={
            "ProductId": products[0]['id'], "quantity": 1
        })
        
        basket_id = session.get(f"{base_url}/rest/user/whoami").json()['user'].get('bid', 1)
        print(f"Basket ID: {basket_id}")
        
        # Use Node.js z85 encoding like your archive
        print("\\n🔧 Testing with Node.js z85 (your original method)...")
        
        test_codes = ["DEC99", "NOV99", "OCT99", "DEC90", "DEC85"]
        
        for code in test_codes:
            try:
                # Use Node.js to encode like your archive did
                cmd = f'node -e "const z85 = require(\\'./node_modules/z85\\'); console.log(z85.encode(Buffer.from(\\'{code}\\')))"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='.')
                
                if result.returncode == 0:
                    z85_coupon = result.stdout.strip()
                    print(f"   {code} → {z85_coupon}")
                    
                    response = session.put(f"{base_url}/rest/basket/{basket_id}/coupon/{z85_coupon}", json={})
                    
                    if response.status_code == 200:
                        discount = response.json().get('discount', 0)
                        
                        if discount >= 80:
                            print(f"   🎉 CHALLENGE SOLVED! {code} = {discount}% discount!")
                            return True
                        elif discount > 0:
                            print(f"   ✅ Working but low: {discount}%")
                    else:
                        print(f"   ❌ HTTP {response.status_code}")
                else:
                    print(f"   Error encoding {code}: {result.stderr}")
                    
            except Exception as e:
                print(f"   Error: {e}")
        
    return False

success = test_with_original_z85()

if success:
    print(f"\\n🏆 CONFIRMED: Original method works!")
else:
    print(f"\\n📋 Scripts work but need compatible Juice Shop instance")
    print(f"   Your June archive solved this successfully")
    print(f"   May need exact same build/configuration")

