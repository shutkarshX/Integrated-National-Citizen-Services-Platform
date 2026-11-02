# Phase 2 — Concurrency, Deadlock and Memory Management

Course: Operating Systems (CCSE0303A) · Group: 66

Phase 2 follows the official Modules 3 and 4 syllabus. Work is isolated from the Phase 1 implementation.

## Implemented Module 3 demonstrations

The current source includes race-condition and mutex exercises; Peterson's Solution, Strict Alternation, Lamport's Bakery Algorithm and a Test-and-Set-style spin lock; bounded-buffer Producer–Consumer; parent-child Pipe IPC; binary/counting semaphore demonstrations; a writer-preference Readers–Writers monitor; Dining Philosophers; Sleeping Barber; Resource Allocation Graph cycle detection; the Banker's safety and resource-request algorithms; multi-instance deadlock detection; a victim-selection recovery example; Coffman conditions and prevention strategies; and a database transaction wait-for graph case study.

These are user-space teaching simulations in Python, not kernel implementations. The Test-and-Set-style lock is not a hardware instruction. The Resource Allocation Graph cycle example uses single-instance resource types; with multiple instances, a cycle alone is not sufficient to prove deadlock. Banker's Algorithm checks whether a state is safe before granting a request. The recovery example illustrates one possible victim-selection policy, not a universal operating-system policy.

## Run from repository root

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py rag-demo
PYTHONPATH=phase-2/src python3 phase-2/src/main.py banker-demo
PYTHONPATH=phase-2/src python3 phase-2/src/main.py deadlock-detection
PYTHONPATH=phase-2/src python3 phase-2/src/main.py deadlock-prevention
PYTHONPATH=phase-2/src python3 phase-2/src/main.py deadlock-recovery
PYTHONPATH=phase-2/src python3 phase-2/src/main.py database-deadlock
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

No third-party Python packages are required.

## Pending scope

Module 4 memory management remains pending: loading/linking/address binding, partition allocation, paging/segmentation, virtual memory and page replacement, file and disk management, virtualization, and GPU/CUDA introduction.
