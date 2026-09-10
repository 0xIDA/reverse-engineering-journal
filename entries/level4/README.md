# level4 (Lacks — crackmes.one)

| | |
|---|---|
| Started | 2026-09-10 |
| Last touched | 2026-09-10 |
| Status | solved |
| Platform | Windows x64 console (PE32+) |
| Tooling | IDA |
| Source | [crackmes.one/user/Lacks](https://crackmes.one/user/Lacks) |

## Summary
"CRACKME LEVEL 4": username + numeric serial. The serial *is* the key: the program always decrypts and prints a hidden 7-byte buffer with a single-byte XOR key derived from the serial — correct serial prints the flag, wrong serial prints gibberish.

## Findings
- **Solution: username `admin`, serial `64083`** → `[+] Success! Your decrypted flag is: Solved!`
- Algorithm in `main` @ `0x140001300` (Hex-Rays failed again — 50688, vectorized loop; disasm):
  - `sum = Σ signed_bytes(username)` (same SSE `psrad 18h` pattern as level3);
  - `r12d = sum * 0x7B` (123) @ `0x1400014be` — the expected serial;
  - key byte: `sil = (serial & 0xFF) ^ 0x34` @ `0x1400014c8`;
  - decrypt loop @ `0x140001500`: `out[i] = key ^ enc[i]` over a 7-byte heap buffer from the dynamic initializer `init_flag_enc` @ `0x140001000` (global `flag_enc_begin`/`flag_enc_end` pair @ `0x140006218/0x140006228`, zeros in static image);
  - branch @ `0x140001551`: serial == sum*0x7B → `"[+] Success! Your decrypted flag is: "` + plaintext; else `"[-] Access Denied. Decrypted output: "` + text + `" (Gibberish!)"`.
- Encrypted bytes (initializer stores: dword `285935668` + word `770` + byte `70`): `34 08 0B 11 02 03 46`.
- Both the flag and the key are recoverable statically: brute-force the 256 possible key bytes over the 7 ciphertext bytes → only `key 0x67` gives fully-printable text = **`Solved!`** — which pins `serial & 0xFF = 0x53`, satisfied by `admin` (`sum 521 * 123 = 64083`).

## Process
1. Strings showed no grant message at all, only `"...Decrypted output: "` — red flag that the "password" is a decryption key, not a stored string.
2. Disassembled `main` (Hex-Rays 50688 fallback): recognized the level3 byte-sum, then the `imul 0x7B` and the XOR-key loop reading a runtime-built global.
3. Reused the `runtime-initialized-globals` skill: xrefs to the global → `init_flag_enc` → immediate stores → ciphertext `34 08 0B 11 02 03 46`.
4. Brute-forced all 256 XOR keys for printable output → `Solved!` @ key `0x67` → back-derived `admin`/`64083`. Verified live.

## Outcome
Solved — flag `Solved!` with `admin`/`64083`. IDB annotated and saved.

## Lessons
- When a program prints a "decrypted output" on *every* path, the ciphertext is in the binary and the key is input-derived — recover ciphertext statically, then brute-force the small key space instead of guessing the input. → see `notes/single-byte-xor-flag.md`.
- Second reuse of `runtime-initialized-globals` (level2's skill fired as-is) — the `{begin,end}` heap-buffer pattern is now a series signature.
