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

These are user-space teaching simulations of address translation, not hardware MMU implementations. The three CLI demonstrations and complete 55-test suite were locally verified on 2026-11-03.


## Demand paging and page replacement

The current slice adds demand loading and FIFO, LRU, Optimal and LFU replacement. LFU ties are resolved by LRU. A separate FIFO example demonstrates Belady's anomaly.

Run from repository root:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py demand-paging-demo
PYTHONPATH=phase-2/src python3 phase-2/src/main.py page-replacement-demo
PYTHONPATH=phase-2/src python3 phase-2/src/main.py belady-anomaly-demo
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

These are user-space educational simulations, not kernel virtual-memory implementations. The demand-paging, four-algorithm comparison and Belady anomaly demonstrations were locally verified on 2026-11-03; the complete suite passed 67 tests with 0 failures and 0 errors.

## Final browser integration

The final browser integration is implemented at the repository root in `web_app.py`. It reuses the Phase 1 service-process model and CPU scheduling algorithms, provides local JSON persistence, and exposes FCFS, SJF, Priority and Round Robin through a browser UI. Run and verify it using `phase-2/docs/FINAL_BROWSER_INTEGRATION.md`. Owner-side tests and manual browser acceptance are still pending.


## Working-set model and thrashing risk — source added

The working-set demonstration calculates the distinct pages referenced in a trailing window and compares that active set with the process's allocated frames. When the working set exceeds the allocation, the demonstration flags memory pressure as a thrashing risk.

Run from repository root:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py working-set-demo
PYTHONPATH=phase-2/src python3 phase-2/src/main.py thrashing-demo
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

This is a user-space educational model, not a kernel thrashing detector. Local verification is pending. See `phase-2/docs/IMPLEMENTATION_STATUS.md` and `phase-2/docs/EVIDENCE_LOG.md` for status.

## Remaining scope

Loading/linking/address binding and file access/allocation with disk scheduling are implemented and locally verified. Virtualization/hypervisors and GPU/CUDA introduction have now been implemented; local verification is pending.


## Loading, linking and address binding — source added

The implementation models external-symbol resolution between modules, loader-assigned memory bases, relocation of exported symbols, and translation from a module-relative address to an absolute address. The demo also explains compile-time, load-time and execution-time address binding.

Run from repository root:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py loading-linking-demo
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

This is an educational user-space model, not a real executable linker, loader or MMU. Local verification is pending; see `phase-2/docs/IMPLEMENTATION_STATUS.md` and `phase-2/docs/EVIDENCE_LOG.md`.


## File management and disk scheduling — source added

File access examples cover sequential, direct and indexed access. File allocation examples cover contiguous, linked and indexed allocation. Disk scheduling compares FCFS, SSTF, SCAN, C-SCAN, LOOK and C-LOOK, including initial head direction and total cylinder movement.

Run from repository root:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py file-management-demo
PYTHONPATH=phase-2/src python3 phase-2/src/main.py disk-scheduling-demo
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

These are in-memory teaching simulations, not real filesystem modifications or physical disk I/O. Locally verified on 2026-11-03: compilation passed, both CLI demos completed, and the complete test suite passed 132 tests with 0 failures and 0 errors. See the implementation tracker and evidence log for recorded output.


## Virtual machines, hypervisors and GPU/CUDA — source added

The virtualization demonstration validates a VM's virtual CPU and memory request against host capacity and contrasts Type-1 (bare-metal) and Type-2 (hosted) hypervisors. The CUDA demonstration explains host/device roles and the grid–block–thread hierarchy, then simulates global thread indexing for vector addition, including bounds checks for a partially filled final block.

Run from repository root:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py virtualization-demo
PYTHONPATH=phase-2/src python3 phase-2/src/main.py cuda-demo
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

These are educational CPU-side models. The VM model does not boot a guest OS, and the CUDA model does not execute on a GPU or require a CUDA runtime. Local verification is pending; see the implementation tracker and evidence log.


## Syllabus audit

The official CCSE0303A Modules 3–4 coverage review is documented in [`docs/SYLLABUS_AUDIT.md`](docs/SYLLABUS_AUDIT.md). The current implementation suite passes 132 tests, but the audit identifies remaining syllabus-level gaps; passing tests alone is not treated as proof of complete syllabus coverage.


## Additional syllabus coverage work in progress

The explicit lock-variable race, process-classification notes and demand-paging effective-access-time model are available through:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py lock-variable-demo
PYTHONPATH=phase-2/src python3 phase-2/src/main.py process-types
PYTHONPATH=phase-2/src python3 phase-2/src/main.py demand-paging-performance
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

A sourced Windows 10 virtual-memory research case study is in `docs/WINDOWS_10_VIRTUAL_MEMORY_CASE_STUDY.md`. It is not a local Windows measurement. An optional real CUDA kernel source is in `cuda/vector_add.cu`; compile and run it only on a CUDA-capable system with `nvcc`.


### Memory-management functions overview

Run the conceptual overview with:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py memory-management-functions
```

It summarizes memory tracking, allocation and reclamation, address translation, protection, controlled sharing, virtual-memory support and fragmentation management. It is a study aid; the project remains a user-space simulation and does not implement a kernel memory manager.
