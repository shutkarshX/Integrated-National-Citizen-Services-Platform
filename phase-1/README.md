# Integrated National Citizen Services Platform — Phase 1

Course: Operating Systems (CCSE0303A) · Group: 66 · Scope: official syllabus Modules 1 and 2.

Fresh Linux-first implementation workspace. The original repository-root implementation and submitted Report 1 are preserved unchanged.

## Included in this source drop
- Read-only Linux host inspection using Python standard library and common Linux utilities.
- Bash system audit: host, kernel, uptime, memory, filesystem and process snapshot.
- Application-level citizen-service process model with PCB-like metadata and lifecycle state.
- CPU scheduling simulations: FCFS, non-preemptive SJF, non-preemptive Priority, SRTF and Round Robin.
- Unit tests for process validation and scheduling metrics.

These are user-space educational simulations. They do not create or inspect kernel PCBs, change Linux scheduling policy, or integrate real government services. The scheduling algorithms simulate a workload; they do not replace the Linux kernel scheduler.

## Run from repository root
    source .venv/bin/activate
    python3 phase-1/src/main.py system
    python3 phase-1/src/main.py schedule --algorithm fcfs
    python3 phase-1/src/main.py schedule --algorithm rr --quantum 2
    bash phase-1/scripts/linux_audit.sh
    python3 -m unittest discover -s phase-1/tests -v

No third-party Python packages are required. Capture screenshots from the actual Linux machine after running these commands. Do not use illustrative output as evidence.

## Not yet implemented / not claimed complete
Thread execution and multithreading models, real process creation with fork/exec, IPC, synchronization, multilevel scheduling, and RTOS implementation are not part of this initial source drop. Module 1 theory (interrupts, system calls, kernel architecture, OS generations/types) and Module 2 theory/case study still require documented study and evidence.
