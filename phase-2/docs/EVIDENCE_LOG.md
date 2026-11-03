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


## Deadlock management demonstrations — locally verified 2026-11-03

The project owner pulled the deadlock implementation and ran the CLI help, all six demonstrations, and the complete automated test suite on the Ubuntu project machine.

CLI syntax/help command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py --help
```

Observed: command completed successfully and listed `rag-demo`, `banker-demo`, `deadlock-detection`, `deadlock-prevention`, `deadlock-recovery`, and `database-deadlock`.

### Resource Allocation Graph

Command: `PYTHONPATH=phase-2/src python3 phase-2/src/main.py rag-demo`

Observed:
```text
cycle_detected: True
cycle: ['P1', 'R2', 'P2', 'R1', 'P1']
```

This example uses single-instance resource types, for which a cycle indicates deadlock.

### Banker's Algorithm

Command: `PYTHONPATH=phase-2/src python3 phase-2/src/main.py banker-demo`

Observed:
```text
safe: True
safe_sequence: [1, 3, 0, 2, 4]
need: [[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]]
work_at_end: [10, 5, 7]
```

The observed safe sequence differs from other valid sequences for the classic example; it is valid because the algorithm found a completion order in which each process's remaining need could be met.

### Multi-instance deadlock detection

Command: `PYTHONPATH=phase-2/src python3 phase-2/src/main.py deadlock-detection`

Observed:
```text
deadlock_detected: True
deadlocked_processes: [0, 1]
finish: [False, False]
work_at_end: [0, 0]
```

### Coffman conditions and prevention

Command: `PYTHONPATH=phase-2/src python3 phase-2/src/main.py deadlock-prevention`

Observed: all four necessary conditions were printed (mutual exclusion, hold and wait, no preemption, circular wait), together with a corresponding prevention strategy for each.

### Deadlock recovery

Command: `PYTHONPATH=phase-2/src python3 phase-2/src/main.py deadlock-recovery`

Observed:
```text
victim_process: 1
released_resources: [0, 3]
policy: terminate the deadlocked process holding the largest total allocation
```

This is an illustrative victim-selection policy, not a universal OS policy.

### Database transaction deadlock

Command: `PYTHONPATH=phase-2/src python3 phase-2/src/main.py database-deadlock`

Observed:
```text
transactions: ['T1', 'T2']
locks_held: {'T1': 'Row-A', 'T2': 'Row-B'}
waiting_for: {'T1': 'Row-B (held by T2)', 'T2': 'Row-A (held by T1)'}
deadlock_detected: True
wait_for_cycle: ['T1', 'T2', 'T1']
```

The case study models two transactions holding one row lock each and waiting for the other's lock; rolling back one transaction releases its locks.

### Updated full test suite

Command:

```bash
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

Observed result:

```text
Ran 32 tests in 0.242s

OK
```

All 32 tests reported `ok`; zero failures and zero errors. The CLI help and all six deadlock commands also completed successfully.

## Evidence limitations

- These results verify the implemented concurrency, synchronization, bounded-buffer and Pipe IPC demonstrations and their current tests.
- Deadlock management algorithms and CLI demonstrations are locally verified as recorded above.
- Module 4 progress and remaining topics are tracked in `phase-2/docs/IMPLEMENTATION_STATUS.md`; allocation, address translation, demand paging and replacement are verified as detailed below.
- No screenshots or terminal-output attachments have been committed yet.


## Memory allocation — locally verified 2026-11-03

The project owner pulled commit `f402b53`, compiled the memory-allocation module and CLI entry point, ran the fixed-partition comparison, ran variable-partition First Fit, Best Fit and Worst Fit, and ran the full test suite.

Compilation command:

```bash
PYTHONPATH=phase-2/src python3 -m py_compile phase-2/src/citizen_os/memory_allocation.py phase-2/src/main.py
```

Observed: compilation completed with no errors.

Fixed-partition comparison completed for First Fit, Best Fit and Worst Fit. In this sample, First Fit and Worst Fit each left one process unallocated; Best Fit allocated all four. Internal fragmentation totals observed were 559, 433 and 659 units respectively.

Variable-partition commands:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py variable-partitions --strategy first-fit
PYTHONPATH=phase-2/src python3 phase-2/src/main.py variable-partitions --strategy best-fit
PYTHONPATH=phase-2/src python3 phase-2/src/main.py variable-partitions --strategy worst-fit
```

Observed comparison:

- First Fit: 280 units total free; largest hole 160; external fragmentation 120.
- Best Fit: 280 units total free; largest hole 250; external fragmentation 30.
- Worst Fit: 280 units total free; largest hole 110; external fragmentation 170.

All three strategies allocated the three sample processes. These values are specific to the demonstration's initial holes and process sequence.

Updated full test suite:

```bash
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

Observed: `Ran 44 tests in 0.241s`, `OK`; zero failures and zero errors. The 44 tests include the memory-allocation tests as well as the earlier concurrency, synchronization and deadlock tests.

## Paging and segmentation — source added, local verification pending

Added `phase-2/src/citizen_os/address_translation.py` and `phase-2/tests/test_address_translation.py`.

The module demonstrates:
- Paging: logical page number and offset calculation, page-table lookup, and physical-address construction.
- Segmentation: segment selection, base-plus-offset translation, and limit checking.
- Segmented paging: segment selection followed by page-table lookup and frame-plus-offset translation.

These are educational address-translation simulations, not actual hardware MMU or kernel implementations. The new test cases and CLI commands have not yet been run locally by the project owner.


## Paging, segmentation and segmented paging — locally verified 2026-11-03

The project owner pulled the address-translation implementation and ran all three CLI demonstrations and the complete test suite.

### Paging

Command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py paging-demo
```

Observed:
- Page size: 1024 bytes.
- Logical address: 2500.
- Page number: 2; offset: 452.
- Page table maps page 2 to frame 2.
- Physical address returned: 2500.

### Segmentation

Command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py segmentation-demo
```

Observed:
- Segment number: 1; offset: 120.
- Base: 5000; limit: 800.
- Physical address returned: 5120.

### Segmented paging

Command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py segmented-paging-demo
```

Observed:
- Segment number: 1; offset: 1500.
- Page number: 1; page offset: 476.
- Page table maps this page to frame 3.
- Physical address returned: 3548.

### Updated full automated test suite

Command:

```bash
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

Observed:

```text
Ran 55 tests in 0.246s

OK
```

All 55 tests reported `ok`; zero failures and zero errors. This includes the 10 address-translation tests and all previously implemented tests.

### Scope note

These demonstrations verify educational address-translation logic in user space. They do not implement a hardware MMU or kernel memory-management subsystem.


## Demand paging and page replacement — locally verified 2026-11-03

The project owner ran all three new demonstrations and the complete updated test suite after pulling the correction to the demand-paging test expectation.

### Demand paging demonstration

Command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py demand-paging-demo
```

Observed with FIFO and 3 frames, reference string `[7, 0, 1, 2, 0, 3, 0, 4]`:
- Page faults: 7.
- Hits: 1.
- Hit ratio: 0.125.
- Fault ratio: 0.875.

The first three references fill the frames. The later missing pages cause replacement faults; the reference to page 0 at step 5 is the only hit.

### Page-replacement comparison

Command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py page-replacement-demo
```

Observed with 3 frames and reference string `[7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]`:

| Algorithm | Page faults | Hits |
|---|---:|---:|
| FIFO | 10 | 3 |
| LRU | 9 | 4 |
| Optimal | 7 | 6 |
| LFU | 8 | 5 |

LFU uses least-recently-used as its tie-break when resident pages have equal reference frequency. Optimal is a theoretical benchmark because it uses future references.

### Belady's Anomaly

Command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py belady-anomaly-demo
```

Observed using FIFO and reference string `[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]`:
- 3 frames: 9 page faults.
- 4 frames: 10 page faults.
- `belady_anomaly_observed: True`.

This reproduces Belady's Anomaly: increasing frame count increased FIFO page faults for this reference string.

### Corrected test expectation and full suite

The first run exposed one incorrect test expectation: the FIFO demand-paging sample produced 7 page faults, while its test expected 6. The implementation trace confirmed 7 faults and 1 hit. The test was corrected to expect 7; no algorithm change was required.

After pulling commit `6df588a`, the project owner reran:

```bash
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

Observed:

```text
Ran 67 tests in 0.241s

OK
```

All 67 tests reported `ok`; zero failures and zero errors. The three CLI demonstrations and complete test suite are locally verified. These are user-space teaching simulations, not a kernel virtual-memory implementation.


## Working-set model and thrashing risk — source added, local verification pending

Added `phase-2/src/citizen_os/working_set.py` and `phase-2/tests/test_working_set.py`.

The model computes the distinct pages in each trailing reference window and flags a memory-pressure step when that working-set size exceeds the process's allocated frame count. The sample uses a five-reference window and three allocated frames. This is an educational working-set pressure indicator; it does not measure real system page-fault frequency or detect kernel-level thrashing.

Commands to run from the repository root after pulling:

```bash
PYTHONPATH=phase-2/src python3 -m py_compile phase-2/src/citizen_os/working_set.py phase-2/src/main.py
PYTHONPATH=phase-2/src python3 phase-2/src/main.py working-set-demo
PYTHONPATH=phase-2/src python3 phase-2/src/main.py thrashing-demo
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

The new implementation includes 10 focused tests. These commands have not yet been run on the project owner's Ubuntu machine; outputs and test count must be added after actual execution.


## Working-set model and thrashing risk — locally verified 2026-11-03

The project owner pulled the implementation and ran compilation, both demonstrations and the complete test suite on the Ubuntu project machine.

Compilation:

```bash
PYTHONPATH=phase-2/src python3 -m py_compile phase-2/src/citizen_os/working_set.py phase-2/src/main.py
```

Observed: completed with no compilation errors.

Commands executed:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py working-set-demo
PYTHONPATH=phase-2/src python3 phase-2/src/main.py thrashing-demo
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

Both demonstrations completed successfully. The sample reference string was `[1, 2, 3, 4, 5, 1, 2, 3, 4, 5]`, with a trailing window of 5 references and 3 allocated frames. Observed peak working-set size: 5 pages; memory-pressure steps: 7; `thrashing_risk_observed: True`.

The complete test suite reported:

```text
Ran 77 tests in 0.432s

OK
```

All 77 tests reported `ok`; zero failures and zero errors. The new working-set test module contributes 10 tests. This is an educational working-set/frame-pressure simulation, not an actual kernel thrashing detector or measurement of real page-fault frequency.


## Loading, linking and address binding — source added, local verification pending

Added `phase-2/src/citizen_os/loading_linking.py` and `phase-2/tests/test_loading_linking.py`.

The module provides an educational model of external-symbol resolution across modules, loader-assigned consecutive load bases, relocation of exported symbol addresses, and load-base plus relative-address translation. The CLI command is `loading-linking-demo`. The demo includes compile-time, load-time and execution-time binding explanations.

Run from the repository root after pulling:

```bash
PYTHONPATH=phase-2/src python3 -m py_compile phase-2/src/citizen_os/loading_linking.py phase-2/src/main.py
PYTHONPATH=phase-2/src python3 phase-2/src/main.py loading-linking-demo
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

The new test module contains 11 tests. This is a user-space teaching model, not a real object-file linker, executable loader, process loader or hardware address-translation implementation. Local verification is pending; actual output must be recorded after the project owner runs these commands.


## Loading, linking and address binding — locally verified 2026-11-03

The project owner pulled the implementation and ran compilation, the CLI demonstration and the complete test suite on the Ubuntu project machine.

Compilation command:

```bash
PYTHONPATH=phase-2/src python3 -m py_compile phase-2/src/citizen_os/loading_linking.py phase-2/src/main.py
```

Observed: compilation completed with no errors.

CLI command:

```bash
PYTHONPATH=phase-2/src python3 phase-2/src/main.py loading-linking-demo
```

Observed:
- External reference `application:calculate_tax` resolved to the `tax_library` module.
- Application module load base: 4096; size: 256.
- Tax library load base: 4352; size: 128.
- Relocated `calculate_tax` absolute address: 4384 (relative address 32 plus load base 4352).
- Next free address after loading both modules: 4480.
- The demo completed and printed compile-time, load-time and execution-time binding explanations.

Full test command:

```bash
PYTHONPATH=phase-2/src python3 -m unittest discover -s phase-2/tests -v
```

Observed:

```text
Ran 88 tests in 0.353s

OK
```

All 88 tests reported `ok`; zero failures and zero errors. The loading/linking test module contributes 11 tests. The implementation remains an educational user-space model, not a real object-file linker, executable loader or hardware MMU.
