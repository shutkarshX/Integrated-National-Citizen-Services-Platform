# Phase 2 — Concurrency, Deadlock and Memory Management

Course: Operating Systems (CCSE0303A) · Group: 66

Phase 2 follows the official Modules 3 and 4 syllabus. Work is isolated from the Phase 1 implementation.

## Implemented Module 3 demonstrations

The current source includes deterministic race-condition and mutex counter exercises; Peterson's Solution, Strict Alternation, Lamport's Bakery Algorithm and a Test-and-Set-style spin lock; bounded-buffer Producer–Consumer; parent-child process communication through a multiprocessing Pipe; binary/counting semaphore capacity demonstrations; a writer-preference Readers–Writers monitor; Dining Philosophers using an N-1 admission semaphore to prevent circular wait; and a Sleeping Barber simulation with a finite waiting room.

These are user-space teaching simulations in Python, not kernel implementations. The Test-and-Set-style lock uses Python's non-blocking lock acquisition and is not a hardware Test-and-Set instruction. The Readers–Writers monitor uses writer preference, which can delay readers under a continuous stream of writers. The Dining Philosophers solution limits entry to N-1 philosophers. The Sleeping Barber simulation models finite waiting-room capacity and records served versus turned-away customers.

## Run from repository root

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py semaphore-demo --workers 6 --permits 3
PYTHONPATH=phase-2/src python3 phase-2/src/main.py semaphore-demo --workers 6 --permits 1
PYTHONPATH=phase-2/src python3 phase-2/src/main.py readers-writers --readers 4 --writers 2 --iterations 10
PYTHONPATH=phase-2/src python3 phase-2/src/main.py dining-philosophers --philosophers 5 --meals 3
PYTHONPATH=phase-2/src python3 phase-2/src/main.py sleeping-barber --customers 10 --chairs 3
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

No third-party Python packages are required.

## Pending scope

Deadlock characterization, prevention, avoidance, detection and recovery; Banker's Algorithm; database transaction deadlock case study; and all Module 4 memory-management topics remain pending until implemented and verified.
