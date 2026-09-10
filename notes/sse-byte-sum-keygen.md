# SSE-vectorized byte-sum keygens

| | |
|---|---|
| Date | 2026-09-10 |
| Category | keygen / sse |
| Source | `entries/level3/` |

## The technique
A serial check that depends on the *username* is a keygen, not a password check. The checksum is often compiler-vectorized: `movd xmm0, [rax]` + `punpcklbw/punpcklwd` + `psrad xmm0, 18h` + `paddd` is **`movsx` byte→dword, SIMD form** — a plain sign-extending byte sum, not a hash. The scalar tail (`movsx ecx, byte ptr [rax]; add edx, ecx`) confirms it.

Serial formula in this family: `serial = ((Σ signed_bytes(username)) * K) ^ C` — here `K = 0x539` (1337), `C = 0x5A5A`, 32-bit.

## When it applies
- `cin >> user; cin >> serial;` (or fgets/atoi equivalents) followed by a checksum-over-input compare.
- Hex-Rays refuses the function (error 50688 with these loops) — the disassembly is short and reads top-down; use it directly.

## Pitfalls
- `psrad 18h` ⇒ **signed** extension: bytes ≥ 0x80 count negative — extended-ASCII usernames change the sum.
- Empty-input special case: level3 denies an empty username outright even when the formula would "match".
- Keep keygen math masked to 32 bits; serial is read as `unsigned int`.
- Test the keygen with a fresh username, not just the one you found in memory.
