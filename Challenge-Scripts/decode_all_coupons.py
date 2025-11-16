#!/usr/bin/env python3

import requests

# Get the full backup file content
backup_response = requests.get("https://juice5.wonkatech.org/ftp/coupons_2013.md.bak%2500.pdf")
backup_content = backup_response.text.strip()

print("🔍 All backup coupon codes:")
backup_codes = backup_content.split('\n')

# Import our Z85 decoder
import sys
sys.path.append('.')

# Inline Z85 decoder
import struct

Z85_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"

def z85_decode(encoded):
    if len(encoded) % 5 != 0:
        raise ValueError("Encoded length must be multiple of 5")
    
    decoded = b""
    for i in range(0, len(encoded), 5):
        chunk = encoded[i:i+5]
        value = 0
        
        for char in chunk:
            value = value * 85 + Z85_ALPHABET.index(char)
        
        decoded += struct.pack('>I', value)
    
    return decoded

print("\n📋 Decoded coupon patterns:")
for i, code in enumerate(backup_codes):
    if code.strip():
        try:
            decoded = z85_decode(code.strip())
            plaintext = decoded.decode('utf-8')
            print(f"{i+1:2d}. {code.strip()} → {plaintext}")
        except Exception as e:
            print(f"{i+1:2d}. {code.strip()} → ERROR: {e}")

print(f"\n🧠 Pattern Analysis:")
print("- All codes from 2013 (year 13)")
print("- Months: OCT, NOV, DEC")  
print("- Discounts: 10%, 15%")
print("- Format confirmed: MMMYY-DD")

