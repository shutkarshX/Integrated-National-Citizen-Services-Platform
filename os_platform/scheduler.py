"""Simple deterministic First-Come, First-Served scheduler."""

from collections.abc import Iterable

from .models import RequestState, ServiceRequest


def run_fcfs(requests: Iterable[ServiceRequest]) -> list[ServiceRequest]:
    """Process requests in input order using FCFS and update PCB-like metadata.

    The simulated clock advances only while a request is running. If a request
    arrives after the CPU becomes idle, its start time is its arrival time.
    This is a single-threaded educational simulation; it does not model
    preemption, blocking, concurrent execution, or real OS processes.
    """
    ordered = list(requests)
    clock = 0

    for request in ordered:
        # Clear all scheduler-produced fields so rerunning is deterministic.
        request.state = RequestState.NEW
        request.start_time = None
        request.finish_time = None
        request.waiting_time = None
        request.turnaround_time = None

        request.state = RequestState.READY
        clock = max(clock, request.arrival_time)

        request.state = RequestState.RUNNING
        request.start_time = clock
        clock += request.burst_time
        request.finish_time = clock

        request.turnaround_time = request.finish_time - request.arrival_time
        request.waiting_time = request.turnaround_time - request.burst_time
        request.state = RequestState.TERMINATED

    return ordered
