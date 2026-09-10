# What Password (Cyberpenguin)

| | |
|---|---|
| Started | 2026-09-10 |
| Last touched | 2026-09-10 |
| Status | in-progress |
| Platform | Linux x86-64, dynamically linked, glibc 2.34+ |
| Tooling | IDA |

## Summary
Cyberpenguin challenge "What password???": find the password `what_password` accepts. Hand-written NASM (`final1.asm`), unstripped, ships DWARF debug info — labels survive: `wrong_msg`, `right_msg`, `input`, `loop_1`, `wrong`, `right`, `read_int`, `read_char`.

## Recon
- ELF 64-bit LSB executable, x86-64, SYSV, dyn-linked, interpreter `/lib64/ld-linux-x86-64.so.2`, BuildID `9e534503dd83623e613055fcda3ab4f8fa780cac`.
- Not stripped; `.debug_info`/`.debug_line` present. Source: NASM 2.16.01, `final1.asm`, built with Debian GCC 12.2.0.
- Imports: `putchar`, `printf`, `scanf`, `__libc_start_main` — scanf-based input read.
- Messages in `.rodata`: `Incorrect password!`, `Correct! You won!`.
- Curious `.rodata` strings that look encoded: `Y0gh==uuK?=0K/==>K1YY` (plus fragments `Y0Y=1YY`, `Y0Y=0Y=!`) — candidate obfuscated password/comparison data.
- Three identical prologue byte patterns in the image → three functions; `main` dispatches to read/compare logic around `loop_1`.

## Process
(working — filled during IDA session)

## Outcome
(password TBD)

## Lessons
(none yet)
