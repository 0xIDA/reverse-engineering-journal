#!/usr/bin/env python3
"""Level 3 keygen (Lacks crackmes).

Check (from IDA, main @0x140001290):
    sum    = signed byte sum of the username (movsx/psrad 18h -> negatives for bytes >= 0x80)
    serial = (sum * 0x539) ^ 0x5A5A   (32-bit)

Usage: python keygen.py <username> [more names...]
"""
import sys


def serial(username: str) -> int:
    data = username.encode("latin-1", "replace")
    total = 0
    for b in data:
        total += b - 256 if b >= 0x80 else b  # signed byte
    return ((total * 0x539) ^ 0x5A5A) & 0xFFFFFFFF


if __name__ == "__main__":
    for name in (sys.argv[1:] or ["IDA"]):
        print(f"{name} -> {serial(name)}")
