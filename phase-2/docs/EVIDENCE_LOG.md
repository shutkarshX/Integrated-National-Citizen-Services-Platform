# Phase 2 Evidence Log

Record only genuine runs performed on the project machine. The following results were supplied from actual local runs on 2026-11-03.

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

## Producer–Consumer bounded-buffer demonstration

Command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py producer-consumer --items 20 --capacity 5
```

Observed output:

```text
items_requested: 20
items_consumed: 20
buffer_capacity: 5
expected_sum: 210
consumed_sum: 210
buffer_empty: True
```

The run transferred all 20 items, the sum matched the expected sum, and the buffer was empty after completion.

## Parent-child IPC demonstration

Command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py ipc-demo --message "hello from parent"
```

Observed output:

```text
sent: hello from parent
received: hello from parent
response: HELLO FROM PARENT
```

The parent sent a message through a multiprocessing Pipe, the child received it and returned the uppercase response.

## Automated tests

Command:

```bash
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

Observed result:

```text
Ran 13 tests in 0.236s

OK
```

All 13 tests reported `ok`; zero failures and zero errors. This includes eight tests in `test_concurrency.py` and five tests in `test_synchronization.py`.

## Evidence limitations

- These results verify the implemented concurrency, bounded-buffer and Pipe IPC demonstrations and their current tests.
- They do not verify unfinished Module 3 topics or any Module 4 topic.
- No screenshots or terminal-output attachments have been committed yet.
