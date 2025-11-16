#!/usr/bin/env python3
"""
Find Crypto String in OWASP Juice Shop
=======================================
Common crypto strings in CTF challenges
"""

import requests
import base64
import hashlib
import re
from urllib.parse import unquote

# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_crypto_strings(base_url="https://juice5.wonkatech.org"):
    """
    Search for crypto strings in various locations
    """
    session = requests.Session()
    session.verify = False

    print("[*] Searching for crypto strings...")
    print("="*50)

    crypto_strings = []

    # 1. Check common locations for crypto wallet addresses
    print("\n[1] Checking for Crypto Wallet Addresses...")

    # Bitcoin address pattern
    btc_pattern = r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}'

    # Ethereum address pattern
    eth_pattern = r'0x[a-fA-F0-9]{40}'

    # Check main page
    response = session.get(base_url)

    # Search for crypto addresses
    btc_matches = re.findall(btc_pattern, response.text)
    eth_matches = re.findall(eth_pattern, response.text)

    if btc_matches:
        print(f"[+] Found Bitcoin addresses: {btc_matches}")
        crypto_strings.extend(btc_matches)

    if eth_matches:
        print(f"[+] Found Ethereum addresses: {eth_matches}")
        crypto_strings.extend(eth_matches)

    # 2. Check for encoded strings
    print("\n[2] Checking for Encoded Crypto Strings...")

    # Common locations for hidden strings
    endpoints = [
        "/api/Challenges",
        "/rest/products/search?q=",
        "/api/Users",
        "/api/Feedbacks",
        "/#/about",
        "/#/photo-wall",
        "/api/SecurityQuestions",
        "/api/Complaints",
        "/ftp",
        "/encryptionkeys",
        "/.well-known/security.txt",
        "/robots.txt",
        "/api/Quantitys",  # Typo is intentional - Juice Shop has this
    ]

    for endpoint in endpoints:
        try:
            response = session.get(f"{base_url}{endpoint}")
            if response.status_code == 200:
                text = response.text

                # Look for base64 encoded strings
                base64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
                b64_matches = re.findall(base64_pattern, text)

                for b64_str in b64_matches:
                    try:
                        decoded = base64.b64decode(b64_str).decode('utf-8')
                        if 'crypto' in decoded.lower() or 'wallet' in decoded.lower():
                            print(f"[+] Found base64 crypto string at {endpoint}:")
                            print(f"    Encoded: {b64_str}")
                            print(f"    Decoded: {decoded}")
                            crypto_strings.append(decoded)
                    except:
                        pass

                # Look for hex encoded strings
                hex_pattern = r'[0-9a-fA-F]{32,}'
                hex_matches = re.findall(hex_pattern, text)

                for hex_str in hex_matches:
                    if len(hex_str) % 2 == 0:  # Valid hex should be even length
                        try:
                            decoded = bytes.fromhex(hex_str).decode('utf-8')
                            if 'crypto' in decoded.lower():
                                print(f"[+] Found hex crypto string at {endpoint}:")
                                print(f"    Hex: {hex_str}")
                                print(f"    Decoded: {decoded}")
                                crypto_strings.append(decoded)
                        except:
                            pass

        except Exception as e:
            pass

    # 3. Check JavaScript files
    print("\n[3] Checking JavaScript Files...")

    js_files = [
        "/main.js",
        "/vendor.js",
        "/polyfills.js",
        "/runtime.js",
        "/3rdpartylicenses.txt",
    ]

    for js_file in js_files:
        try:
            response = session.get(f"{base_url}{js_file}")
            if response.status_code == 200:
                # Look for crypto-related strings
                crypto_patterns = [
                    r'["\']([13][a-km-zA-HJ-NP-Z1-9]{25,34})["\']',  # BTC
                    r'["\']0x[a-fA-F0-9]{40}["\']',  # ETH
                    r'crypto["\']?\s*:\s*["\']([^"\']+)["\']',  # crypto key
                    r'wallet["\']?\s*:\s*["\']([^"\']+)["\']',  # wallet
                    r'privateKey["\']?\s*:\s*["\']([^"\']+)["\']',  # private key
                ]

                for pattern in crypto_patterns:
                    matches = re.findall(pattern, response.text)
                    if matches:
                        print(f"[+] Found in {js_file}: {matches}")
                        crypto_strings.extend(matches)

        except:
            pass

    # 4. Check for crypto in comments/reviews
    print("\n[4] Checking Comments and Reviews...")

    try:
        # Get all products
        response = session.get(f"{base_url}/rest/products/search?q=")
        if response.status_code == 200:
            products = response.json()

            for product in products.get('data', []):
                # Get reviews for each product
                product_id = product.get('id')
                review_response = session.get(f"{base_url}/rest/products/{product_id}/reviews")

                if review_response.status_code == 200:
                    reviews = review_response.json()
                    for review in reviews.get('data', []):
                        message = review.get('message', '')
                        if 'crypto' in message.lower() or 'wallet' in message.lower():
                            print(f"[+] Found in review: {message}")
                            crypto_strings.append(message)
    except:
        pass

    # 5. Common Juice Shop crypto challenges
    print("\n[5] Common Juice Shop Crypto Strings...")

    common_crypto = [
        "1AbKfgvw9psQ6NjoyTvEf3HytjZ3Kepme",  # Bitcoin donation address
        "0x0f933ab9fcaaa782d0279c300d73750e1311eae6",  # Ethereum address
        "dash1mzcsj8pby3yg8dkgzsqw8eu5rhjwhygxggr5q5",  # Dash address
        "Lbh qvq frr gur tnzr Pehfgb?",  # ROT13 encoded hint
        "K8Ka6xxFWRkJQp3vbUzwXZZaU9n8AzjU16BpvWR1RKghGYe7hqvqPPwPj8tr",  # Coupon code
    ]

    print("[*] Known Juice Shop crypto strings:")
    for crypto in common_crypto:
        print(f"    - {crypto}")

    # 6. Check for blockchain/NFT related strings
    print("\n[6] Checking for Blockchain/NFT Strings...")

    blockchain_endpoints = [
        "/api/nft",
        "/api/wallet",
        "/api/blockchain",
        "/rest/wallet/balance",
    ]

    for endpoint in blockchain_endpoints:
        try:
            response = session.get(f"{base_url}{endpoint}")
            if response.status_code in [200, 401]:
                print(f"[+] Found blockchain endpoint: {endpoint}")
                if response.status_code == 200:
                    data = response.text
                    # Extract any crypto addresses
                    btc = re.findall(btc_pattern, data)
                    eth = re.findall(eth_pattern, data)
                    if btc:
                        print(f"    BTC: {btc}")
                    if eth:
                        print(f"    ETH: {eth}")
        except:
            pass

    print("\n" + "="*50)
    print("SUMMARY OF CRYPTO STRINGS FOUND:")
    print("="*50)

    if crypto_strings:
        for i, crypto_str in enumerate(set(crypto_strings), 1):
            print(f"{i}. {crypto_str}")
    else:
        print("No crypto strings found automatically.")
        print("\nTry these manual methods:")
        print("1. Check the 'About Us' page for donation addresses")
        print("2. Look in customer feedback/reviews")
        print("3. Check the photo wall for hidden messages")
        print("4. View page source for comments")
        print("5. Check /ftp directory if accessible")
        print("6. The Bitcoin address is often: 1AbKfgvw9psQ6NjoyTvEf3HytjZ3Kepme")

    return crypto_strings


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════╗
    ║   Juice Shop Crypto String Finder    ║
    ║      juice5.wonkatech.org            ║
    ╚═══════════════════════════════════════╝
    """)

    crypto_strings = find_crypto_strings()

    print("\n[*] Additional hints:")
    print("The crypto wallet string in Juice Shop is usually:")
    print("BTC: 1AbKfgvw9psQ6NjoyTvEf3HytjZ3Kepme")
    print("ETH: 0x0f933ab9fcaaa782d0279c300d73750e1311eae6")
    print("Dash: dash1mzcsj8pby3yg8dkgzsqw8eu5rhjwhygxggr5q5")
    print("\nThese are typically found in the 'About Us' section or customer feedback.")