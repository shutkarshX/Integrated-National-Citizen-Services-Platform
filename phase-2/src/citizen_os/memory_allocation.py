"""Contiguous memory allocation teaching simulations (fixed and variable partitions)."""
from __future__ import annotations

from collections.abc import Sequence

STRATEGIES = ("first-fit", "best-fit", "worst-fit")


def _validate_sizes(values: Sequence[int], label: str, *, allow_empty: bool = False) -> None:
    if not values and not allow_empty:
        raise ValueError(f"{label} must contain at least one size")
    if any(not isinstance(value, int) or isinstance(value, bool) or value <= 0 for value in values):
        raise ValueError(f"{label} sizes must be positive integers")


def _validate_strategy(strategy: str) -> None:
    if strategy not in STRATEGIES:
        raise ValueError(f"strategy must be one of: {', '.join(STRATEGIES)}")


def allocate_fixed_partitions(partition_sizes: Sequence[int], process_sizes: Sequence[int],
                              strategy: str = "first-fit") -> dict[str, object]:
    """Assign at most one process to each fixed partition; report internal fragmentation."""
    _validate_sizes(partition_sizes, "partition_sizes")
    _validate_sizes(process_sizes, "process_sizes", allow_empty=True)
    _validate_strategy(strategy)
    free = set(range(len(partition_sizes)))
    allocations: list[dict[str, int]] = []
    unallocated: list[int] = []

    for process_id, process_size in enumerate(process_sizes):
        candidates = [i for i in free if partition_sizes[i] >= process_size]
        if not candidates:
            unallocated.append(process_id)
            continue
        if strategy == "first-fit":
            chosen = min(candidates)
        elif strategy == "best-fit":
            chosen = min(candidates, key=lambda i: (partition_sizes[i], i))
        else:
            chosen = min(candidates, key=lambda i: (-partition_sizes[i], i))
        free.remove(chosen)
        allocations.append({
            "process": process_id, "process_size": process_size,
            "partition": chosen, "partition_size": partition_sizes[chosen],
            "internal_fragmentation": partition_sizes[chosen] - process_size,
        })

    return {
        "strategy": strategy,
        "allocations": allocations,
        "unallocated_processes": unallocated,
        "unused_partitions": sorted(free),
        "total_internal_fragmentation": sum(item["internal_fragmentation"] for item in allocations),
        "model": "Each fixed partition holds at most one process; unused space inside an assigned partition is internal fragmentation.",
    }


def allocate_variable_partitions(memory_size: int, process_sizes: Sequence[int],
                                 strategy: str = "first-fit") -> dict[str, object]:
    """Allocate variable-sized contiguous blocks by splitting the selected free hole."""
    _validate_sizes([memory_size], "memory_size")
    _validate_sizes(process_sizes, "process_sizes", allow_empty=True)
    _validate_strategy(strategy)
    holes: list[dict[str, int]] = [{"start": 0, "size": memory_size}]
    allocations: list[dict[str, int]] = []
    unallocated: list[int] = []

    for process_id, process_size in enumerate(process_sizes):
        candidates = [i for i, hole in enumerate(holes) if hole["size"] >= process_size]
        if not candidates:
            unallocated.append(process_id)
            continue
        if strategy == "first-fit":
            chosen = min(candidates, key=lambda i: (holes[i]["start"], i))
        elif strategy == "best-fit":
            chosen = min(candidates, key=lambda i: (holes[i]["size"], holes[i]["start"]))
        else:
            chosen = min(candidates, key=lambda i: (-holes[i]["size"], holes[i]["start"]))
        hole = holes.pop(chosen)
        allocations.append({
            "process": process_id, "process_size": process_size,
            "start": hole["start"], "end": hole["start"] + process_size,
            "allocated_size": process_size,
        })
        remainder = hole["size"] - process_size
        if remainder:
            holes.append({"start": hole["start"] + process_size, "size": remainder})
        holes.sort(key=lambda item: item["start"])

    total_free = sum(hole["size"] for hole in holes)
    largest_hole = max((hole["size"] for hole in holes), default=0)
    return {
        "strategy": strategy,
        "allocations": allocations,
        "unallocated_processes": unallocated,
        "free_holes": holes,
        "total_free_memory": total_free,
        "largest_free_hole": largest_hole,
        "external_fragmentation": total_free - largest_hole,
        "model": "Variable partitions split a selected free hole; external fragmentation is free memory spread across separate holes.",
    }


def run_fixed_partition_demo() -> dict[str, object]:
    partitions = [100, 500, 200, 300, 600]
    processes = [212, 417, 112, 426]
    return {
        strategy: allocate_fixed_partitions(partitions, processes, strategy)
        for strategy in STRATEGIES
    }


def run_variable_partition_demo(strategy: str = "first-fit") -> dict[str, object]:
    return allocate_variable_partitions(1000, [212, 417, 112, 426], strategy)
