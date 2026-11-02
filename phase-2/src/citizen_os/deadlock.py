"""Deadlock graphs, Banker's safety/request algorithms, detection and recovery."""
from __future__ import annotations

from collections.abc import Mapping, Sequence


def find_directed_cycle(graph: Mapping[str, Sequence[str]]) -> list[str] | None:
    """Return one directed cycle path, or None when the graph is acyclic."""
    state: dict[str, int] = {}
    stack: list[str] = []
    positions: dict[str, int] = {}

    def visit(node: str) -> list[str] | None:
        state[node] = 1
        positions[node] = len(stack)
        stack.append(node)
        for neighbour in graph.get(node, ()):
            if state.get(neighbour, 0) == 0:
                cycle = visit(neighbour)
                if cycle:
                    return cycle
            elif state.get(neighbour) == 1:
                return stack[positions[neighbour]:] + [neighbour]
        stack.pop()
        positions.pop(node, None)
        state[node] = 2
        return None

    nodes = set(graph)
    for neighbours in graph.values():
        nodes.update(neighbours)
    for node in sorted(nodes):
        if state.get(node, 0) == 0:
            cycle = visit(node)
            if cycle:
                return cycle
    return None


def resource_allocation_graph_demo() -> dict[str, object]:
    """Example with single-instance resources: P1->R2->P2->R1->P1."""
    graph = {"P1": ["R2"], "R2": ["P2"], "P2": ["R1"], "R1": ["P1"]}
    cycle = find_directed_cycle(graph)
    return {"cycle_detected": cycle is not None, "cycle": cycle or [],
            "interpretation": "For single-instance resource types, a cycle indicates deadlock."}


def _validate_matrix(allocation: Sequence[Sequence[int]], maximum: Sequence[Sequence[int]],
                     available: Sequence[int]) -> tuple[int, int]:
    if not allocation or len(allocation) != len(maximum):
        raise ValueError("allocation and maximum must have the same non-zero process count")
    resources = len(available)
    if resources == 0 or any(len(row) != resources for row in allocation) or any(len(row) != resources for row in maximum):
        raise ValueError("all resource vectors and matrix rows must have the same non-zero width")
    if any(value < 0 for row in allocation for value in row) or any(value < 0 for row in maximum for value in row) or any(value < 0 for value in available):
        raise ValueError("resource counts cannot be negative")
    if any(allocation[p][r] > maximum[p][r] for p in range(len(allocation)) for r in range(resources)):
        raise ValueError("allocation cannot exceed declared maximum")
    return len(allocation), resources


def bankers_safety(allocation: Sequence[Sequence[int]], maximum: Sequence[Sequence[int]],
                   available: Sequence[int]) -> dict[str, object]:
    """Run the Banker's safety algorithm and return a safe sequence when one exists."""
    processes, resources = _validate_matrix(allocation, maximum, available)
    need = [[maximum[p][r] - allocation[p][r] for r in range(resources)] for p in range(processes)]
    work = list(available)
    finish = [False] * processes
    sequence: list[int] = []

    while True:
        selected = None
        for p in range(processes):
            if not finish[p] and all(need[p][r] <= work[r] for r in range(resources)):
                selected = p
                break
        if selected is None:
            break
        for r in range(resources):
            work[r] += allocation[selected][r]
        finish[selected] = True
        sequence.append(selected)

    return {"safe": all(finish), "safe_sequence": sequence if all(finish) else [],
            "need": need, "work_at_end": work}


def bankers_request(allocation: Sequence[Sequence[int]], maximum: Sequence[Sequence[int]],
                    available: Sequence[int], process: int,
                    request: Sequence[int]) -> dict[str, object]:
    """Check and tentatively grant one process request using Banker's algorithm."""
    processes, resources = _validate_matrix(allocation, maximum, available)
    if not 0 <= process < processes or len(request) != resources or any(x < 0 for x in request):
        raise ValueError("invalid process index or request vector")
    need = [maximum[process][r] - allocation[process][r] for r in range(resources)]
    if any(request[r] > need[r] for r in range(resources)):
        return {"status": "rejected", "reason": "request exceeds declared remaining need"}
    if any(request[r] > available[r] for r in range(resources)):
        return {"status": "waiting", "reason": "resources are not currently available"}

    new_allocation = [list(row) for row in allocation]
    new_available = list(available)
    for r in range(resources):
        new_allocation[process][r] += request[r]
        new_available[r] -= request[r]
    safety = bankers_safety(new_allocation, maximum, new_available)
    if not safety["safe"]:
        return {"status": "unsafe", "reason": "grant would leave the system in an unsafe state"}
    return {"status": "granted", "safe_sequence": safety["safe_sequence"],
            "available_after": new_available}


def detect_deadlock(available: Sequence[int], allocation: Sequence[Sequence[int]],
                    outstanding_request: Sequence[Sequence[int]]) -> dict[str, object]:
    """Multi-instance deadlock detection using Available, Allocation and Request."""
    processes = len(allocation)
    if processes == 0 or len(outstanding_request) != processes:
        raise ValueError("allocation and request must have the same non-zero process count")
    resources = len(available)
    if resources == 0 or any(len(row) != resources for row in allocation) or any(len(row) != resources for row in outstanding_request):
        raise ValueError("all resource vectors and matrix rows must have the same non-zero width")
    if any(x < 0 for x in available) or any(x < 0 for row in allocation for x in row) or any(x < 0 for row in outstanding_request for x in row):
        raise ValueError("resource counts cannot be negative")

    work = list(available)
    finish = [not any(allocation[p]) for p in range(processes)]
    while True:
        selected = None
        for p in range(processes):
            if not finish[p] and all(outstanding_request[p][r] <= work[r] for r in range(resources)):
                selected = p
                break
        if selected is None:
            break
        for r in range(resources):
            work[r] += allocation[selected][r]
        finish[selected] = True
    deadlocked = [p for p, done in enumerate(finish) if not done]
    return {"deadlock_detected": bool(deadlocked), "deadlocked_processes": deadlocked,
            "finish": finish, "work_at_end": work}


def recover_by_terminating_victim(allocation: Sequence[Sequence[int]],
                                  deadlocked_processes: Sequence[int]) -> dict[str, object]:
    """Select the deadlocked process holding the most resources as a teaching recovery policy."""
    if not allocation or not deadlocked_processes:
        raise ValueError("allocation and at least one deadlocked process are required")
    if any(not 0 <= p < len(allocation) for p in deadlocked_processes):
        raise ValueError("deadlocked process index out of range")
    victim = max(deadlocked_processes, key=lambda p: (sum(allocation[p]), -p))
    released = list(allocation[victim])
    return {"victim_process": victim, "released_resources": released,
            "policy": "terminate the deadlocked process holding the largest total allocation"}


def deadlock_conditions_and_prevention() -> dict[str, object]:
    """Summarize Coffman conditions and a representative prevention strategy for each."""
    return {
        "necessary_conditions": [
            "Mutual exclusion: at least one resource is non-shareable.",
            "Hold and wait: a process holds resources while waiting for more.",
            "No preemption: resources cannot be forcibly taken away.",
            "Circular wait: a circular chain of processes waits for resources held by the next process.",
        ],
        "prevention_strategies": {
            "mutual exclusion": "Make resources shareable where the resource semantics permit.",
            "hold and wait": "Require processes to request all needed resources together, or release held resources before requesting more.",
            "no preemption": "Allow resource preemption when safe and meaningful for that resource type.",
            "circular wait": "Impose a global ordering on resource types and request them only in increasing order.",
        },
    }


def run_bankers_demo() -> dict[str, object]:
    allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    maximum = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    available = [3, 3, 2]
    return bankers_safety(allocation, maximum, available)
