#!/usr/bin/env python3
"""
Z85 Encoder/Decoder for Juice Shop Coupon Challenge
===================================================
CLI script to encode and decode Z85 strings for coupon forgery.

Usage:
    python3 encode_coupon.py encode "OCT25-80"
    python3 encode_coupon.py decode "pEw8ph7Z^w"
    python3 encode_coupon.py sample
"""

import sys
import struct

# Z85 alphabet
Z85_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"

def z85_encode(data):
    """Encode bytes to Z85 string"""
    if len(data) % 4 != 0:
        raise ValueError("Data length must be multiple of 4 bytes")

    encoded = ""
    for i in range(0, len(data), 4):
        # Convert 4 bytes to 32-bit integer
        chunk = data[i:i+4]
        value = struct.unpack('>I', chunk)[0]

        # Convert to base-85
        for j in range(5):
            encoded = Z85_ALPHABET[value % 85] + encoded
            value //= 85

    return encoded

def z85_decode(encoded):
    """Decode Z85 string to bytes"""
    if len(encoded) % 5 != 0:
        raise ValueError("Encoded length must be multiple of 5 characters")

    decoded = b""
    for i in range(0, len(encoded), 5):
        chunk = encoded[i:i+5]
        value = 0

        # Convert from base-85
        for char in chunk:
            if char not in Z85_ALPHABET:
                raise ValueError(f"Invalid Z85 character: {char}")
            value = value * 85 + Z85_ALPHABET.index(char)

        # Convert to 4 bytes
        decoded += struct.pack('>I', value)

    return decoded

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 encode_coupon.py encode \"OCT25-80\"")
        print("  python3 encode_coupon.py decode \"pEw8ph7Z^w\"")
        print("  python3 encode_coupon.py sample")
        return

    command = sys.argv[1].lower()

    if command == "encode":
        if len(sys.argv) != 3:
            print("Usage: python3 encode_coupon.py encode \"PLAINTEXT\"")
            return

        plaintext = sys.argv[2]

        # Check length requirement
        if len(plaintext) % 4 != 0:
            print(f"Error: Input length ({len(plaintext)}) must be multiple of 4")
            print(f"Current input: '{plaintext}' ({len(plaintext)} chars)")
            return

        try:
            data = plaintext.encode('utf-8')
            encoded = z85_encode(data)
            print(f"Plaintext: {plaintext}")
            print(f"Z85 encoded: {encoded}")
        except Exception as e:
            print(f"Error: {e}")

    elif command == "decode":
        if len(sys.argv) != 3:
            print("Usage: python3 encode_coupon.py decode \"Z85STRING\"")
            return

        encoded = sys.argv[2]

        try:
            decoded = z85_decode(encoded)
            plaintext = decoded.decode('utf-8')
            print(f"Z85 encoded: {encoded}")
            print(f"Plaintext: {plaintext}")
        except Exception as e:
            print(f"Error: {e}")

    elif command == "sample":
        # Show example encoding
        sample_plaintext = "OCT25-80"
        sample_encoded = z85_encode(sample_plaintext.encode('utf-8'))

        print("=== Sample Z85 Encoding ===")
        print(f"Plaintext: {sample_plaintext}")
        print(f"Z85 encoded: {sample_encoded}")
        print(f"\nFormat: MMMYY-VV")
        print(f"  MMM = 3-letter month (OCT)")
        print(f"  YY  = 2-digit year (25)")
        print(f"  VV  = discount percent (80)")

    else:
        print(f"Unknown command: {command}")
        print("Available commands: encode, decode, sample")

if __name__ == '__main__':
    main()