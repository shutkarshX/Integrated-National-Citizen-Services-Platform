"""Working-set and thrashing teaching simulations."""
from collections.abc import Sequence


def analyze_working_set(reference_string: Sequence[int], window_size: int, frame_count: int) -> dict[str, object]:
    """Measure each trailing working set and flag when it exceeds allocated frames.

    The working set at step t contains distinct pages referenced in the most
    recent window_size references, including the current reference.
    """
    if not isinstance(window_size, int) or isinstance(window_size, bool) or window_size <= 0:
        raise ValueError("window_size must be a positive integer")
    if not isinstance(frame_count, int) or isinstance(frame_count, bool) or frame_count <= 0:
        raise ValueError("frame_count must be a positive integer")
    if any(not isinstance(page, int) or isinstance(page, bool) or page < 0 for page in reference_string):
        raise ValueError("reference_string must contain non-negative integer page numbers")

    trace = []
    pressure_steps = 0
    peak_working_set = 0
    for index, page in enumerate(reference_string):
        start = max(0, index - window_size + 1)
        window = list(reference_string[start:index + 1])
        working_set = sorted(set(window))
        size = len(working_set)
        pressure = size > frame_count
        pressure_steps += int(pressure)
        peak_working_set = max(peak_working_set, size)
        trace.append({
            "step": index + 1, "page": page, "window_references": window,
            "working_set": working_set, "working_set_size": size,
            "allocated_frames": frame_count, "memory_pressure": pressure,
        })

    return {
        "window_size": window_size, "allocated_frames": frame_count,
        "reference_count": len(reference_string), "peak_working_set": peak_working_set,
        "memory_pressure_steps": pressure_steps,
        "thrashing_risk_observed": pressure_steps > 0, "trace": trace,
        "model": "A step is flagged when its trailing working-set size exceeds the process frame allocation; this is an educational pressure indicator, not a kernel thrashing detector.",
    }


def run_working_set_demo() -> dict[str, object]:
    reference = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
    return {
        "concept": "The working-set model estimates a process active locality using a recent reference window.",
        "reference_string": reference,
        **analyze_working_set(reference, window_size=5, frame_count=3),
    }


def run_thrashing_demo() -> dict[str, object]:
    result = run_working_set_demo()
    result["concept"] = "Thrashing risk rises when a process active working set cannot fit in its allocated frames; the OS can respond by reducing multiprogramming or allocating more frames when available."
    return result