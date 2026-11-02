"""CPU scheduling simulations for citizen-service application processes."""
from collections import deque
from dataclasses import dataclass
from copy import deepcopy
from .models import ProcessState, ServiceProcess

@dataclass(frozen=True)
class ScheduleResult:
    algorithm: str
    timeline: list[tuple[int,int,int]]
    processes: list[ServiceProcess]
    @property
    def average_waiting_time(self):
        return sum(p.waiting_time for p in self.processes)/len(self.processes) if self.processes else 0.0
    @property
    def average_turnaround_time(self):
        return sum(p.turnaround_time for p in self.processes)/len(self.processes) if self.processes else 0.0

def _prepare(items):
    if not items: raise ValueError("At least one process is required")
    ps=[deepcopy(p) for p in items]
    if len({p.pid for p in ps}) != len(ps): raise ValueError("Process IDs must be unique")
    return ps

def _finish(ps,timeline,name):
    for p in ps:
        if p.completion_time is None: raise RuntimeError(f"Process {p.pid} was not completed")
        p.turnaround_time=p.completion_time-p.arrival_time
        p.waiting_time=p.turnaround_time-p.burst_time
        p.state=ProcessState.TERMINATED
    return ScheduleResult(name,timeline,sorted(ps,key=lambda p:p.pid))

def fcfs(items):
    ps=_prepare(items); t=0; tl=[]
    for p in sorted(ps,key=lambda x:(x.arrival_time,x.pid)):
        t=max(t,p.arrival_time); p.state=ProcessState.RUNNING; p.start_time=t; p.response_time=t-p.arrival_time
        tl.append((p.pid,t,t+p.burst_time)); t+=p.burst_time; p.completion_time=t
    return _finish(ps,tl,"FCFS")

def sjf(items):
    ps=_prepare(items); t=0; done=set(); tl=[]
    while len(done)<len(ps):
        ready=[p for p in ps if p.pid not in done and p.arrival_time<=t]
        if not ready: t=min(p.arrival_time for p in ps if p.pid not in done); continue
        p=min(ready,key=lambda x:(x.burst_time,x.arrival_time,x.pid)); p.state=ProcessState.RUNNING; p.start_time=t; p.response_time=t-p.arrival_time
        tl.append((p.pid,t,t+p.burst_time)); t+=p.burst_time; p.completion_time=t; done.add(p.pid)
    return _finish(ps,tl,"SJF (non-preemptive)")

def priority(items):
    ps=_prepare(items); t=0; done=set(); tl=[]
    while len(done)<len(ps):
        ready=[p for p in ps if p.pid not in done and p.arrival_time<=t]
        if not ready: t=min(p.arrival_time for p in ps if p.pid not in done); continue
        p=min(ready,key=lambda x:(x.priority,x.arrival_time,x.pid)); p.state=ProcessState.RUNNING; p.start_time=t; p.response_time=t-p.arrival_time
        tl.append((p.pid,t,t+p.burst_time)); t+=p.burst_time; p.completion_time=t; done.add(p.pid)
    return _finish(ps,tl,"Priority (non-preemptive)")

def round_robin(items,quantum=2):
    if quantum<1: raise ValueError("quantum must be at least 1")
    ps=_prepare(items); pending=sorted(ps,key=lambda p:(p.arrival_time,p.pid)); q=deque(); t=0; i=0; tl=[]
    while i<len(pending) or q:
        if not q and i<len(pending) and t<pending[i].arrival_time: t=pending[i].arrival_time
        while i<len(pending) and pending[i].arrival_time<=t: pending[i].state=ProcessState.READY; q.append(pending[i]); i+=1
        p=q.popleft(); p.state=ProcessState.RUNNING
        if p.start_time is None: p.start_time=t; p.response_time=t-p.arrival_time
        start=t; t+=min(quantum,p.remaining_time); p.remaining_time-=t-start; tl.append((p.pid,start,t))
        while i<len(pending) and pending[i].arrival_time<=t: pending[i].state=ProcessState.READY; q.append(pending[i]); i+=1
        if p.remaining_time: p.state=ProcessState.READY; q.append(p)
        else: p.completion_time=t
    return _finish(ps,tl,f"Round Robin (q={quantum})")

def srtf(items):
    ps=_prepare(items); t=min(p.arrival_time for p in ps); tl=[]; done=set()
    while len(done)<len(ps):
        ready=[p for p in ps if p.pid not in done and p.arrival_time<=t and p.remaining_time>0]
        if not ready: t=min(p.arrival_time for p in ps if p.pid not in done and p.arrival_time>t); continue
        p=min(ready,key=lambda x:(x.remaining_time,x.arrival_time,x.pid))
        if p.start_time is None: p.start_time=t; p.response_time=t-p.arrival_time
        p.state=ProcessState.RUNNING; start=t; t+=1; p.remaining_time-=1
        if tl and tl[-1][0]==p.pid and tl[-1][2]==start: tl[-1]=(p.pid,tl[-1][1],t)
        else: tl.append((p.pid,start,t))
        if p.remaining_time==0: p.completion_time=t; done.add(p.pid)
    return _finish(ps,tl,"SRTF")

def multilevel_queue(items, quantum=2):
    """Fixed queues: lower numeric priority is higher; RR within each queue.

    A newly ready process in a higher-priority queue preempts a lower queue.
    Queue membership never changes. All queues use the same RR quantum.
    """
    if quantum<1: raise ValueError("quantum must be at least 1")
    ps=_prepare(items); levels=sorted({p.priority for p in ps})
    queues={level:deque() for level in levels}
    pending=sorted(ps,key=lambda p:(p.arrival_time,p.pid)); i=0; t=0; timeline=[]
    while i<len(pending) or any(queues[level] for level in levels):
        while i<len(pending) and pending[i].arrival_time<=t:
            p=pending[i]; p.state=ProcessState.READY; queues[p.priority].append(p); i+=1
        ready_levels=[level for level in levels if queues[level]]
        if not ready_levels:
            t=pending[i].arrival_time
            continue
        level=ready_levels[0]; p=queues[level].popleft(); p.state=ProcessState.RUNNING
        if p.start_time is None: p.start_time=t; p.response_time=t-p.arrival_time
        start=t; used=0
        while used<quantum and p.remaining_time>0:
            t+=1; used+=1; p.remaining_time-=1
            while i<len(pending) and pending[i].arrival_time<=t:
                new=pending[i]; new.state=ProcessState.READY; queues[new.priority].append(new); i+=1
            if any(queues[higher] for higher in levels if higher<level):
                break
        timeline.append((p.pid,start,t))
        if p.remaining_time==0: p.completion_time=t
        else: p.state=ProcessState.READY; queues[level].append(p)
    return _finish(ps,timeline,f"Multilevel Queue (RR q={quantum})")

def multilevel_feedback_queue(items, quantums=(2,4,8)):
    """Dynamic MLFQ: new jobs enter top queue and are demoted on full slices.

    Higher queues preempt lower queues. A preempted job keeps its unused
    quantum when it is next dispatched. The lowest queue uses round robin.
    No priority boost/aging is applied in this basic teaching implementation.
    """
    if not quantums or any(q<1 for q in quantums):
        raise ValueError("quantums must contain positive integers")
    ps=_prepare(items); queues=[deque() for _ in quantums]
    pending=sorted(ps,key=lambda p:(p.arrival_time,p.pid)); i=0; t=0; timeline=[]
    level_of={p.pid:0 for p in ps}; slice_left={p.pid:quantums[0] for p in ps}
    while i<len(pending) or any(queues):
        while i<len(pending) and pending[i].arrival_time<=t:
            p=pending[i]; p.state=ProcessState.READY; queues[0].append(p); i+=1
        active=next((level for level,q in enumerate(queues) if q),None)
        if active is None:
            t=pending[i].arrival_time
            continue
        p=queues[active].popleft(); p.state=ProcessState.RUNNING
        if p.start_time is None: p.start_time=t; p.response_time=t-p.arrival_time
        start=t; preempted=False
        while slice_left[p.pid]>0 and p.remaining_time>0:
            t+=1; p.remaining_time-=1; slice_left[p.pid]-=1
            while i<len(pending) and pending[i].arrival_time<=t:
                new=pending[i]; new.state=ProcessState.READY; queues[0].append(new); i+=1
            if active>0 and queues[0]:
                preempted=True
                break
            if any(queues[higher] for higher in range(active)):
                preempted=True
                break
        timeline.append((p.pid,start,t))
        if p.remaining_time==0:
            p.completion_time=t
        elif preempted:
            p.state=ProcessState.READY; queues[active].appendleft(p)
        elif slice_left[p.pid]==0:
            next_level=min(active+1,len(quantums)-1)
            level_of[p.pid]=next_level; slice_left[p.pid]=quantums[next_level]
            p.state=ProcessState.READY; queues[next_level].append(p)
    return _finish(ps,timeline,"Multilevel Feedback Queue")
