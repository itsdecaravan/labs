# Labs

A structured scratchpad for experiments and learning exercises in **Python**, **C**, **Lua**, and **Linux/Bash**.

This is intentionally **not** a polished portfolio repo.
Anything reusable or “project-grade” graduates into its own repository.

---

## Structure

- `python/` – CLI, parsing, automation, algorithms, maths
- `c/` – fundamentals, file I/O, data structures, networking
- `lua/` – ComputerCraft, LÖVE, scripting, maths
- `linux/` – bash tools, system notes, VM-only experiments
- `docs/` – conventions, setup, learning notes
- `datasets/` – sample input files (logs/text) for testing

---

## Conventions

**Good filenames**
- ✅ `logparse_v2_argparse.py`
- ✅ `pi_monte_carlo.c`
- ❌ `test.py`
- ❌ `stuff2.c`

Each script should include:
- Purpose
- Usage
- Notes (optional)

---

## Graduation rule

Move something into its own repo if it has **two or more** of:
- full README
- CLI interface
- multiple modules/files
- tests
- meaningful refactor history
- someone else could realistically use it

---

## ⚠️ Safety Lab (VM only)

`linux/bash/safety-lab/` contains **intentionally destructive / resource exhaustion** scripts.

Run **only in a disposable VM** (snapshot first).
Never run on real machines.
