# PBL Progress Report II — Draft

**Programme:** BTech CSE (Data Science)  
**Course:** Operating System (CCSE0303A)  
**Faculty:** Ms. Amita Pathania  
**Assignment:** Group Assignment — Group 66  
**Project:** Integrated National Citizen Services Platform  
**Reporting period:** Month 2

> Formatting note: this draft follows the NIET Progress Report II structure for Group Assignments: Sections 9–10 only, up to 250 words per module, two body pages maximum, at least six references, and a source-code appendix of up to three pages. Title-page submission date remains blank for completion before submission.

## 9. Module 3: Concurrency and Deadlock Management

The project models citizen-service requests as concurrent processes competing for shared server resources. During Month 2, the team translated Module 3 concepts into runnable Python demonstrations covering race conditions, critical sections, mutual exclusion, inter-process communication, synchronization and deadlock management. The implementation includes a deterministic lost-update example and a mutex-protected counter; Peterson’s Solution, Strict Alternation and Lamport’s Bakery Algorithm; a non-atomic lock-variable interleaving; bounded-buffer Producer–Consumer; parent–child communication through `multiprocessing.Pipe`; binary and counting semaphores; a writer-preference Readers–Writers monitor; Dining Philosophers and Sleeping Barber simulations. Deadlock coverage includes resource-allocation graph cycle detection, Coffman conditions, Banker’s safety algorithm, multi-instance detection, recovery illustration and a database transaction wait-for graph simulation. The database example is a model, not an Oracle/MySQL integration. The Test-and-Set-style lock uses Python’s lock primitive and is not a hardware atomic instruction. The demonstrations are exposed through CLI commands and covered by automated tests. The latest complete local test run reported **140 tests passed**, with zero failures and zero errors in 0.355 seconds. The results validate the tested user-space models; they do not claim kernel-level implementation or deployment of a live government service platform [1]–[3].

## 10. Module 4: Memory Management

Module 4 work addresses memory management and related storage topics. Implemented demonstrations cover memory-management responsibilities; loading, linking and address binding; fixed and variable partition allocation using First Fit, Best Fit and Worst Fit; paging, segmentation and segmented paging; demand paging; FIFO, LRU, Optimal and LFU page replacement; Belady’s anomaly; working sets and thrashing risk; file access and allocation methods; and FCFS, SSTF, SCAN, C-SCAN, LOOK and C-LOOK disk scheduling. The memory-management overview explains tracking, allocation and reclamation, address translation, protection, controlled sharing, virtual-memory support and fragmentation management. Its CLI command ran successfully, and its two dedicated tests passed within the 140-test suite. The Windows 10 virtual-memory case study is research-based and does not represent local Windows measurements. The VM demonstration validates a hypothetical resource configuration but has not booted a guest operating system. A CUDA vector-addition simulation ran on the CPU; the optional CUDA source has not been compiled or executed on a GPU. These limits are retained explicitly rather than reported as completed hardware experiments [4]–[6].

## 17. References

1. Python Software Foundation, “multiprocessing — Process-based parallelism,” Python Documentation. https://docs.python.org/3/library/multiprocessing.html (accessed 3 Nov. 2026).
2. Microsoft, “Processes and Threads,” Microsoft Learn. https://learn.microsoft.com/en-us/windows/win32/procthread/processes-and-threads (accessed 3 Nov. 2026).
3. A. Silberschatz, P. B. Galvin, and G. Gagne, *Operating System Concepts*, 10th ed. Wiley, 2018.
4. Microsoft, “About Memory Management,” Microsoft Learn. https://learn.microsoft.com/en-us/windows/win32/memory/about-memory-management (accessed 3 Nov. 2026).
5. NVIDIA, *CUDA C++ Programming Guide*. https://docs.nvidia.com/cuda/cuda-c-programming-guide/ (accessed 3 Nov. 2026).
6. Integrated National Citizen Services Platform, Phase 2 source code, tests and verification records, branch `phase-2/concurrency-memory`. https://github.com/shutkarshX/Integrated-National-Citizen-Services-Platform/tree/phase-2/concurrency-memory (accessed 3 Nov. 2026).

## 18. Appendix — Source Code

The source code, tests, CLI entry point and evidence log are maintained in this repository under `phase-2/src/citizen_os/`, `phase-2/src/main.py`, `phase-2/tests/` and `phase-2/docs/EVIDENCE_LOG.md`. The CUDA kernel remains unverified on GPU hardware.
