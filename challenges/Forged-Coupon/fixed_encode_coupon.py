#!/usr/bin/env python3
"""encode_coupon.py - Z85 encode/decode utility for Juice Shop forged coupon challenge.

Usage:
  python3 encode_coupon.py encode "MMMYY-VV"
  python3 encode_coupon.py decode "Z85STRING"
  python3 encode_coupon.py sample    # prints sample encoding for OCT25-80

Notes:
- Z85 requires input byte length to be a multiple of 4. The coupons used in the Juice Shop
  challenge are typically 8 bytes (format MMMYY-VV), which works out-of-the-box.
- If your input length is not a multiple of 4, pad with null bytes (\x00) to the next multiple of 4,
  but be aware Juice Shop expects the exact plaintext format (no padding) so crafting should use
  multiples of 4 (e.g., 8 bytes).
"""
import sys

z85_alphabet = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"

def z85_encode(data: bytes) -> str:
    if len(data) % 4 != 0:
        raise ValueError("Length of data must be multiple of 4 bytes for Z85 encode.")
    encoded = []
    for i in range(0, len(data), 4):
        chunk = data[i:i+4]
        value = (chunk[0] << 24) + (chunk[1] << 16) + (chunk[2] << 8) + chunk[3]
        chars = []
        for _ in range(5):
            chars.append(z85_alphabet[value % 85])
            value //= 85
        encoded.extend(reversed(chars))
    return bytes(encoded).decode('ascii')

def z85_decode(text: str) -> bytes:
    if len(text) % 5 != 0:
        raise ValueError("Length of Z85 text must be multiple of 5 characters.")
    lookup = {chr(c): i for i, c in enumerate(z85_alphabet)}
    out = bytearray()
    for i in range(0, len(text), 5):
        chunk = text[i:i+5]
        value = 0
        for ch in chunk:
            if ch not in lookup:
                raise ValueError(f"Invalid Z85 character: {ch!r}")
            value = value * 85 + lookup[ch]
        out.extend([(value >> 24) & 0xFF, (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF])
    return bytes(out)

def main():
    if len(sys.argv) < 2:
        print("Usage: encode_coupon.py <encode|decode|sample> <value>")
        sys.exit(1)
    cmd = sys.argv[1].lower()
    if cmd == "encode":
        if len(sys.argv) != 3:
            print("Usage: encode_coupon.py encode \"MMMYY-VV\"")
            sys.exit(1)
        plain = sys.argv[2].encode('ascii')
        print(z85_encode(plain))
    elif cmd == "decode":
        if len(sys.argv) != 3:
            print("Usage: encode_coupon.py decode \"Z85STRING\"")
            sys.exit(1)
        decoded = z85_decode(sys.argv[2])
        print(decoded.rstrip(b'\x00').decode('ascii', errors='replace'))
    elif cmd == "sample":
        print("Plain : OCT25-80")
        print("Z85   :", z85_encode(b"OCT25-80"))
    else:
        print("Unknown command:", cmd)
        sys.exit(2)

if __name__ == "__main__":
    main()