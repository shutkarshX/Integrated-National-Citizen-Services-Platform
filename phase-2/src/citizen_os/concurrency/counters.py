"""Deterministic race-condition and mutex-protected counter demonstrations."""
from __future__ import annotations
import threading


def run_race_demo(increments_per_worker: int = 100) -> dict[str, int]:
    """Force a lost-update race between two threads using a two-phase barrier.

    Both workers read the same shared value before either writes it. This makes
    the lost update reproducible instead of relying on scheduler luck.
    """
    if increments_per_worker < 1:
        raise ValueError("increments_per_worker must be >= 1")

    counter = 0
    rendezvous = threading.Barrier(2)

    def worker() -> None:
        nonlocal counter
        for _ in range(increments_per_worker):
            observed = counter
            rendezvous.wait()
            counter = observed + 1
            rendezvous.wait()

    threads = [threading.Thread(target=worker, name=f"racy-worker-{i}") for i in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return {
        "workers": 2,
        "increments_per_worker": increments_per_worker,
        "expected_total": 2 * increments_per_worker,
        "actual_total": counter,
        "lost_updates": 2 * increments_per_worker - counter,
    }


def run_locked_counter(workers: int = 4, increments_per_worker: int = 1000) -> dict[str, int]:
    """Increment shared state under a mutex and report the verified total."""
    if workers < 1 or increments_per_worker < 0:
        raise ValueError("workers must be >= 1 and increments_per_worker >= 0")

    counter = 0
    lock = threading.Lock()

    def worker() -> None:
        nonlocal counter
        for _ in range(increments_per_worker):
            with lock:
                counter += 1

    threads = [threading.Thread(target=worker, name=f"locked-worker-{i}") for i in range(workers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    expected = workers * increments_per_worker
    return {"workers": workers, "increments_per_worker": increments_per_worker,
            "expected_total": expected, "actual_total": counter}
