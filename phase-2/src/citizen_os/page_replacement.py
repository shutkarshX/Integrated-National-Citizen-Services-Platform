"""Demand-paging and page-replacement teaching simulations."""
from collections.abc import Sequence

ALGORITHMS = ("fifo", "lru", "optimal", "lfu")


def simulate_page_replacement(reference_string: Sequence[int], frame_count: int, algorithm: str) -> dict[str, object]:
    """Load pages on demand and simulate one replacement policy; LFU ties use LRU."""
    if not isinstance(frame_count, int) or isinstance(frame_count, bool) or frame_count <= 0:
        raise ValueError("frame_count must be a positive integer")
    if algorithm not in ALGORITHMS:
        raise ValueError(f"algorithm must be one of: {', '.join(ALGORITHMS)}")
    if any(not isinstance(page, int) or isinstance(page, bool) or page < 0 for page in reference_string):
        raise ValueError("reference_string must contain non-negative integer page numbers")

    frames = []
    loaded_at, last_used, frequency = {}, {}, {}
    trace, faults, hits = [], 0, 0
    for time, page in enumerate(reference_string):
        evicted = None
        if page in frames:
            hits += 1
            status = "hit"
        else:
            faults += 1
            status = "fault"
            if len(frames) == frame_count:
                if algorithm == "fifo":
                    victim = min(frames, key=lambda item: loaded_at[item])
                elif algorithm == "lru":
                    victim = min(frames, key=lambda item: last_used[item])
                elif algorithm == "optimal":
                    future = reference_string[time + 1:]
                    victim = max(frames, key=lambda item: future.index(item) if item in future else float("inf"))
                else:
                    victim = min(frames, key=lambda item: (frequency[item], last_used[item]))
                frames.remove(victim)
                evicted = victim
                del loaded_at[victim], last_used[victim], frequency[victim]
            frames.append(page)
            loaded_at[page] = time
            frequency[page] = 0
        frequency[page] += 1
        last_used[page] = time
        trace.append({"step": time + 1, "page": page, "status": status,
                      "frames": list(frames), "evicted": evicted})
    total = len(reference_string)
    return {"algorithm": algorithm.upper(), "reference_string": list(reference_string),
            "frame_count": frame_count, "page_faults": faults, "hits": hits,
            "hit_ratio": hits / total if total else 0.0,
            "fault_ratio": faults / total if total else 0.0, "trace": trace,
            "model": "A page is loaded on its first reference; a missing page causes a page fault."}


def compare_page_replacement(reference_string: Sequence[int], frame_count: int) -> dict[str, object]:
    return {name: simulate_page_replacement(reference_string, frame_count, name) for name in ALGORITHMS}


def run_demand_paging_demo() -> dict[str, object]:
    return {"concept": "Demand paging loads a page only when referenced; a missing page causes a page fault.",
            **simulate_page_replacement([7, 0, 1, 2, 0, 3, 0, 4], 3, "fifo")}


def run_page_replacement_comparison() -> dict[str, object]:
    reference = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
    return {"reference_string": reference, "frame_count": 3,
            "results": compare_page_replacement(reference, 3)}


def run_belady_anomaly_demo() -> dict[str, object]:
    reference = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    three = simulate_page_replacement(reference, 3, "fifo")
    four = simulate_page_replacement(reference, 4, "fifo")
    return {"algorithm": "FIFO", "reference_string": reference,
            "three_frames_faults": three["page_faults"], "four_frames_faults": four["page_faults"],
            "belady_anomaly_observed": four["page_faults"] > three["page_faults"],
            "explanation": "Belady's anomaly occurs when increasing frame count increases FIFO page faults for a particular reference string."}
