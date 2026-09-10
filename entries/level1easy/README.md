# level1easy (Lacks — crackmes.one)

| | |
|---|---|
| Started | 2026-09-10 |
| Last touched | 2026-09-10 |
| Status | solved |
| Platform | Windows x64 console (PE32+) |
| Tooling | IDA |
| Source | [crackmes.one/user/Lacks](https://crackmes.one/user/Lacks) |

## Summary
Login screen: "Enter Password:" → grant on correct password. Part 1 of Lacks' leveled series (12 crackmes: `level1easy` → `level10`, then `UltimateBoss` / `UltimateRealBoss`).

## Findings
- **Password: `password`** (8 chars, verified live: `Access Granted. Welcome!`).
- Login logic in `main` @ `0x140001290` (renamed from `sub_140001290`):
  - prints the banner, `std::cin >> input` (via inlined `operator>>` helpers at `0x140001550` / `0x140001720`);
  - check: `input.size() == 8 && memcmp(input.data(), expected, 8) == 0` → `"\nAccess Granted. Welcome!\n"` else `"\nAccess Denied. Invalid Password.\n"`.
- The expected string never exists in `.rodata` — it's an inline immediate on the stack: `Buf2[0] = 0x64726F7773736170`, little-endian bytes `70 61 73 73 77 6f 72 64` = `password` (set at `0x1400012df`).
- Recon had flagged: MSVC dynamic CRT, leaked PDB path (`crackmetest` project), `memcmp`/`strlen` imports — all confirmed.

## Process
1. Strings pass (Python): banner + grant/deny strings; `memcmp` import → compare-based check.
2. IDA: located `main` by xrefs from the string `"Enter Password: "` (`0x140003438`) → `0x140001290`.
3. Decompiled `main`: no obvious string compare target in `.rodata`; the constant `0x64726F7773736170` decoded (LE) to "password".
4. Verified live: `echo password | level1easy.exe` → Access Granted.

## Outcome
Solved — `password`. Level 1 of 12; expect the series to layer obfuscation on top of this same compare shape.

## Lessons
- Missing string in `.rodata` + a huge hex immediate in the compare = the string *is* the immediate, read little-endian. → see `notes/qword-immediate-strings.md`.
