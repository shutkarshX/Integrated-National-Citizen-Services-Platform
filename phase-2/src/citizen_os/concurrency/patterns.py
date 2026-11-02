"""Semaphore, monitor and classical synchronization problem demonstrations."""
from __future__ import annotations

import threading
import time
from collections import deque
from typing import Any


def run_semaphore_demo(workers: int = 6, permits: int = 2, iterations: int = 20) -> dict[str, int]:
    """Measure concurrency admitted by a counting semaphore (permits=1 is binary)."""
    if workers < 1 or permits < 1 or iterations < 0 or permits > workers:
        raise ValueError("require workers >= permits >= 1 and iterations >= 0")
    semaphore = threading.Semaphore(permits)
    guard = threading.Lock()
    active = maximum = completed = 0

    def worker() -> None:
        nonlocal active, maximum, completed
        for _ in range(iterations):
            semaphore.acquire()
            try:
                with guard:
                    active += 1
                    maximum = max(maximum, active)
                time.sleep(0)
                with guard:
                    active -= 1
                    completed += 1
            finally:
                semaphore.release()

    threads = [threading.Thread(target=worker) for _ in range(workers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return {"workers": workers, "permits": permits, "operations_expected": workers * iterations,
            "operations_completed": completed, "maximum_concurrent": maximum}


class ReadersWritersMonitor:
    """Writer-preference monitor: active writer excludes everyone; waiting writers block new readers."""
    def __init__(self) -> None:
        self._condition = threading.Condition()
        self._active_readers = 0
        self._waiting_writers = 0
        self._writer_active = False

    def begin_read(self) -> None:
        with self._condition:
            while self._writer_active or self._waiting_writers:
                self._condition.wait()
            self._active_readers += 1

    def end_read(self) -> None:
        with self._condition:
            self._active_readers -= 1
            if self._active_readers == 0:
                self._condition.notify_all()

    def begin_write(self) -> None:
        with self._condition:
            self._waiting_writers += 1
            try:
                while self._writer_active or self._active_readers:
                    self._condition.wait()
                self._writer_active = True
            finally:
                self._waiting_writers -= 1

    def end_write(self) -> None:
        with self._condition:
            self._writer_active = False
            self._condition.notify_all()


def run_readers_writers(readers: int = 4, writers: int = 2, iterations: int = 10) -> dict[str, int]:
    """Exercise a writer-preference monitor and report operation counts / overlap."""
    if readers < 1 or writers < 1 or iterations < 0:
        raise ValueError("readers and writers must be >= 1; iterations must be >= 0")
    monitor = ReadersWritersMonitor()
    state = threading.Lock()
    active_readers = active_writers = max_readers = violations = reads = writes = 0

    def reader() -> None:
        nonlocal active_readers, max_readers, active_writers, violations, reads
        for _ in range(iterations):
            monitor.begin_read()
            with state:
                active_readers += 1
                max_readers = max(max_readers, active_readers)
                if active_writers:
                    violations += 1
            time.sleep(0)
            with state:
                active_readers -= 1
                reads += 1
            monitor.end_read()

    def writer() -> None:
        nonlocal active_readers, active_writers, violations, writes
        for _ in range(iterations):
            monitor.begin_write()
            with state:
                active_writers += 1
                if active_writers > 1 or active_readers:
                    violations += 1
            time.sleep(0)
            with state:
                active_writers -= 1
                writes += 1
            monitor.end_write()

    threads = [threading.Thread(target=reader) for _ in range(readers)]
    threads += [threading.Thread(target=writer) for _ in range(writers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return {"reads_completed": reads, "writes_completed": writes, "maximum_simultaneous_readers": max_readers,
            "synchronization_violations": violations}


def run_dining_philosophers(philosophers: int = 5, meals: int = 3) -> dict[str, int]:
    """Avoid circular wait by allowing at most N-1 philosophers to compete for forks."""
    if philosophers < 2 or meals < 0:
        raise ValueError("philosophers must be >= 2 and meals must be >= 0")
    forks = [threading.Lock() for _ in range(philosophers)]
    room = threading.Semaphore(philosophers - 1)
    completed = [0] * philosophers

    def dine(index: int) -> None:
        left, right = forks[index], forks[(index + 1) % philosophers]
        for _ in range(meals):
            with room:
                with left:
                    with right:
                        completed[index] += 1
                        time.sleep(0)

    threads = [threading.Thread(target=dine, args=(i,)) for i in range(philosophers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return {"philosophers": philosophers, "meals_each": meals,
            "meals_expected": philosophers * meals, "meals_completed": sum(completed)}


def run_sleeping_barber(customers: int = 10, waiting_chairs: int = 3) -> dict[str, int]:
    """Simulate a barber shop with a finite waiting room and customer completion events."""
    if customers < 0 or waiting_chairs < 0:
        raise ValueError("customers and waiting_chairs must be >= 0")
    condition = threading.Condition()
    waiting: deque[tuple[int, threading.Event]] = deque()
    finished = 0
    served = turned_away = 0
    start = threading.Barrier(customers) if customers > 0 else None

    def customer(customer_id: int) -> None:
        nonlocal finished, turned_away
        done = threading.Event()
        assert start is not None
        start.wait()
        with condition:
            if len(waiting) >= waiting_chairs:
                turned_away += 1
                finished += 1
                condition.notify_all()
                return
            waiting.append((customer_id, done))
            condition.notify_all()
        done.wait(timeout=5)

    def barber() -> None:
        nonlocal finished, served
        while True:
            with condition:
                while not waiting and finished < customers:
                    condition.wait()
                if finished >= customers and not waiting:
                    return
                _, done = waiting.popleft()
            time.sleep(0)
            done.set()
            with condition:
                served += 1
                finished += 1
                condition.notify_all()

    barber_thread = threading.Thread(target=barber, name="barber")
    barber_thread.start()
    threads = [threading.Thread(target=customer, args=(i,)) for i in range(customers)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    with condition:
        condition.notify_all()
    barber_thread.join(timeout=5)
    if barber_thread.is_alive():
        raise RuntimeError("barber simulation did not terminate")
    return {"customers": customers, "waiting_chairs": waiting_chairs,
            "served": served, "turned_away": turned_away, "accounted_for": served + turned_away}
