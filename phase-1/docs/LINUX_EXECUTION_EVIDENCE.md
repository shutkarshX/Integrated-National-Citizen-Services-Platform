# Phase 1 — Linux Execution Evidence

**Evidence source:** terminal output supplied by the user after running the commands on their Ubuntu machine.  
**Environment:** Ubuntu 26.04 LTS (Resolute Raccoon), Linux kernel 7.0.0-29-generic, x86_64, Python 3.14.4.  
**Host name shown in terminal:** zoro-pc.

This record summarizes the observed output. It is not a substitute for screenshots of the terminal.

## 1. Python unit tests

Command:

```bash
python3 -m unittest discover -s phase-1/tests -v
```

Observed result:

- 10 tests executed.
- All 10 passed.
- Runtime reported: 0.001 seconds.
- Final status: `OK`.

The passing tests cover process initialization and validation, PCB-like snapshot metadata, FCFS metrics, SJF order, non-preemptive Priority order, SRTF preemption, Round Robin completion, invalid quantum and empty workload.

## 2. Linux host inspection

Command:

```bash
python3 phase-1/src/main.py system
```

Observed successfully:
- Operating system: Linux.
- Distribution: Ubuntu 26.04 LTS.
- Kernel release: 7.0.0-29-generic.
- Architecture: x86_64.
- Python: 3.14.4.
- Uptime, memory and root filesystem information were returned.
- Root filesystem output showed 144G total, 15G used and 122G available at the time of execution.

## 3. Bash system audit

Command:

```bash
bash phase-1/scripts/linux_audit.sh
```

Observed successfully:
- Host and OS details via `hostnamectl`.
- Kernel details via `uname -a`.
- Uptime.
- Memory and swap summary.
- Root filesystem usage.
- A top-process snapshot from `ps`.
- Script ended with: `Audit complete. No system settings were changed.`

The terminal output contained a machine ID. It is intentionally omitted from this repository evidence record because it is a host-specific identifier and is not needed for the academic demonstration.

## 4. Round Robin scheduling demonstration

Command:

```bash
python3 phase-1/src/main.py schedule --algorithm rr --quantum 2
```

Observed result:

| PID | Service | Arrival | Burst | Completion | Waiting | Turnaround |
|---:|---|---:|---:|---:|---:|---:|
| 101 | Birth certificate | 0 | 5 | 14 | 9 | 14 |
| 102 | Address update | 1 | 3 | 11 | 7 | 10 |
| 103 | Pension enquiry | 2 | 8 | 20 | 10 | 18 |
| 104 | Grievance filing | 3 | 4 | 16 | 9 | 13 |

- Time quantum: 2.
- Average waiting time: 8.75.
- Average turnaround time: 13.75.
- All four simulated processes reached completion.

This is an application-level scheduling simulation. It does not alter Linux's actual process scheduler.

## 5. Remaining evidence task

For the final academic evidence pack, capture genuine screenshots from the Ubuntu terminal showing:
1. the 10 passing unit tests;
2. the Linux host-inspection output;
3. the Bash audit output;
4. the Round Robin schedule and metrics.

Do not fabricate or recreate screenshots from this text summary.

## 7. Multilevel Queue (MLQ) scheduling

Command: `python3 phase-1/src/main.py schedule --algorithm mlq --quantum 2`

User-provided Ubuntu output showed all four sample processes completed. Average waiting time: 5.00. Average turnaround time: 10.00. The observed timeline was `P101[0-1] -> P102[1-3] -> P102[3-4] -> P101[4-6] -> P104[6-8] -> P101[8-10] -> P104[10-12] -> P103[12-14] -> P103[14-16] -> P103[16-18] -> P103[18-20]`.

## 8. Multilevel Feedback Queue (MLFQ) scheduling

Command: `python3 phase-1/src/main.py schedule --algorithm mlfq`

User-provided Ubuntu output showed all four sample processes completed. Average waiting time: 8.75. Average turnaround time: 13.75. The observed timeline was `P101[0-2] -> P102[2-4] -> P103[4-6] -> P104[6-8] -> P101[8-11] -> P102[11-12] -> P103[12-16] -> P104[16-18] -> P103[18-20]`.

## 9. Updated automated test suite

Command: `python3 -m unittest discover -s phase-1/tests -v`

Observed result: 17 tests ran in 0.028 seconds; final status `OK`. This includes the four new MLQ/MLFQ tests. The user initially encountered one incorrect expected-timeline assertion in the MLQ test; after pulling the corrected test expectation, the full suite passed 17/17.

These records summarize terminal output supplied by the user. Genuine terminal screenshots are still required for the final evidence pack.