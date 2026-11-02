# Phase 2 Evidence Log

Record only genuine runs performed on the project machine. The following results were supplied from actual local runs on 2026-11-03.

## Environment

- Machine: project owner's Ubuntu desktop.
- Python: Python 3.14.
- Working directory: repository root, `Integrated-National-Citizen-Services-Platform`.
- Branch: `phase-2/concurrency-memory`.

## Previously verified demonstrations

The race condition, mutex, Peterson, Strict Alternation, Lamport Bakery, Test-and-Set-style lock, bounded-buffer Producer–Consumer and parent-child Pipe IPC results are retained in the preceding history of this log. Their source code and earlier execution records remain unchanged.

## Semaphore demonstrations

Binary semaphore command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py semaphore-demo --workers 6 --permits 1
```

Observed: 120 operations expected and completed; maximum simultaneous operations: 1.

Counting semaphore command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py semaphore-demo --workers 6 --permits 3
```

Observed: 120 operations expected and completed; maximum simultaneous operations: 3.

## Readers–Writers monitor

Command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py readers-writers --readers 4 --writers 2 --iterations 10
```

Observed:

```text
reads_completed: 40
writes_completed: 20
maximum_simultaneous_readers: 4
synchronization_violations: 0
```

## Dining Philosophers

Command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py dining-philosophers --philosophers 5 --meals 3
```

Observed: 5 philosophers; 3 meals each; 15 expected and 15 completed.

## Sleeping Barber

Command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py sleeping-barber --customers 10 --chairs 3
```

Observed:

```text
customers: 10
waiting_chairs: 3
served: 4
turned_away: 6
accounted_for: 10
```

The served/turned-away split depends on thread scheduling and is not a fixed expected result. The important invariant in this run is that served plus turned away equals all 10 customers.

## Full automated test suite

Command:

```bash
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

Observed result:

```text
Ran 20 tests in 0.245s

OK
```

All 20 tests reported `ok`; zero failures and zero errors. The suite includes the original concurrency tests, bounded-buffer / IPC tests, and semaphore / monitor / classical-problem tests.

## Evidence limitations

- These results verify the implemented concurrency, synchronization, bounded-buffer and Pipe IPC demonstrations and their current tests.
- Deadlock algorithms and Module 4 memory-management topics remain unimplemented/unverified.
- No screenshots or terminal-output attachments have been committed yet.
