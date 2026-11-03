# Final Browser Integration

This is the final integration layer for the Phase 1 citizen-service process model. It provides a local browser interface for registering synthetic service requests, persisting them to JSON, and running the Phase 1 CPU scheduling algorithms from the UI.

## Run

From the repository root:

```bash
python3 web_app.py
```

Open `http://127.0.0.1:8000` in a browser. Stop with Ctrl+C.

## Included

- Responsive operations dashboard with a request-entry form.
- Synthetic service categories matching the Phase 1 project scope.
- Local JSON persistence in `data/web_requests.json`.
- FCFS, non-preemptive SJF, non-preemptive Priority and Round Robin scheduling.
- Schedule timeline, per-process waiting/turnaround values and average metrics.
- Input validation and JSON API error responses.

## Scope and safety

This is a local academic prototype. It uses synthetic data, binds to loopback (`127.0.0.1`), has no authentication, and does not connect to government systems. Do not enter real personal information. The browser UI is an integration of the Phase 1 service-process/scheduler code; Phase 2 concurrency and memory demonstrations remain separate teaching modules and are not misrepresented as a production service backend.

## Verification

Run the web integration tests from the repository root:

```bash
PYTHONPATH=. python3 -m unittest phase-2.tests.test_web_integration -v
```

Also manually verify request creation, page refresh persistence, and each scheduling option in a browser. Record screenshots only after these steps have actually been run on the owner machine.