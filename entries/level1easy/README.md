# level1easy (Lacks — crackmes.one)

| | |
|---|---|
| Started | 2026-09-10 |
| Last touched | 2026-09-10 |
| Status | in-progress |
| Platform | Windows x64 console (PE32+) |
| Tooling | IDA |
| Source | [crackmes.one/user/Lacks](https://crackmes.one/user/Lacks) |

## Summary
Login screen: "Enter Password:" → grant on correct password. Part 1 of Lacks' leveled series (12 crackmes: `level1easy` → `level10`, then `UltimateBoss` / `UltimateRealBoss`).

## Recon
- PE32+ x64 console, MSVC (MSVCP140 / VCRUNTIME140 dynamic CRT), ~19.5 KB, no packing — plain `.text/.rdata/.data/.pdata/.rsrc/.reloc`.
- PDB path leak: `C:\Users\knze2\source\repos\crackmetest\x64\Release\crackmetest.pdb` — project "crackmetest", x64 Release.
- Strings: `password`, `===…` banner with `LOGIN SCREEN`, `Enter Password: `, `Access Granted. Welcome!`, `Access Denied. Invalid Password.`, `Press Enter to exit...`
- Imports of interest: `memcmp`, `strlen`, `std::cin`/`std::cout`, `std::string` — straight string compare expected.

## Process
(working)

## Outcome
TBD

## Lessons
(none yet)
