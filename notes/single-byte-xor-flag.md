# Single-byte XOR flag + printable-brute

| | |
|---|---|
| Date | 2026-09-10 |
| Category | crypto / ctf |
| Source | `entries/level4/` |

## The technique
When a crackme decrypts and prints a "flag"/message on **both** the success and failure paths, the ciphertext is embedded (or runtime-built) and the key is derived from the input — often a single byte: `key = (input_lowbyte ^ const)`, `flag[i] = enc[i] ^ key`. You don't need the intended username at all: recover the ciphertext statically, then brute-force all 256 single-byte keys and keep the candidates that are fully printable — the real flag stands out (often a short ASCII phrase).

## When it applies
- Messages like "Decrypted output:" / "Your decrypted flag is:" printed unconditionally.
- A decrypt loop XORing a small buffer with a byte derived from user input.
- Ciphertext in a runtime-initialized global (zeros in `.data` — see `runtime-initialized-globals`).

## Procedure
1. Extract the ciphertext (initializer immediates or `.rodata` blob).
2. `for k in 0..255: dec = enc ^ k` — score by printability; short flags with mixed case usually yield exactly one clean candidate.
3. If several keys decode printable text, tie the key back to the input: `input_byte = k ^ const` (here `k = (serial & 0xFF) ^ 0x34`), then find an input satisfying the serial formula — or just present the flag.
4. Verify by running the binary with a matching username/serial pair.

## Pitfalls
- The success branch can still print gibberish if the check passes for a username the ciphertext wasn't keyed for — printable-brute finds the *intended* plaintext regardless.
- Watch for key reuse across bytes (single byte here) vs rolling keys — check the loop indexing before assuming.
- Reference: journal `entries/level4/` — ciphertext `34 08 0B 11 02 03 46`, key `0x67` → `"Solved!"`.
