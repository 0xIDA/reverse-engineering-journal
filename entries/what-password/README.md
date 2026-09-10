# What Password (Cyberpenguin)

| | |
|---|---|
| Started | 2026-09-10 |
| Last touched | 2026-09-10 |
| Status | solved |
| Platform | Linux x86-64, dynamically linked, glibc 2.34+ |
| Tooling | IDA, WSL kali (verification) |
| Source | [crackmes.one — What password???](https://crackmes.one/crackme/6a83e2f205a9e80a90724421) |

## Summary
Cyberpenguin challenge "What password???": find the password `what_password` accepts. Hand-written NASM (`final1.asm`), unstripped, ships DWARF debug info — labels survive: `wrong_msg`, `right_msg`, `input`, `loop_1`, `pw`.

## Findings
- **Password: `kr@meri$dab3st`** (14 chars — leetspeak "kramer is da best").
- Entry point logic lives in one function at `0x401150` (IDA named it `$_94_1_`, alt name `main`).
- Check loop (decompiled):

```c
sys_read(0, input, 0x400);
v3 = 0;
for ( i = 2; ; i += 2 ) {
    n10 = i + (pw[v3] ^ 0x27);   // n10 is a char → mod-256 arithmetic
    if ( n10 != input[v3] ) break;      // mismatch → wrong
    if ( n10 == 10 ) goto right;        // expected char is '\n' → solved
    ++v3;
}
```

- So: `input[k] == ((pw[k] ^ 0x27) + 2*(k+1)) & 0xFF`, terminate when that equals `\n`.
- `pw` @ `0x404028` (15 bytes): `4e 49 1d 42 7c 41 7c 33 75 6a 6b 3c 7e 7f cb` — immediately followed by `wrong_msg` ("Incorrect password!"), which the loop would read past if the password were longer.
- The trap: `(0xCB ^ 0x27) + 30 = 0x10A` looks non-terminating in 32-bit math, but `n10` is an 8-bit `char`, so it wraps to `0x0A` = `\n` — that wrap is the intended stop condition. Solution length = 14.

## Process
1. `strings`-style pass (Python) → messages + encoded-looking `.rodata` blob; identified ELF64, NASM, unstripped.
2. Loaded into IDA and decompiled `main` at `0x401150` — small hand-written NASM, reads straight through.
3. Decompiled check is self-explanatory; key insight from a decompiler type hint: the accumulator is typed `char` → arithmetic wraps mod 256, making k=14 produce `\n`.
4. Derived password from `pw` bytes; verified against the real binary under WSL kali: `Correct! You won!`.

## Outcome
Solved — `kr@meri$dab3st`. Verification script: `scripts/solve.py`.

## Lessons
- Decompiler type hints are load-bearing: a `char` accumulator means the check runs in mod-256, not int math. → see `notes/decompiler-char-wrap.md`.
