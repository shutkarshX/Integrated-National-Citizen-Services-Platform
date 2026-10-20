"""Simple deterministic First-Come, First-Served scheduler."""

from collections.abc import Iterable

from .models import RequestState, ServiceRequest


def run_fcfs(requests: Iterable[ServiceRequest]) -> list[ServiceRequest]:
    """Process requests in input order and return the scheduled requests.

    This is a single-threaded educational simulation. It does not model
    preemption, blocking, concurrent execution, or real OS processes.
    """
    ordered = list(requests)
    clock = 0

    for request in ordered:
        if request.state == RequestState.TERMINATED:
            # Reset prior schedule so a repeated demo run stays deterministic.
            request.state = RequestState.NEW
            request.start_time = None
            request.finish_time = None

        request.state = RequestState.READY
        request.state = RequestState.RUNNING
        request.start_time = clock
        clock += request.burst_time
        request.finish_time = clock
        request.state = RequestState.TERMINATED

    return ordered
