# Reverse Engineering Journal

Working journal for everything we reverse, solve, and learn. Each solved target becomes a self-contained entry; anything that transfers to other targets gets distilled into a note. The repo ships as-is to GitHub — write every entry assuming a stranger (or future-you) reads it cold.

## Layout

```
entries/        one folder per target — the full writeup
  _template/    copy this folder to start a new entry
    ida/         local IDA databases (.i64/.idb) — never committed
notes/          target-agnostic lessons & techniques
  _template.md  copy this file to start a new note
cheatsheets/    quick reference: file formats, opcodes, calling conventions, tool quirks
resources/      links, papers, tools worth remembering
wiki/           markdown source for the GitHub wiki tab
```

## Conventions

- **Entry folder:** `entries/<target-name>/` — kebab-case, stable, no date in the name (dates live in the header table). One target, one folder, updated in place across sessions.
- **Binaries stay out of git.** `artifacts/` (dumps, packed samples) and `ida/` (IDA/Ghidra databases) in each entry are gitignored — they stay local. Only knowledge is committed: writeups, notes, scripts.
- **Scripts are knowledge.** Anything reusable we wrote during a session (IDAPython, Ghidra scripts, patchers, keygens) goes in the entry's `scripts/` and gets committed.
- **Dead ends get written down.** A hypothesis that didn't pan out and *why* is often more valuable than the solution.
- **Notes link back.** A note distilled from an entry links to its source entry, and the entry links forward to the note.

## Starting an entry

1. `cp -r entries/_template entries/<target-name>`
2. Fill in the header table, keep `Status` honest (`in-progress` / `solved` / `abandoned`).
3. Commit early, commit often — the journal is append-mostly, rewrites are fine.
