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

## Module 4 — memory allocation source added

The first Module 4 slice implements fixed-partition allocation and variable-partition allocation using First Fit, Best Fit and Worst Fit. The fixed-partition model reports internal fragmentation and permits one process per partition. The variable-partition model splits selected free holes and reports remaining free regions and external fragmentation. The variable allocator accepts an optional set of non-overlapping initial free holes so the three placement policies can be compared meaningfully.

Run from repository root:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py fixed-partitions
PYTHONPATH=phase-2/src python3 phase-2/src/main.py variable-partitions --strategy first-fit
PYTHONPATH=phase-2/src python3 phase-2/src/main.py variable-partitions --strategy best-fit
PYTHONPATH=phase-2/src python3 phase-2/src/main.py variable-partitions --strategy worst-fit
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

These are user-space educational simulations, not kernel memory allocators. This slice has been locally verified on 2026-11-03: the three allocation strategy commands completed and all 44 tests passed.

## Address translation source added

The next Module 4 slice adds logical-to-physical address translation demonstrations for paging, segmentation and segmented paging. Paging uses a page table to map a logical page to a physical frame. Segmentation uses a segment base and limit. Segmented paging first selects a segment and then consults that segment's page table.

Run from repository root:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py paging-demo
PYTHONPATH=phase-2/src python3 phase-2/src/main.py segmentation-demo
PYTHONPATH=phase-2/src python3 phase-2/src/main.py segmented-paging-demo
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

These are user-space teaching simulations of address translation, not hardware MMU implementations. The code and tests are committed; local execution is pending.

## Remaining scope

Loading/linking/address binding, paging/segmentation, virtual memory and page replacement, file and disk management, virtualization, and GPU/CUDA introduction remain pending.
