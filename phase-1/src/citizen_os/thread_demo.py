"""Threading demonstration with shared state protected by a lock."""
from __future__ import annotations
import threading

def run_thread_demo(workers: int = 4, increments_per_worker: int = 1000) -> dict[str, int]:
    """Run concurrent service counters and protect updates with a mutex."""
    if workers < 1 or increments_per_worker < 0:
        raise ValueError("workers must be >= 1 and increments_per_worker >= 0")
    counter = 0
    lock = threading.Lock()

    def update_counter() -> None:
        nonlocal counter
        for _ in range(increments_per_worker):
            with lock:
                counter += 1

    threads = [
        threading.Thread(target=update_counter, name=f"service-worker-{i + 1}")
        for i in range(workers)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return {
        "workers": workers,
        "increments_per_worker": increments_per_worker,
        "expected_total": workers * increments_per_worker,
        "actual_total": counter,
    }
