# Integrated National Citizen Services Platform

**Operating Systems PBL · CCSE0303A · Group 66**

An academic web application prototype that models a unified citizen-service experience. Citizens can explore a catalogue of sample services, submit a synthetic application, receive a reference number and look up its current status. The application workflow is supported by OS concepts implemented and studied across the project phases.

> This is an educational prototype. It is not an official government portal, does not connect to government databases or payment gateways, and must only be used with fictional demonstration information.

## Run the citizen-facing website

Requires Python 3.10+; no third-party packages are required.

```bash
python3 web_app.py
```

Open **http://127.0.0.1:8000**.

The portal includes a service catalogue, service-specific application form, input validation, locally persisted application records, generated reference numbers and status lookup. Records are stored in `data/citizen_applications.json`.

## Administrator dashboard

The local administrator console is available at **http://127.0.0.1:8000/admin**. Configure a password before starting the server:

```bash
export CIVICONE_ADMIN_PASSWORD='choose-a-local-demo-password'
python3 web_app.py
```

The dashboard lists submitted applications, supports search and status filters, and allows an administrator to move an application between `Submitted`, `Under Review`, `Approved` and `Rejected`. Status changes and a simple status history are persisted in the same local JSON store. The admin API requires a signed-in session; the citizen tracking endpoint continues to expose only the reference, service, status and submission time.

This is a local academic demonstration, not production authentication or a deployment-ready administrative system. Keep the server bound to localhost and use fictional applicant data.

## OS scheduling demonstration

The CPU scheduling browser demonstration is retained separately so it does not define the citizen-facing experience:

```bash
python3 os_lab_app.py
```

Open **http://127.0.0.1:8001**. It demonstrates synthetic process requests, FCFS, SJF, Priority and Round Robin scheduling. The OS lab uses its own local JSON store.

## Tests

Citizen portal HTTP tests:

```bash
PYTHONPATH=. python3 -m unittest discover -s phase-2/tests -p 'test_citizen_portal.py' -v
```

Administrator dashboard tests:

```bash
PYTHONPATH=. python3 -m unittest discover -s phase-2/tests -p 'test_admin_dashboard.py' -v
```

OS lab HTTP tests:

```bash
PYTHONPATH=. python3 -m unittest discover -s phase-2/tests -p 'test_web_integration.py' -v
```

Phase 1 tests:

```bash
python3 -m unittest discover -s phase-1/tests -v
```

Phase 2 tests:

```bash
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

## Project structure

- `web_app.py` — citizen-facing web portal.
- `os_lab_app.py` — separate browser-based CPU scheduling teaching demo.
- `os_platform/` — original repository-root process model and FCFS baseline.
- `phase-1/` — Phase 1 process, thread and scheduling work, notes and evidence.
- `phase-2/` — Phase 2 concurrency, deadlock, memory and storage demonstrations, tests and reports.
- `data/` — local synthetic demonstration records.

## Important scope notes

Applications are locally stored and initially receive the status **Submitted**. This prototype does not provide real identity verification, staff review, notifications, document uploads, payments or live government-service fulfilment. Status lookup returns only the reference, service, status and submission timestamp; it does not expose the stored contact fields.

The OS simulations are user-space educational models. They do not modify the Linux kernel scheduler, implement kernel internals or represent measured production-government workloads. Claims about hardware execution must be limited to the tests and environments actually used.
