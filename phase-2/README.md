# Phase 2 — Concurrency, Deadlock and Memory Management

Course: Operating Systems (CCSE0303A) · Group: 66

Phase 2 follows the official Modules 3 and 4 syllabus. The work is kept separate from the Phase 1 implementation.

## Current implementation

The first Module 3 increment contains user-space demonstrations of a deterministic lost-update race, a mutex-protected counter, Peterson's Solution, Strict Alternation, Lamport's Bakery Algorithm and a Test-and-Set-style spin lock.

These are teaching simulations in Python. They do not alter kernel synchronization primitives. Strict alternation demonstrates mutual exclusion but has a progress limitation; it is included to illustrate that mutual exclusion alone is not sufficient for a correct critical-section solution.

## Run

From the repository root:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py race-demo --iterations 100
PYTHONPATH=phase-2/src python3 phase-2/src/main.py locked-demo --workers 4 --iterations 1000
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

No third-party Python packages are required.

## Scope still pending

IPC, producer-consumer, semaphores, monitors, classical synchronization problems, deadlock/Banker's Algorithm, memory management, virtual memory, file and disk management, virtualization and GPU/CUDA topics remain pending until implemented and verified.
