# Integrated National Citizen Services Platform — Phase 1

Course: Operating Systems (CCSE0303A) · Group: 66 · Scope: official syllabus Modules 1 and 2.

Fresh Linux-first implementation workspace. The original repository-root implementation and submitted Report 1 are preserved unchanged.

## Included in this source drop
- Read-only Linux host inspection using Python standard library and common Linux utilities.
- Bash system audit: host, kernel, uptime, memory, filesystem and process snapshot.
- Application-level citizen-service process model with PCB-like metadata and lifecycle state.
- CPU scheduling simulations: FCFS, non-preemptive SJF, non-preemptive Priority, SRTF, Round Robin, Multilevel Queue (MLQ) and Multilevel Feedback Queue (MLFQ).
- Real user-space child-process creation and waiting using Python `subprocess` (not kernel-level process creation code).
- Concurrent worker threads sharing a counter protected by `threading.Lock`.
- Unit tests for process validation, scheduling, process execution and thread synchronization.

These are user-space educational simulations. They do not create or inspect kernel PCBs, change Linux scheduling policy, or integrate real government services. The scheduling algorithms simulate a workload; they do not replace the Linux kernel scheduler.

## Run from repository root
```bash
source .venv/bin/activate
python3 phase-1/src/main.py system
python3 phase-1/src/main.py process-demo
python3 phase-1/src/main.py thread-demo
python3 phase-1/src/main.py schedule --algorithm fcfs
python3 phase-1/src/main.py schedule --algorithm rr --quantum 2
python3 phase-1/src/main.py schedule --algorithm mlq --quantum 2
python3 phase-1/src/main.py schedule --algorithm mlfq
bash phase-1/scripts/linux_audit.sh
python3 -m unittest discover -s phase-1/tests -v
```

No third-party Python packages are required. Capture screenshots from the actual Linux machine after running these commands. Do not use illustrative output as evidence.

## Remaining work
IPC, synchronization primitives beyond the thread-lock demonstration, and RTOS implementation remain pending. Module 1 theory (interrupts, system calls, kernel architecture, OS generations/types) and Module 2 theory/case study still require documented study and evidence.