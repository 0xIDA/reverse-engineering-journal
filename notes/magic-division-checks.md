# Magic-number division (compiler divisibility checks)

| | |
|---|---|
| Date | 2026-09-10 |
| Category | decompilation / asm |
| Source | `entries/level5/` |

## The technique
Compilers replace `n % d == 0` with multiply-high magic: `mov eax, MAGIC; mul n; shr edx, S` computes `n / d`, then `imul ecx, edx, d; cmp n, ecx` tests exact divisibility. **The multiplier in the follow-up `imul` is the divisor in plain sight** — you rarely need to invert the magic constant.

Common magics: `0xF0F0F0F1` (s=4) → d=17; `0x51EB851F` (s=5?) → d=25-family; `0xCCCCCCCD` (s=2) → d=10; `0x51EB851E...` for 100. When unsure, recover d as `round(2^(32+S) / MAGIC)`.

## When it applies
- License checks with "key must be multiple of N" style rules.
- Any decompiled/disassembled check with a 32-bit `mul` by a huge odd constant followed by a right shift.

## Pitfalls
- The magic applies to *unsigned* division; signed variants use different constants and `sar`.
- Shift count matters when inverting: `d = 2^(32+shift) / magic` (nearest integer).
- Sometimes only `shr edx, S` remains (no imul) — that's just a division, not a divisibility test; the modulus then comes from the magic itself.
- Reference: journal `entries/level5/` — `0xF0F0F0F1` @ `0x140001393`, follow-up `imul ecx, edx, 0x11` → mod 17.
