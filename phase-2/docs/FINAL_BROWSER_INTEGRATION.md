# Final Browser Integration

The final integration layer connects the Phase 1 citizen-service process model and CPU schedulers to a local browser interface. It is an academic prototype using synthetic records only.

## Run

From the repository root:

```bash
python3 web_app.py
```

Open `http://127.0.0.1:8000`. Stop the server with Ctrl+C.

## Included

- Responsive dashboard and service-request form.
- Local JSON persistence at `data/web_requests.json`.
- FCFS, non-preemptive SJF, non-preemptive Priority and Round Robin scheduling.
- Schedule timeline, per-process waiting/turnaround values and average metrics.
- Input validation and JSON API error responses.

## Automated checks

```bash
PYTHONPATH=. python3 -m unittest discover -s phase-2/tests -p 'test_web_integration.py' -v
```

The HTTP-level tests cover homepage delivery, request creation and persistence, invalid input, scheduling, and the empty-queue case. Run the command on the owner machine and record the actual result before marking this integration verified.

## Manual browser acceptance

1. Start the server and open the local URL.
2. Add at least two fictional service requests with different burst times.
3. Refresh the page and confirm both requests remain listed.
4. Run FCFS, SJF, Priority and Round Robin; confirm each produces a timeline and waiting/turnaround values.
5. Try an invalid request and confirm the form displays a validation message.
6. Capture screenshots from the actual browser after these steps.

## Scope and safety

The server binds to loopback (`127.0.0.1`), has no authentication and does not connect to government systems. Do not enter real personal information. This browser layer integrates Phase 1 request/scheduling functionality; Phase 2 concurrency and memory-management demonstrations remain separate teaching modules, not a production backend.
