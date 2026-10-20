# Integrated National Citizen Services Platform

**Operating Systems PBL — implementation baseline**

An educational command-line simulation of citizen-service requests, built to demonstrate operating-system concepts through a small, inspectable Python project.

## Scope

The simulator models four synthetic service categories:
- Certificate services
- Identity services
- Grievance redressal
- Tax services

Each service request is represented as a simulated process. Its request ID acts as a process identifier, and the request stores PCB-like metadata: lifecycle state, arrival time, burst time, start time, finish time, waiting time, and turnaround time. The current scheduler uses deterministic First-Come, First-Served (FCFS) processing. Demo records are stored as JSON.

> This is an academic simulation. It does not connect to real government systems and uses synthetic demo data only.

## Requirements

- Python 3.10+ (standard library only)

## Run

```bash
python main.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Phase 1 Linux / shell automation check

On Linux or WSL, run this from the repository root:

```bash
bash scripts/phase1_check.sh
```

It checks required project files, runs the unit tests, and launches the synthetic CLI demo. It does not install packages or contact external services. The first run on your machine is still required before claiming either script has been verified. On Windows PowerShell, use the native equivalent:

```powershell
powershell -ExecutionPolicy Bypass -File .\\scripts\\phase1_check.ps1
```

See [the Phase 1 syllabus coverage checklist](docs/PHASE_1_CHECKLIST.md) for the Module 1–2 gap audit.

## Implemented

- `ServiceRequest` model with process lifecycle states: NEW, READY, RUNNING, WAITING, TERMINATED
- PCB-like scheduling metadata: arrival, burst, start, finish, waiting, and turnaround times
- FCFS sequential processing, including requests with later arrival times
- JSON save/load helpers
- CLI demonstration using synthetic requests
- Unit tests for scheduler timing, lifecycle outcome, repeat runs, and storage behavior

## Scheduling definitions

- **Waiting time** = start time − arrival time
- **Turnaround time** = finish time − arrival time
- **Finish time** = start time + burst time

The current implementation is deliberately single-threaded. FCFS processes requests in the supplied list order; it does not sort requests by arrival time. A later-arriving request causes the simulated CPU clock to wait until that request's arrival only when the clock is earlier than its arrival time.

## Not yet implemented

- Concurrent processing or real synchronization primitives
- Blocking/wakeup simulation for waiting requests
- Alternate CPU scheduling algorithms such as Round Robin or Priority
- Deadlock experiments or role-based access control
- A web interface or integration with real public services

These are possible next steps after the current baseline is tested and reviewed.

## Project structure

```text
.
├── main.py
├── os_platform/
│   ├── __init__.py
│   ├── models.py
│   ├── scheduler.py
│   └── storage.py
├── data/
│   └── demo_requests.json
└── tests/
    ├── test_scheduler.py
    └── test_storage.py
```

## Academic context

- Course: Operating Systems
- Course code: CCSE0303A
- Group: 66
- Project title: Integrated National Citizen Services Platform
- Academic year: 2026–27

The submitted Report 1 remains the historical record of what was submitted. This repository records the implementation baseline separately; dates and progress claims should reflect actual work and evidence.
