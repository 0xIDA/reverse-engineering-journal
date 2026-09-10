# Runtime-initialized globals (zeros in the static image)

| | |
|---|---|
| Date | 2026-09-10 |
| Category | decompilation / data |
| Source | `entries/level2/` |

## The technique
When the comparison target is a global that reads as **all zeros in the file**, the data is built at startup by a C++ **dynamic initializer** (registered in `.CRT$XCU`, run by `_initterm` before `main`). Don't trust static `.data` for such globals — find the initializer.

The runtime shape in level2: a global `{begin, end}` pointer pair into a heap buffer; length is computed as `end - begin` at check time.

## Procedure
1. Decompile the check; note the global the compare indexes into.
2. Read it in the image — if zeros (or garbage), do NOT conclude "impossible"; find writes: `xrefs_to <global>` in the disassembler.
3. One xref before `main` = the dynamic initializer (small function doing `operator new` + immediate stores, then registering itself). Decompile it — the stores are the data, often as dword/word/byte immediates.
4. Reassemble the bytes from the immediates (LE per field, in address order).
5. Apply whatever transform the compare does (XOR/add) to get the expected input.

## Pitfalls
- The initializer may split data across multiple store widths (dword + word + byte) — concatenate in address order.
- Idiom check: the same address also gets a matching **destructor** (atexit-registered `free`) — the pair confirms the global is object-like, not a plain array.
- If the initializer copies from a `.rodata` blob instead of immediates, that blob is the data — decode there.
- Reference: journal `entries/level2/` — `expected_begin` @ `0x140005218`, initializer `0x140001000` stores `28 3F 2C 3F 28 29 3F`, XOR key `0x5A` → `"reverse"`.
