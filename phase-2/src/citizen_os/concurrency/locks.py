"""Software mutual-exclusion algorithms for bounded teaching demonstrations.

These algorithms are implemented at user level for study. Python's runtime and
operating-system scheduling mean they are not substitutes for production locks.
"""
from __future__ import annotations
import threading
import time
from contextlib import contextmanager
from typing import Iterator


class PetersonLock:
    """Peterson's two-process mutual-exclusion algorithm."""
    def __init__(self) -> None:
        self._flag = [False, False]
        self._turn = 0
        self._meta = threading.Lock()

    @contextmanager
    def hold(self, participant: int) -> Iterator[None]:
        if participant not in (0, 1):
            raise ValueError("PetersonLock supports participant 0 or 1")
        other = 1 - participant
        with self._meta:
            self._flag[participant] = True
            self._turn = other
        while True:
            with self._meta:
                should_wait = self._flag[other] and self._turn == other
            if not should_wait:
                break
            time.sleep(0)
        try:
            yield
        finally:
            with self._meta:
                self._flag[participant] = False


class StrictAlternationLock:
    """Strict alternation for exactly two participants; can limit progress."""
    def __init__(self) -> None:
        self._turn = 0
        self._condition = threading.Condition()

    @contextmanager
    def hold(self, participant: int) -> Iterator[None]:
        if participant not in (0, 1):
            raise ValueError("StrictAlternationLock supports participant 0 or 1")
        with self._condition:
            while self._turn != participant:
                self._condition.wait()
        try:
            yield
        finally:
            with self._condition:
                self._turn = 1 - participant
                self._condition.notify_all()


class BakeryLock:
    """Lamport's Bakery algorithm for a fixed number of participants."""
    def __init__(self, participants: int) -> None:
        if participants < 1:
            raise ValueError("participants must be >= 1")
        self._choosing = [False] * participants
        self._number = [0] * participants
        self._meta = threading.Lock()
        self.participants = participants

    @contextmanager
    def hold(self, participant: int) -> Iterator[None]:
        if not 0 <= participant < self.participants:
            raise ValueError("participant index out of range")
        with self._meta:
            self._choosing[participant] = True
            self._number[participant] = max(self._number) + 1
            ticket = self._number[participant]
            self._choosing[participant] = False

        for other in range(self.participants):
            if other == participant:
                continue
            while True:
                with self._meta:
                    choosing = self._choosing[other]
                if not choosing:
                    break
                time.sleep(0)
            while True:
                with self._meta:
                    other_ticket = self._number[other]
                if other_ticket == 0 or (ticket, participant) < (other_ticket, other):
                    break
                time.sleep(0)
        try:
            yield
        finally:
            with self._meta:
                self._number[participant] = 0


class TestAndSetLock:
    """Spin lock using Python's atomic non-blocking Lock.acquire operation."""
    def __init__(self) -> None:
        self._flag = threading.Lock()

    @contextmanager
    def hold(self) -> Iterator[None]:
        while not self._flag.acquire(blocking=False):
            time.sleep(0)
        try:
            yield
        finally:
            self._flag.release()


def run_lock_demo(algorithm: str, participants: int = 2, increments_per_participant: int = 500) -> dict[str, int | str]:
    """Run a shared-counter demonstration using one of the syllabus lock algorithms."""
    factories = {
        "peterson": lambda: PetersonLock(),
        "strict-alternation": lambda: StrictAlternationLock(),
        "bakery": lambda: BakeryLock(participants),
        "test-and-set": lambda: TestAndSetLock(),
    }
    if algorithm not in factories:
        raise ValueError(f"unknown algorithm: {algorithm}")
    if participants < 2 and algorithm in {"peterson", "strict-alternation"}:
        raise ValueError(f"{algorithm} requires exactly two participants")
    if algorithm in {"peterson", "strict-alternation"} and participants != 2:
        raise ValueError(f"{algorithm} requires exactly two participants")
    if participants < 1 or increments_per_participant < 0:
        raise ValueError("participants must be >= 1 and increments_per_participant >= 0")

    lock = factories[algorithm]()
    counter = 0

    def worker(pid: int) -> None:
        nonlocal counter
        for _ in range(increments_per_participant):
            context = lock.hold(pid) if algorithm in {"peterson", "strict-alternation", "bakery"} else lock.hold()
            with context:
                counter += 1

    threads = [threading.Thread(target=worker, args=(i,), name=f"{algorithm}-worker-{i}") for i in range(participants)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    expected = participants * increments_per_participant
    return {"algorithm": algorithm, "participants": participants,
            "increments_per_participant": increments_per_participant,
            "expected_total": expected, "actual_total": counter}
