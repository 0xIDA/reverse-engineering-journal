# Decompiler `char` accumulator = mod-256 arithmetic

| | |
|---|---|
| Date | 2026-09-10 |
| Category | decompilation / ctf |
| Source | `entries/what-password/` |

## The technique
When a decompiled check loop "never terminates" in int math, read the decompiler's type annotations before giving up. An accumulator or result variable typed `char` (or `unsigned char`) means the comparison runs in 8-bit: `((x ^ K) + i) & 0xFF`. Hex-Rays propagates these types from the registers/widths actually used (`r12b` etc.) — trust them over your own 32/64-bit mental simulation.

Concretely (what-password): expected char = `(pw[k] ^ 0x27) + 2*(k+1)`. In int math the last iteration is `0xEC + 30 = 266` — no match against `\n`. As a `char`: `266 & 0xFF = 10` = `\n` → password length 14.

## When it applies
- Byte-wise compare loops in hand-written asm (NASM/custom loaders) compiled without optimization.
- Any decompiled snippet where a variable is shown as `char`/`__int8` while you'd naturally compute in wider ints.
- "The loop must eventually hit a sentinel but no byte value can produce it" → look for wraparound.

## Pitfalls
- Signed vs unsigned still matters *within* the 8-bit domain: `signed char` compares against -x values, `unsigned char` against 0..255. Check the decompiler's exact type.
- Don't confuse the char accumulator with the index: `i` (`r15`) was also char here, but the wrap only mattered on `n10` (`r12b`).
