# Phase 2 Implementation Status

This tracker distinguishes source implementation from execution evidence. Items marked implemented still require a local run on the project machine before being claimed as verified.

## Module 3 — Concurrency and Deadlock Management

- [x] Source added: deterministic race-condition demonstration with a barrier-controlled lost update (local verification pending).
- [x] Source added: mutex-protected shared counter demonstration (local verification pending).
- [x] Source added: Peterson's Solution (two participants; local verification pending).
- [x] Source added: Strict Alternation (two participants; progress limitation documented; local verification pending).
- [x] Source added: Lamport's Bakery Algorithm (fixed participant count; local verification pending).
- [x] Source added: Test-and-Set-style spin lock using Python's non-blocking lock acquisition (local verification pending).
- [ ] IPC and producer-consumer / bounded buffer.
- [ ] Counting and binary semaphores; monitors.
- [ ] Dining philosophers, readers-writers and sleeping barber.
- [ ] Deadlock characterization, prevention, avoidance, detection and recovery.
- [ ] Banker's Algorithm and database transaction case study.

## Module 4 — Memory Management

- [ ] Loading, linking and address binding.
- [ ] Fixed/variable partitions and First Fit, Best Fit, Worst Fit.
- [ ] Paging, segmentation and segmented paging.
- [ ] Demand paging and FIFO, LRU, Optimal, LFU page replacement.
- [ ] Belady's anomaly and thrashing.
- [ ] File access, file allocation and disk scheduling.
- [ ] Virtual machines, hypervisors, GPU and CUDA introduction.

## Local verification required

Run from repository root:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py race-demo --iterations 100
PYTHONPATH=phase-2/src python3 phase-2/src/main.py locked-demo --workers 4 --iterations 1000
PYTHONPATH=phase-2/src python3 phase-2/src/main.py lock-demo --algorithm peterson --workers 2 --iterations 500
PYTHONPATH=phase-2/src python3 phase-2/src/main.py lock-demo --algorithm strict-alternation --workers 2 --iterations 500
PYTHONPATH=phase-2/src python3 phase-2/src/main.py lock-demo --algorithm bakery --workers 4 --iterations 500
PYTHONPATH=phase-2/src python3 phase-2/src/main.py lock-demo --algorithm test-and-set --workers 4 --iterations 500
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

Do not record a test count, success result or completion percentage until these commands have actually been run and observed.
