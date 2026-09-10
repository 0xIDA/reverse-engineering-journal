# level2 (Lacks — crackmes.one)

| | |
|---|---|
| Started | 2026-09-10 |
| Last touched | 2026-09-10 |
| Status | solved |
| Platform | Windows x64 console (PE32+) |
| Tooling | IDA |
| Source | [crackmes.one/user/Lacks](https://crackmes.one/user/Lacks) |

## Summary
"CRACKME LEVEL 2": "Enter Secret Key:" → grant on correct key. Same MSVC template as level1, first obfuscation layer on the compare.

## Findings
- **Secret key: `reverse`** (7 chars, verified live: `[+] Access Granted! You solved it.`).
- Login logic in `main` @ `0x140001300`:
  - `cin >> input`, then: `input_len == expected_size` **and** per-byte `(input[i] ^ 0x5A) == expected[i]`.
- `expected` is **not** in `.rodata` and the global `expected_begin`/`expected_end` pair @ `0x140005218/0x140005228` reads as zeros in the static image — it's a heap buffer built by the dynamic initializer `init_expected` @ `0x140001000` (registered via `.CRT$XCU`, freed by `free_expected` @ `0x140002d10` at exit).
- Initializer writes 7 bytes: `28 3F 2C 3F 28 29 3F` (as dword `0x3F2C3F28` + word `0x2928` + byte `0x3F`) = `"reverse" ^ 0x5A`.

## Process
1. Strings + xrefs → `main` @ `0x140001300` (same shape as level1: banner, `cin >>`, size check, byte compare).
2. Decompile showed the compare against a global whose bytes were zero in `.data` — dead end reading the image directly.
3. Xrefs on the global → the dynamic initializer; decoded its immediate stores (`0x3F2C3F28`, `0x2928`, `0x3F`) → `28 3F 2C 3F 28 29 3F`.
4. Applied the XOR key from the compare loop (`0x5A`) → `reverse`. Verified live.

## Outcome
Solved — `reverse`. IDB cleaned up: `main`/`out_cstr`/`read_string`/`init_expected`/`free_expected` renamed, locals renamed (`input`, `input_len`, `expected_begin`, ...), step comments, bookmark, saved.

## Lessons
- A global the checker reads that's all zeros in the file was built at runtime — follow xrefs to its dynamic initializer instead of trusting static `.data`. → see `notes/runtime-initialized-globals.md`.
