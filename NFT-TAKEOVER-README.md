# NFT Takeover Educational Scripts

## ⚠️ IMPORTANT DISCLAIMER
These scripts are for **EDUCATIONAL PURPOSES ONLY** and should only be used in:
- CTF (Capture The Flag) competitions
- Authorized penetration testing engagements
- Personal test environments you own
- Bug bounty programs where you have explicit permission

**NEVER** use these scripts on production systems or NFT platforms without explicit written authorization.

## Overview

This repository contains two NFT takeover scripts that demonstrate common vulnerabilities in NFT platforms:

1. **nft-takeover-educational.py** - Comprehensive testing suite
2. **nft-takeover-simple.py** - Simplified version for quick CTF challenges

## Installation

```bash
# Clone or download the scripts
cd /Users/walterbarr_1/sql-injection-lab/

# Install requirements
pip3 install -r nft-requirements.txt
```

## Usage

### Simple Script (Recommended for CTFs)

```bash
# Basic usage
python3 nft-takeover-simple.py <target_url> [nft_id]

# Example
python3 nft-takeover-simple.py http://ctf.example.com 1
python3 nft-takeover-simple.py http://localhost:3000 42
```

### Comprehensive Script

```bash
# Run all tests
python3 nft-takeover-educational.py http://test.example.com

# Run specific test
python3 nft-takeover-educational.py http://test.example.com --specific-test metadata

# With smart contract address
python3 nft-takeover-educational.py http://test.example.com --contract 0x123...abc
```

## Vulnerabilities Tested

### 1. **Direct Ownership Transfer**
- Attempts to change NFT ownership without authorization
- Tests various API endpoints and HTTP methods
- Exploits missing access controls

### 2. **Metadata Manipulation**
- Modifies NFT metadata (name, description, attributes)
- Tests for unprotected metadata endpoints
- Attempts to change ownership through metadata

### 3. **Parameter Pollution**
- Uses duplicate parameters to confuse the application
- Tests array injection techniques
- Exploits parsing inconsistencies

### 4. **Authorization Bypass**
- Tests various HTTP headers for privilege escalation
- Attempts to impersonate admin users
- Exploits trust in client-provided headers

### 5. **Signature Verification Bypass**
- Tests null/empty signatures
- Attempts to bypass cryptographic checks
- Exploits weak signature validation

### 6. **Unauthorized Minting**
- Attempts to create new NFTs without permission
- Tests for unprotected mint endpoints
- Exploits missing role checks

### 7. **Reentrancy Vulnerabilities**
- Tests for reentrancy in withdrawal functions
- Simulates recursive calls
- Exploits state management issues

## Common CTF Scenarios

### Scenario 1: Basic Ownership Takeover
```bash
# The NFT with ID 1 belongs to 'admin'
# Your goal is to take ownership

python3 nft-takeover-simple.py http://ctf-challenge.com 1
```

### Scenario 2: Metadata Manipulation
```bash
# Change NFT metadata to prove exploitation

python3 nft-takeover-educational.py http://ctf-challenge.com --specific-test metadata
```

### Scenario 3: Mass NFT Takeover
```bash
# Take over multiple NFTs
for i in {1..10}; do
    python3 nft-takeover-simple.py http://ctf-challenge.com $i
done
```

## Expected Output

### Successful Takeover:
```
[*] Starting NFT Takeover on: http://ctf.example.com
[*] Target NFT ID: 1

[1] Testing Direct Ownership Change...
[+] SUCCESS via POST to /api/nft/1/transfer
    Payload: {'tokenId': 1, 'newOwner': 'attacker'}
    Response: {"success": true, "message": "NFT transferred"}

[+] NFT TAKEOVER SUCCESSFUL!
```

### Failed Attempt:
```
[1] Testing Direct Ownership Change...
[2] Testing Metadata Manipulation...
[3] Testing Parameter Pollution...
[4] Testing Authorization Bypass...

[-] All takeover attempts failed
[-] NFT takeover failed - target may be secure
```

## Defensive Measures

For developers looking to protect against these vulnerabilities:

1. **Implement Proper Access Controls**
   ```python
   def transfer_nft(request, nft_id):
       # Verify the sender owns the NFT
       if request.user != nft.owner:
           return forbidden()
   ```

2. **Use Server-Side Session Management**
   ```python
   # Get user from session, not from request
   user_id = session.get('user_id')
   # Never trust client-provided user identifiers
   ```

3. **Validate All Inputs**
   ```python
   # Validate signatures
   if not verify_signature(signature, message, sender_address):
       return error("Invalid signature")
   ```

4. **Implement Rate Limiting**
   ```python
   @rate_limit(max_calls=10, period=60)
   def transfer_nft():
       # Transfer logic
   ```

## Troubleshooting

### SSL Certificate Errors
```bash
# Disable SSL verification (CTF only!)
export PYTHONWARNINGS="ignore:Unverified HTTPS request"
```

### Connection Errors
```bash
# Check if target is reachable
curl -I http://target.com
```

### Permission Denied
```bash
# Make script executable
chmod +x nft-takeover-*.py
```

## Legal Notice

Using these scripts on systems without authorization is **ILLEGAL** and can result in:
- Criminal charges
- Civil lawsuits
- Permanent ban from platforms
- Damage to reputation

Always ensure you have explicit permission before testing any system.

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Web3 Security Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [NFT Security Guide](https://www.certik.com/resources/blog/nft-security)
- [CTF Resources](https://ctftime.org/)

## Contributing

This is an educational project. Contributions that improve the educational value or add new vulnerability demonstrations are welcome.

---

**Remember**: With great power comes great responsibility. Use these tools ethically and legally!