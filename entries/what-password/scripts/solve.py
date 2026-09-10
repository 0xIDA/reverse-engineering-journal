#!/usr/bin/env python3
"""Derive the what_password password from the `pw` table.

Check (from IDA decompile of main @0x401150):
    input[k] == ((pw[k] ^ 0x27) + 2*(k+1)) & 0xFF   (char arithmetic)
    stop when the expected char is '\n'.

pw @ 0x404028 (15 bytes, from IDA):
    4e 49 1d 42 7c 41 7c 33 75 6a 6b 3c 7e 7f cb
"""
PW = bytes.fromhex("4e491d427c417c33756a6b3c7e7fcb")

pw_out = bytearray()
for k, b in enumerate(PW):
    c = ((b ^ 0x27) + 2 * (k + 1)) & 0xFF
    if c == 0x0A:
        break
    pw_out.append(c)

print(pw_out.decode())  # -> kr@meri$dab3st
