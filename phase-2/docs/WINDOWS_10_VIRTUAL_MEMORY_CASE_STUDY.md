# Case Study: Virtual Memory Management in Windows 10

## Purpose and scope

The CCSE0303A syllabus asks for a study of virtual-memory management in a modern operating system such as Windows 10 and how paging affects performance. This document is a **documented research case study**, not a measurement performed on a Windows 10 machine. The project owner's verified development environment is Ubuntu; no Windows performance counters or Task Manager screenshots have been supplied.

## Virtual address spaces and paging

Windows applications use virtual addresses. The operating system and hardware translate virtual addresses to physical memory locations. This abstraction allows processes to operate in separate address spaces and lets the memory manager manage which pages are resident in physical RAM. The page file is not a direct copy of all RAM: Microsoft describes it as backing for infrequently accessed modified pages and as a way to extend the system commit limit.

## Page file and committed memory

Microsoft documents that the system commit limit is the sum of physical memory and page-file capacity. The commit charge represents committed virtual memory that the system has promised to back. If commit charge reaches the commit limit, allocations may fail and applications or the system can freeze or crash. A page file can also support crash dumps. Therefore, page-file use alone is not proof that a machine is short of RAM or running slowly.

## How paging affects performance

When a process references a page that is not resident, the memory manager must resolve the fault. A hard page fault requires storage I/O; this is much slower than a memory-resident access. Repeated hard faults can increase latency and disk activity. If active working sets compete for insufficient physical frames, frequent page movement can contribute to thrashing and poor responsiveness.

Microsoft cautions that hard page faults are not all page-file reads: they can also load executable images, DLLs and memory-mapped files. A high Pages/sec value alone does not prove a low-RAM bottleneck. It should be correlated with disk activity and related counters. Microsoft identifies Pages Output/sec, Page Reads/sec, Page Inputs/sec, Available MBytes, Committed Bytes, Commit Limit, and process Working Set as useful measurements.

## Suggested Windows 10 observation procedure

If a Windows 10 system becomes available, capture the following without changing page-file settings:

1. Open Task Manager → Performance → Memory and record In use, Available, Committed and the displayed memory configuration.
2. Open Resource Monitor → Memory and record Hard Faults/sec for the workload being observed.
3. Open Performance Monitor and collect `\\Memory\\Page Reads/sec`, `\\Memory\\Page Inputs/sec`, `\\Memory\\Pages Output/sec`, `\\Memory\\Available MBytes`, `\\Memory\\Committed Bytes`, `\\Memory\\Commit Limit`, and `\\Process(*)\\Working Set`.
4. Record the workload, observation duration and whether disk activity rises at the same time as hard faults.
5. Repeat under a lighter workload for comparison. Do not infer causation from one counter or one short sample.

## Link to the project simulator

The Phase 2 demand-paging simulator compares FIFO, LRU, Optimal and LFU using controlled page-reference strings. The effective-access-time model separately illustrates how fault rate and fault-service cost can affect average access time. These are teaching models; they are not measurements of the Windows 10 memory manager and do not reproduce Windows replacement policies.

## Findings

Windows virtual memory is used even when installed RAM is not exhausted. The page file supports committed memory and can hold modified pages that are not currently needed in RAM. Performance impact depends on the workload, fault frequency, storage latency and available memory. A page-file percentage or a single page-fault counter must not be treated as a standalone diagnosis.

## Limitations

No Windows 10 host was available for this project verification. Consequently, this case study contains Microsoft-documented behaviour and a proposed observation method, not locally measured Windows results. No claim is made that the project simulator implements Windows internals.

## References

1. Microsoft Learn, “Introduction to the page file” (applies to Windows 10): https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/introduction-to-the-page-file
2. Microsoft Learn, “How to determine the appropriate page file size for 64-bit versions of Windows” (applies to Windows 10): https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/how-to-determine-the-appropriate-page-file-size-for-64-bit-versions-of-windows
3. Microsoft Learn, “RAM, virtual memory, pagefile, and memory management in Windows”: https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/ram-virtual-memory-pagefile-management
