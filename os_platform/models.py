"""Data model for a simulated citizen-service request."""

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class RequestState(str, Enum):
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    TERMINATED = "TERMINATED"


@dataclass
class ServiceRequest:
    """A service request represented as a process with PCB-like metadata.

    request_id acts as the simulated process identifier (PID). Timing fields
    are populated by the scheduler and persisted by the JSON storage layer.
    """

    request_id: str
    service_type: str
    applicant_label: str
    burst_time: int
    state: RequestState = RequestState.NEW
    start_time: int | None = None
    finish_time: int | None = None
    arrival_time: int = 0
    waiting_time: int | None = None
    turnaround_time: int | None = None

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id must not be empty")
        if not self.service_type.strip():
            raise ValueError("service_type must not be empty")
        if self.burst_time <= 0:
            raise ValueError("burst_time must be a positive integer")
        if self.arrival_time < 0:
            raise ValueError("arrival_time must be zero or positive")
        if not isinstance(self.state, RequestState):
            self.state = RequestState(self.state)

    def to_dict(self) -> dict[str, Any]:
        record = asdict(self)
        record["state"] = self.state.value
        return record

    @classmethod
    def from_dict(cls, record: dict[str, Any]) -> "ServiceRequest":
        values = dict(record)
        values["state"] = RequestState(values.get("state", RequestState.NEW.value))
        return cls(**values)
