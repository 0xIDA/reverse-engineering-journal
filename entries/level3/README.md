# level3 (Lacks — crackmes.one)

| | |
|---|---|
| Started | 2026-09-10 |
| Last touched | 2026-09-10 |
| Status | solved |
| Platform | Windows x64 console (PE32+) |
| Tooling | IDA |
| Source | [crackmes.one/user/Lacks](https://crackmes.one/user/Lacks) |

## Summary
"CRACKME LEVEL 3": username + numeric serial — a proper keygen, not a fixed password. Same MSVC template.

## Findings
- **Keygen: `serial = (signed byte sum of username) * 0x539 ^ 0x5A5A`** (32-bit).
  - `0x539` = 1337; signed bytes matter only for usernames with bytes ≥ 0x80 (movsx everywhere).
- Login logic in `main` @ `0x140001290`:
  - `cin >> username` (std::string), `cin >> serial` (unsigned int);
  - non-numeric serial → stream fail → `"[-] Invalid input. Serial must be a number..."`;
  - empty username → straight deny (even though sum=0 → serial 0x5A5A would "match" the formula);
  - check: `sum = Σ movsx(username[i])` (SSE-vectorized at `0x1400013e0`, scalar tail at `0x140001443`), then `imul eax, sum, 0x539` @ `0x14000145a`, `xor eax, 0x5A5A` @ `0x140001456`, compare to serial @ `0x14000145b`.
- Verified live: username `IDA` → sum 206 → serial `289156` → `[+] Access Granted! You are a master keygenerator.`
- Keygen script: `scripts/keygen.py`.

## Process
1. Strings → main via xrefs; Hex-Rays **failed** on `main` (error 50688 — the vectorized sum loop) — fell back to full disassembly, which reads cleanly.
2. Recognized the SSE pattern `movd/punpcklbw/punpcklwd/psrad 18h/paddd` as a sign-extending byte sum; scalar tail confirms `movsx`.
3. Rebuilt formula from the `imul`/`xor` tail; wrote `scripts/keygen.py`; verified against the binary.

## Outcome
Solved — general keygen for any username. IDB annotated: `main`/`out_cstr`/`read_string`/`std_cin`/`std_cout` renamed, step comments on the algorithm, bookmark, saved.

## Lessons
- `movd + punpcklwd + psrad 18h + paddd` = compiler-vectorized `movsx` byte sum — don't stare at it like crypto, it's Σsigned(bytes). → see `notes/sse-byte-sum-keygen.md`.
- When Hex-Rays bails (50688), the disasm of a short function is often trivially readable — don't fight the decompiler.
