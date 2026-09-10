# level5 (Lacks — crackmes.one)

| | |
|---|---|
| Started | 2026-09-10 |
| Last touched | 2026-09-10 |
| Status | solved |
| Platform | Windows x64 console (PE32+) |
| Tooling | IDA |
| Source | [crackmes.one/user/Lacks](https://crackmes.one/user/Lacks) |

## Summary
"CRACKME LEVEL 5": two-part numeric license key; correct pair validates the license and prints the flag. No username — the pair is self-contained.

## Findings
- **Solution: part1 = `1700`, part2 = `5565`** → `[+] LICENSE VALIDATED!` / `[+] Flag: Victory!`
- Checks in `main` @ `0x140001210` (Hex-Rays 50688 fallback → disasm):
  - both inputs read as `unsigned int`; stream fail → `"Invalid input."`;
  - `part1 != 0` **and** `part1 % 17 == 0` — compiler divisibility idiom @ `0x140001393`: `mul 0xF0F0F0F1` + `shr edx,4` = `part1/17`, then `imul ecx, edx, 0x11` + compare = exact division test;
  - chained: `part2 == ((part1 ^ 0x1337) + 0x2A)` @ `0x1400013a6`;
  - flag: 8-byte heap buffer from `init_flag_enc` @ `0x140001000` (global `flag_enc_begin`/`flag_enc_end` @ `0x1400051e0/0x1400051f0`), enc qword `0x9CC4CFD2C9DED4EB` = `EB D4 DE C9 D2 CF C4 9C`; printed on both branches with `key = part2 & 0xFF` (`" (Garbage!)"` suffix on failure).
- Key `0xBD` is the only one of the 256 printable candidates forming a real word: `Victory!`. Back-derived: `part2 ≡ 0xBD (mod 256)` with `part2 = (part1 ^ 0x1337) + 0x2A`, `part1 = 17*100 = 1700` → `part2 = 0x15BD = 5565`.

## Process
1. Strings: no granted/denied, two key parts → decompile failed (50688) → disasm.
2. Read the magic-division block as mod-17, the chain `part2 = f(part1)`, the XOR decrypt loop over the (4th) runtime-built global.
3. Recovered ciphertext via the `runtime-initialized-globals` skill (initializer: single qword store this time), printable-brute over 256 keys → `Victory!` @ `0xBD`.
4. Solved the chained constraint for the smallest printable-key part1 (`17×100`), verified live.

## Outcome
Solved — flag `Victory!`. IDB annotated and saved.

## Lessons
- `mul <huge odd const>` followed by `imul ecx, edx, K` + compare = **exact divisibility test by K** — the multiplier of the follow-up `imul` gives you the modulus for free. → see `notes/magic-division-checks.md`.
- Third reuse of `runtime-initialized-globals` + second of `single-byte-xor-flag` — the series' flag buffer pattern is stable: initializer → ciphertext → printable-brute.
