"""Application-level process and PCB model (not a kernel PCB)."""
from dataclasses import dataclass, field
from enum import Enum

class ProcessState(str, Enum):
    NEW="NEW"; READY="READY"; RUNNING="RUNNING"; WAITING="WAITING"; TERMINATED="TERMINATED"

@dataclass
class ServiceProcess:
    pid: int
    citizen_name: str
    service_name: str
    burst_time: int
    arrival_time: int = 0
    priority: int = 1
    state: ProcessState = ProcessState.NEW
    remaining_time: int = field(init=False)
    start_time: int | None = None
    completion_time: int | None = None
    waiting_time: int = 0
    turnaround_time: int = 0
    response_time: int | None = None
    def __post_init__(self):
        if self.pid < 1: raise ValueError("pid must be positive")
        if self.burst_time < 1: raise ValueError("burst_time must be at least 1")
        if self.arrival_time < 0: raise ValueError("arrival_time cannot be negative")
        if self.priority < 1: raise ValueError("priority must be at least 1")
        self.remaining_time=self.burst_time
    def pcb_snapshot(self):
        return {"pid":self.pid,"citizen":self.citizen_name,"service":self.service_name,"state":self.state.value,"arrival_time":self.arrival_time,"burst_time":self.burst_time,"remaining_time":self.remaining_time,"priority":self.priority}
