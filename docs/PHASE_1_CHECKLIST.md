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
| Shell scripting essentials | Bash script exists; native PowerShell equivalent `scripts/phase1_check.ps1` was run successfully on Windows | Windows automation verified; Linux Bash execution remains pending |
| System-administration automation / case study | Project-check automation script and documentation exist | Explain purpose, commands used, error handling and observed result; add any course-required broader case study only if the rubric requires it |

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
- Windows PowerShell automation `scripts/phase1_check.ps1`: **verified by the user** on 2026-10-20; all six required files found, 12/12 tests passed in 0.044s, CLI demo completed, and success message printed.
- Bash automation `scripts/phase1_check.sh`: **not yet verified on Linux/WSL**. Run it only in an environment with Bash and record the actual result.
- Supporting notes and diagrams are now available in `docs/PHASE_1_OS_CONCEPTS.md` and `docs/PHASE_1_EVIDENCE_PACK.md`.
- Do not fabricate Linux screenshots, terminal output, report evidence or completion status.

## Explicitly outside current Phase 1 implementation

Do not add these merely to make the project larger: a web interface, real government integration, role-based access control, concurrency/synchronization primitives, or deadlock experiments. Revisit any item only if the confirmed later-phase syllabus specifically requires it. Do not assume these are automatically Phase 2 work; choose Phase 2 scope from Modules 3–4.

## Next Phase 1 steps

1. Pull the latest repository updates.
2. If Linux practical evidence is required, run `bash scripts/phase1_check.sh` on Linux/WSL and save genuine output; otherwise keep Linux execution marked pending.
3. Compare the checklist and supporting notes with the instructor's actual Phase 1 report requirements.
4. Capture genuine screenshots/output from the verified Windows run if evidence screenshots are required.
5. Mark remaining syllabus items complete only after the required explanation, demonstration, or evidence actually exists.
