# Phase 2 Evidence Log

Record only genuine runs performed on the project machine. The following results were supplied from an actual local run on 2026-11-03.

## Environment

- Machine: project owner's Ubuntu desktop.
- Python: Python 3.14 (identified from the local Python standard-library traceback during initial test discovery).
- Working directory: repository root, `Integrated-National-Citizen-Services-Platform`.
- Branch: `phase-2/concurrency-memory`.

## Race-condition demonstration

Command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py race-demo
```

Observed output:

```text
workers: 2
increments_per_worker: 100
expected_total: 200
actual_total: 100
lost_updates: 100
```

Interpretation: the controlled unsynchronized read-modify-write demonstrates 100 lost updates in this run.

## Mutex-protected counter

Command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py locked-demo
```

Observed output:

```text
workers: 4
increments_per_worker: 1000
expected_total: 4000
actual_total: 4000
```

## Mutual-exclusion algorithm demonstrations

| Algorithm | Participants | Increments per participant | Expected total | Actual total |
|---|---:|---:|---:|---:|
| Peterson | 2 | 500 | 1,000 | 1,000 |
| Strict alternation | 2 | 500 | 1,000 | 1,000 |
| Lamport Bakery | 4 | 500 | 2,000 | 2,000 |
| Test-and-Set-style lock | 4 | 500 | 2,000 | 2,000 |

Each demonstration completed and printed the expected and actual totals as equal. The Test-and-Set-style example uses Python's `threading.Lock.acquire(blocking=False)` as a user-space primitive; it does not invoke a hardware atomic Test-and-Set instruction.

## Automated tests

Command:

```bash
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

Observed result:

```text
Ran 8 tests in 0.162s

OK
```

All eight tests reported `ok`; zero failures and zero errors.

## Evidence limitations

- These results verify the current concurrency demonstrations and the eight tests in `phase-2/tests/test_concurrency.py`.
- They do not verify unfinished Module 3 topics or any Module 4 topic.
- No screenshots or terminal-output attachments have been committed yet.
