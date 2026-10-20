# OS PBL — Phase 1 Syllabus Coverage Checklist

**Project:** Integrated National Citizen Services Platform  
**Course:** Operating System (CCSE0303A)  
**Group:** 66  
**Scope rule:** This checklist is limited to Modules 1 and 2. Submitted Report 1 is historical and must remain unchanged.

This is a working checklist, not a claim that every item is already implemented. Mark an item complete only after its explanation, demonstration, or evidence actually exists.

## Module 1 — OS fundamentals, Linux and shell

| Syllabus area | Current evidence/status | Phase 1 action |
|---|---|---|
| OS fundamentals, objectives and functions | Relevant theory; not separately evidenced by the code | Explain in Phase 1 technical notes and relate to request processing |
| OS architecture, kernel and system calls | Not implemented as real kernel/system-call behavior by this simulator | Explain accurately; do not claim the Python program implements a kernel |
| OS types and generations | Theory topic; no project feature required | Prepare concise syllabus-aligned notes/examples |
| Linux architecture and command-line interface | Not yet recorded as hands-on evidence | Run basic Linux commands and capture genuine terminal output |
| Shell scripting essentials | Added scripts/phase1_check.sh for project-file checks, test execution and CLI demonstration | Run it on Linux/WSL; capture actual output before marking verified |
| System-administration automation / case study | Script is a small project-check automation example | Explain purpose, commands used, error handling and observed result |

## Module 2 — Processes and CPU scheduling

| Syllabus area | Current evidence/status | Phase 1 action |
|---|---|---|
| Process concept and process states | ServiceRequest models a simulated process with lifecycle states | Explain state transitions; note that WAITING blocking/wakeup is not simulated |
| PCB | PCB-like metadata exists: request ID as simulated PID, state and timing fields | Document the mapping and its limitations |
| Scheduling/performance criteria | FCFS reports waiting and turnaround times; start/finish times are calculated | Show formulas and a worked example; do not imply all metrics are implemented |
| FCFS | Implemented and covered by tests | Keep as the current baseline |
| SJF, SRTF, non-preemptive/preemptive priority, Round Robin, multilevel queue and multilevel feedback queue | Not implemented | Decide which concepts need theory/comparison evidence for Phase 1; do not build extra algorithms unless the Phase 1 deliverable requires them |
| Processes, threads, thread states, benefits/types, multithreading models and hyper-threading | Not represented as real concurrent threads in the project | Cover through accurate notes/diagram or a small syllabus-required demonstration; do not claim concurrency exists |
| RTOS / real-time embedded CPU-scheduling case study | No case study recorded yet | Prepare a brief case study if required by Module 2 syllabus/report expectations |

## Verification record

- Existing implementation: FCFS, process-state model, PCB-like timing metadata, JSON storage and CLI demo.
- User-reported local verification on 2026-10-20: 12/12 unit tests passed and python main.py completed successfully.
- New shell script: **not yet verified on Linux/WSL**. Run bash scripts/phase1_check.sh from the repository root and record the actual result.
- Do not fabricate Linux screenshots, terminal output, report evidence or completion status.

## Explicitly outside current Phase 1 implementation

Do not add these merely to make the project larger: a web interface, real government integration, role-based access control, concurrency/synchronization primitives, or deadlock experiments. Revisit any item only if the confirmed later-phase syllabus specifically requires it. Do not assume these are automatically Phase 2 work; choose Phase 2 scope from Modules 3–4.

## Next Phase 1 steps

1. Pull this repository update.
2. Run bash scripts/phase1_check.sh on Linux/WSL and save genuine output.
3. Complete the theory/diagram/case-study evidence required by Modules 1–2.
4. Review the actual Phase 1 report requirements and mark only evidence-backed checklist items complete.
