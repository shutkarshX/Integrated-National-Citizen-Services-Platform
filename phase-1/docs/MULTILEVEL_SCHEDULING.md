# Multilevel CPU Scheduling — Phase 1 Notes

These algorithms are educational user-space simulations over the citizen-service workload. They do not change Linux kernel scheduling policy.

## Multilevel Queue (MLQ)

- The ready queue is divided into fixed queues.
- In this implementation, the `priority` field selects the queue: numeric priority 1 is the highest queue; larger values are lower queues.
- The process stays in its assigned queue for its entire lifetime.
- Each queue uses Round Robin with the same configurable time quantum.
- A ready process in a higher-priority queue preempts a process running in a lower-priority queue.
- Limitation: strict priority can starve lower-priority queues if higher-priority work keeps arriving.

Run: `python3 phase-1/src/main.py schedule --algorithm mlq --quantum 2`

## Multilevel Feedback Queue (MLFQ)

- There are multiple ready queues with different priority levels.
- New processes enter the top-priority queue.
- A process that consumes its full time slice without finishing is demoted to the next lower queue.
- A newly ready higher-queue process can preempt a lower-queue process.
- This implementation uses three queue quanta: 2, 4 and 8 time units.
- A preempted process keeps the unused part of its current time slice.
- At the lowest level, unfinished processes rotate using Round Robin.
- This basic version does not implement priority boosts/aging; starvation is therefore still possible.

Run: `python3 phase-1/src/main.py schedule --algorithm mlfq`

## Compare MLQ and MLFQ

| Feature | MLQ | MLFQ |
|---|---|---|
| Queue assignment | Fixed | Changes based on CPU use |
| Movement between queues | No | Yes, demotion |
| New process placement | Its configured priority queue | Top queue |
| Scheduling within queue | Round Robin | Round Robin with level-specific quantum |
| Higher-priority arrival | Preempts lower queue | Preempts lower queue |
| Starvation | Possible with strict priority | Possible in this basic version without aging |

## Verification

Run the full suite: `python3 -m unittest discover -s phase-1/tests -v`

Tests cover fixed-queue behavior, MLFQ demotion/completion, and invalid quantum configuration. Capture actual terminal output on the Ubuntu host before claiming practical execution evidence.