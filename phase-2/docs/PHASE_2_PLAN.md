# Phase 2 Plan — Modules 3 and 4

**Project:** Integrated National Citizen Services Platform  
**Course:** Operating Systems (CCSE0303A)  
**Group:** 66  
**Branch:** `phase-2/concurrency-memory`

This plan is based on the official B.Tech CSE (Data Science) 2026–27 Operating Systems syllabus. It is a scope and implementation tracker, not evidence that any Phase 2 feature is already complete.

## Phase boundary

- **Phase 1:** Modules 1 and 2 — completed and documented separately under `phase-1/`.
- **Phase 2:** Modules 3 and 4 — concurrency/deadlock management and memory management.
- **Final integration:** Bring the verified Phase 1 and Phase 2 components together in the working browser-based citizen-services application.

There is no Phase 3. The browser-based website is a final integration deliverable, not a claim that Phase 1 or Phase 2 already contains a deployed website.

## Module 3 — Concurrency and Deadlock Management

### Concurrency and synchronization
- Concurrency and types of process.
- Race conditions and critical-section requirements.
- Inter-process communication (IPC).
- Producer–consumer / bounded-buffer problem.
- Lock variable, strict alternation, Peterson's solution, Lamport Bakery solution and test-and-set lock.
- Counting and binary semaphores; monitors.
- Classical synchronization problems: dining philosophers, readers–writers and sleeping barber.

### Deadlock management
- Deadlock definition and characterization.
- Deadlock prevention.
- Deadlock avoidance using the Banker's Algorithm.
- Deadlock detection and recovery.
- Case study: deadlock avoidance in database transaction management systems such as Oracle or MySQL.

### Planned project demonstrations
1. Reproducible race-condition demonstration, followed by a synchronized version.
2. Critical-section and mutual-exclusion demonstrations for the syllabus techniques.
3. Producer–consumer bounded buffer with observable producer/consumer events.
4. IPC demonstration using separate processes and a documented communication mechanism.
5. Classical synchronization simulations with correctness checks and bounded execution.
6. Resource-allocation model with Banker's safety check, safe/unsafe-state examples, deadlock detection and recovery demonstration.
7. Database transaction case study using a clearly labelled simulation or documented experiment; no claim of integration with a production database unless actually performed.

## Module 4 — Memory Management

### Memory allocation and address translation
- Memory-management functions.
- Loading, linking and address binding.
- Contiguous allocation: fixed and variable partitions.
- First Fit, Best Fit and Worst Fit.
- Non-contiguous allocation: paging, segmentation and segmented paging.

### Virtual memory
- Virtual-memory concepts and demand paging.
- Performance of demand paging.
- FIFO, LRU, Optimal and LFU page-replacement algorithms.
- Belady's anomaly and thrashing.
- Case study: virtual-memory management in a modern OS such as Windows 10 and how paging affects performance.

### File, disk and modern OS topics
- File access mechanisms and file-allocation methods.
- Disk-scheduling algorithms.
- Virtual machines and hypervisors.
- Introduction to GPU and CUDA programming.

### Planned project demonstrations
1. Partition-allocation simulator comparing First Fit, Best Fit and Worst Fit.
2. Address-translation demonstrations for paging, segmentation and segmented paging.
3. Demand-paging simulator with page-fault counts and FIFO, LRU, Optimal and LFU replacement.
4. Belady's anomaly and thrashing demonstrations using controlled reference strings/workloads.
5. File-access and file-allocation demonstrations using synthetic records.
6. Disk-scheduling simulator with head movement/seek-distance comparison for the algorithms taught in class.
7. Virtual-machine/hypervisor and GPU/CUDA study demonstrations, clearly separating conceptual explanation from any hardware-dependent practical run.

## Proposed code organization

Keep Phase 1 intact. Add Phase 2 implementation in a separate directory:

```text
phase-2/
  README.md
  src/
    citizen_os/
      concurrency/
      deadlock/
      memory/
      files/
      disk/
      virtualization/
  tests/
  docs/
    PHASE_2_PLAN.md
    IMPLEMENTATION_STATUS.md
    EVIDENCE_LOG.md
```

The exact module/file split may be refined after reviewing the existing Phase 1 interfaces. Do not duplicate or rewrite Phase 1 implementations without a demonstrated need.

## Implementation order

1. Inspect and map the Phase 1 process model, thread demonstration and test conventions.
2. Build concurrency primitives and synchronization demonstrations.
3. Build the producer–consumer and IPC demonstrations.
4. Build deadlock/resource-allocation models, including Banker's Algorithm.
5. Build partition allocation and address-translation simulations.
6. Build demand paging and page-replacement simulations.
7. Build file/disk management demonstrations.
8. Cover virtualization and GPU/CUDA topics with honest environment-aware evidence.
9. Run the complete Phase 2 test suite and record genuine outputs/screenshots.
10. Prepare the Phase 2 report only after implementation and verification.

## Verification and evidence rules

- Every algorithm must have unit tests for normal, boundary and invalid inputs where relevant.
- Demonstrations must be deterministic where possible and must terminate safely.
- Record exact commands, environment and observed results.
- Distinguish simulation from real OS/kernel behavior.
- Do not claim Oracle/MySQL integration, Windows 10 internals, hypervisor configuration, GPU execution or CUDA execution unless that specific activity was actually performed.
- Do not fabricate terminal output, screenshots, benchmark results or completion percentages.
- Mark checklist items complete only when source code and appropriate test/run evidence exist.

## Out of scope for this phase

- A deployed government service or connection to real government systems.
- The final public-facing website and full UI integration; these belong to the Final integration stage.
- Kernel modifications or claims that application-level simulations are kernel implementations.



## Phase 2 scope freeze — 2026-11-03

The Python implementation scope for Modules 3 and 4 is frozen for Progress Report II. The complete owner-run test suite passed 140 tests (0 failures, 0 errors; 0.355 seconds), and the owner ran the memory-management functions CLI successfully. No further feature is being represented as complete without corresponding implementation and owner-run evidence. Known practical limitations remain: CUDA source has not been compiled/executed on a GPU; the VM configuration is a model rather than a booted guest; and the Windows 10 case study is research-based rather than a local Windows experiment. Final browser-based integration remains a later project deliverable, not part of the claimed Phase 2 completion.
