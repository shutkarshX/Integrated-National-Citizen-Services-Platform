# Phase 2 — Concurrency, Deadlock and Memory Management

Course: Operating Systems (CCSE0303A) · Group: 66

Phase 2 follows the official Modules 3 and 4 syllabus. The work is kept separate from the Phase 1 implementation.

## Current implementation

The implemented Module 3 demonstrations include a deterministic lost-update race, a mutex-protected counter, Peterson's Solution, Strict Alternation, Lamport's Bakery Algorithm, a Test-and-Set-style spin lock, a bounded-buffer producer-consumer exercise, and parent-child process communication using a multiprocessing Pipe.

These are teaching simulations in Python. They do not alter kernel synchronization primitives. Strict alternation demonstrates mutual exclusion but has a progress limitation. The Test-and-Set-style example uses Python's non-blocking lock acquisition; it does not execute a hardware Test-and-Set instruction. The bounded-buffer example uses a condition variable to coordinate producer and consumer threads.

## Run

From the repository root:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py race-demo --iterations 100
PYTHONPATH=phase-2/src python3 phase-2/src/main.py locked-demo --workers 4 --iterations 1000
PYTHONPATH=phase-2/src python3 phase-2/src/main.py producer-consumer --items 20 --capacity 5
PYTHONPATH=phase-2/src python3 phase-2/src/main.py ipc-demo --message "hello from parent"
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

No third-party Python packages are required.

## Scope still pending

Counting and binary semaphores, monitors, classical synchronization problems, deadlock/Banker's Algorithm, memory management, virtual memory, file and disk management, virtualization and GPU/CUDA topics remain pending until implemented and verified locally.
