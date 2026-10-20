# Phase 1 OS Concepts — Module 1 and Module 2 Notes

**Project:** Integrated National Citizen Services Platform  
**Course:** Operating System (CCSE0303A)  
**Purpose:** Connect Module 1–2 syllabus concepts to the project without claiming that a Python simulation implements real kernel functionality.

> These notes are study/documentation material. They are not proof of a practical activity unless the activity was actually performed and recorded.

## Module 1 — Operating-system fundamentals

### 1. Meaning and objectives of an operating system
An operating system (OS) is system software that manages computer hardware and provides services to application programs. Its objectives include convenience, efficient resource use, controlled access to resources, and reliable execution.

**Connection to this project:** The program is a user-space educational simulation of how requests can be queued and processed. The operating system running Python still manages the actual CPU, memory, files, and process execution. This project does not replace or implement an OS.

### 2. Main OS functions
- **Process management:** creates, schedules, and terminates processes.
- **Memory management:** allocates and reclaims main memory.
- **File management:** organizes files and controls file operations.
- **I/O management:** coordinates input/output devices and operations.
- **Protection and security:** restricts unauthorized access.
- **Resource allocation and accounting:** distributes and tracks resources.

**Project connection:** JSON persistence demonstrates application-level file handling; FCFS demonstrates scheduling concepts in simulation. It does not implement OS memory management, device drivers, or kernel protection.

### 3. OS architecture, kernel and system calls
The **kernel** is the privileged core of an OS. It manages low-level resources and provides controlled services. Applications request OS services through **system calls**, such as operations related to files, processes, or memory.

A simplified relationship is:

`User application → system-call interface → kernel → hardware`

The Python program uses services provided by the host OS through the Python runtime and standard library. Its scheduler function is not a kernel scheduler and its request IDs are not real operating-system PIDs.

### 4. Types and generations of operating systems
Common OS categories include batch, multiprogramming, time-sharing/multitasking, multiprocessing, distributed, network, real-time, and embedded systems. These categories describe different goals and execution environments; they are not all mutually exclusive.

For revision, learn the definition, one characteristic, and one suitable use case for each type as taught in the course material. The project itself is not an RTOS or distributed system.

### 5. Linux command line
Common commands useful for examining this project include:

| Command | Purpose |
|---|---|
| `pwd` | Print current working directory |
| `ls` | List directory contents |
| `cd path` | Change directory |
| `cat file` | Display a text file |
| `grep pattern file` | Search text |
| `find . -name '*.py'` | Find Python files |
| `python3 --version` | Show Python version |
| `python3 -m unittest discover -s tests -v` | Run the test suite |
| `bash scripts/phase1_check.sh` | Run the Bash project check, when Bash is installed |

**Environment note:** The user's verified environment is Windows PowerShell with Python 3.14.7. The PowerShell check script has passed there. That does not establish that the Bash script has been run on Linux.

### 6. Shell scripting and automation
A shell script combines commands into a repeatable procedure. The project's `scripts/phase1_check.sh` checks required files, runs tests, and starts the demo. The Windows equivalent is `scripts/phase1_check.ps1`.

The PowerShell script was run by the user on 2026-10-20 and completed successfully: all six required files were found, all 12 unit tests passed, and the demo completed. This is genuine Windows verification, not Linux verification.

## Module 2 — Processes and scheduling

### 1. Process and process states
A process is a program in execution with associated state and resources. Typical conceptual states include **new**, **ready**, **running**, **waiting/blocked**, and **terminated**.

The simulator's `ServiceRequest` uses these labels as educational states. The current FCFS function moves each request through READY, RUNNING, and TERMINATED. WAITING is defined in the model, but blocking and wake-up behavior are not simulated.

### 2. Process Control Block (PCB)
An OS PCB stores information needed to manage a process, such as its identifier, state, scheduling information, and context information.

The project has **PCB-like** fields:
- `request_id`: simulated identifier (not a real OS PID)
- `state`: simulated lifecycle state
- `arrival_time`, `burst_time`
- `start_time`, `finish_time`
- `waiting_time`, `turnaround_time`

This is a simplified application data model, not a real kernel PCB.

### 3. FCFS scheduling
First-Come, First-Served (FCFS) is a non-preemptive scheduling algorithm: requests are processed in arrival/input order in this project's simplified model, and a running request is not interrupted by the scheduler.

For the current demo, all arrival times are zero and burst times are 3, 2, 4, and 1.

| Request | Burst | Start | Finish | Waiting | Turnaround |
|---|---:|---:|---:|---:|---:|
| REQ-001 | 3 | 0 | 3 | 0 | 3 |
| REQ-002 | 2 | 3 | 5 | 3 | 5 |
| REQ-003 | 4 | 5 | 9 | 5 | 9 |
| REQ-004 | 1 | 9 | 10 | 9 | 10 |

Formulas used by the implementation:

- Finish time = start time + burst time
- Turnaround time = finish time − arrival time
- Waiting time = turnaround time − burst time (equivalently, start time − arrival time in this non-preemptive simulation)

The displayed times are simulated time units, not seconds of real elapsed time.

### 4. Scheduling performance criteria
- **CPU utilization:** percentage of time the CPU is busy.
- **Throughput:** number of processes completed per unit time.
- **Turnaround time:** time from arrival to completion.
- **Waiting time:** time spent waiting in the ready queue.
- **Response time:** time from arrival until the process first receives CPU service.

The current program calculates waiting and turnaround time and displays start/finish times. It does not currently calculate CPU utilization, throughput, or response time as separate reported metrics.

### 5. Other CPU scheduling algorithms — theory only
The following are syllabus topics, not implemented project features. Do not claim these algorithms are in the code.

| Algorithm | Core idea | Main consideration |
|---|---|---|
| SJF | Select the ready process with the shortest CPU burst | Can reduce average waiting time when burst lengths are known |
| SRTF | Preemptive version of shortest-job scheduling; select least remaining time | A new short job may preempt a running job |
| Non-preemptive Priority | Select highest-priority ready process; let it finish | Low-priority jobs may starve |
| Preemptive Priority | Higher-priority arrival can interrupt current process | Priority starvation is possible |
| Round Robin | Give each ready process a time quantum in rotation | Quantum size affects responsiveness and context-switch overhead |
| Multilevel Queue | Separate queues for different process classes, with defined queue scheduling | Processes generally remain in assigned queues |
| Multilevel Feedback Queue | Processes may move between queues based on behavior/aging rules | Flexible but more complex to configure |

### 6. Threads and multithreading
A thread is an execution path within a process. Threads in the same process can share resources, while each thread has its own execution state and stack. Multithreading can improve responsiveness and overlap work, but shared data requires careful coordination.

This project currently processes requests sequentially in one Python execution flow. It does **not** implement concurrent threads, multithreading models, hyper-threading, locks, or semaphores.

### 7. RTOS / embedded scheduling case study (conceptual)
A real-time embedded controller, such as a medical monitoring device or industrial controller, may need to respond within deadlines. A hard real-time system treats missing a critical deadline as unacceptable; a soft real-time system can tolerate occasional lateness with degraded quality. Scheduling choices depend on task periods, execution times, priorities, deadlines, and the consequences of delay.

This is a conceptual study example only; the citizen-services simulator is not a real-time system.

## Verified implementation evidence (2026-10-20)
The user ran `powershell -ExecutionPolicy Bypass -File .\scripts\phase1_check.ps1` on Windows with Python 3.14.7. The script reported:
- all six required project files found;
- 12/12 unit tests passed in 0.044 seconds;
- the four-request CLI demo completed;
- final message: `Phase 1 project check completed successfully.`

This evidence verifies the current Windows project check, unit tests, and demo. It does not prove Linux execution, concurrency, real kernel behavior, or full coverage of every syllabus topic.

## Phase boundary
This document covers Phase 1 study and implementation evidence for Modules 1–2 only. Do not add features solely to make the project larger. Submitted Report 1 remains unchanged. Phase 2 and Phase 3 implementation are out of scope until Phase 1 is checked against the actual requirements.
