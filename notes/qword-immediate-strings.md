# Inline string immediates (qword compare constants)

| | |
|---|---|
| Date | 2026-09-10 |
| Category | decompilation / strings |
| Source | `entries/level1easy/` |

## The technique
Compilers inline short string comparisons: the expected string never exists in `.rodata` — it's an immediate. In the decompiler you see `Buf2[0] = 0x64726F7773736170` (or in asm, `cmp qword ptr [rsp+X], 0x64726F7773736170` / a `movabs` into a register). Read the constant little-endian, byte by byte: `70 61 73 73 77 6f 72 64` = `"password"`.

Quick eyeball rule: any immediate whose bytes are all in printable ASCII range (each byte ≥ 0x20, mostly 0x30–0x7A) is worth decoding as text.

## When it applies
- Size-then-compare checks against short strings (≤ 8 bytes per qword; longer strings appear as several immediates or split `cmp`/`mov` chains).
- The strings dump shows the success/failure messages but *not* the expected input.
- MSVC/GCC/Clang all do this at -O2 for fixed-length compares (`memcmp` against a literal).

## Pitfalls
- Endianness: little-endian — the **first** character of the string is the **low** byte of the immediate.
- Longer strings get chunked: several immediates in sequence; follow the stack-slot offsets to order them.
- The constant may be transformed before compare (XOR/add) — if the plain-ASCII read fails, check for post-processing between load and compare.
