"""Bounded-buffer producer-consumer and process IPC teaching demonstrations."""
from __future__ import annotations

from collections import deque
import multiprocessing
import threading
from typing import Any


def run_producer_consumer(items: int = 20, capacity: int = 5) -> dict[str, int | bool]:
    """Pass numbered items through a bounded buffer shared by two threads."""
    if items < 0:
        raise ValueError("items must be >= 0")
    if capacity < 1:
        raise ValueError("capacity must be >= 1")

    buffer: deque[int | None] = deque()
    condition = threading.Condition()
    consumed: list[int] = []

    def producer() -> None:
        for item in range(1, items + 1):
            with condition:
                while len(buffer) >= capacity:
                    condition.wait()
                buffer.append(item)
                condition.notify_all()
        with condition:
            while len(buffer) >= capacity:
                condition.wait()
            buffer.append(None)  # sentinel: producer has finished
            condition.notify_all()

    def consumer() -> None:
        while True:
            with condition:
                while not buffer:
                    condition.wait()
                item = buffer.popleft()
                condition.notify_all()
            if item is None:
                break
            consumed.append(item)

    producer_thread = threading.Thread(target=producer, name="bounded-buffer-producer")
    consumer_thread = threading.Thread(target=consumer, name="bounded-buffer-consumer")
    producer_thread.start()
    consumer_thread.start()
    producer_thread.join()
    consumer_thread.join()

    expected_sum = items * (items + 1) // 2
    return {
        "items_requested": items,
        "items_consumed": len(consumed),
        "buffer_capacity": capacity,
        "expected_sum": expected_sum,
        "consumed_sum": sum(consumed),
        "buffer_empty": not buffer,
    }


def _ipc_child(connection: Any) -> None:
    """Child-process endpoint: receive one string and send a response."""
    try:
        message = connection.recv()
        connection.send({"received": message, "response": message.upper()})
    finally:
        connection.close()


def run_pipe_ipc(message: str = "hello from parent") -> dict[str, str]:
    """Exchange one message between parent and child using a multiprocessing Pipe."""
    if not isinstance(message, str) or not message:
        raise ValueError("message must be a non-empty string")

    parent_connection, child_connection = multiprocessing.Pipe(duplex=True)
    child = multiprocessing.Process(target=_ipc_child, args=(child_connection,), name="ipc-child")
    child.start()
    child_connection.close()
    try:
        parent_connection.send(message)
        response = parent_connection.recv()
    finally:
        parent_connection.close()
        child.join(timeout=5)
        if child.is_alive():
            child.terminate()
            child.join()
    if child.exitcode != 0:
        raise RuntimeError(f"IPC child process exited with code {child.exitcode}")
    return {"sent": message, "received": response["received"], "response": response["response"]}
