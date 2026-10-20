# Integrated National Citizen Services Platform

**Operating Systems PBL — Phase 1 starter baseline**

An educational command-line simulation of citizen-service requests, built to demonstrate operating-system concepts through a small, inspectable Python project.

## Scope

The simulator models four synthetic service categories:
- Certificate services
- Identity services
- Grievance redressal
- Tax services

Requests are represented as processes with simple lifecycle states and are processed using a deterministic First-Come, First-Served (FCFS) scheduler. Demo records are stored as JSON.

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

The initial starter baseline was tested locally: 11 unit tests passed. This is not a claim of a GitHub-hosted CI run.

## Current baseline and limitations

Implemented:
- A `ServiceRequest` model and lifecycle status values
- FCFS sequential request processing
- JSON save/load helpers
- A CLI demonstration using synthetic requests
- Unit tests for scheduler and storage behavior

Not yet implemented:
- Concurrent processing or real synchronization primitives
- Blocking/wakeup simulation for waiting requests
- Alternate CPU scheduling algorithms
- Deadlock experiments or role-based access control
- A web interface or integration with real public services

These are possible next steps after the baseline is reviewed and the Phase 1 scope is confirmed.

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
