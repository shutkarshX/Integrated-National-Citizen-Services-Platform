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
    def average_waiting_time(self): return sum(p.waiting_time for p in self.processes)/len(self.processes) if self.processes else 0.0
    @property
    def average_turnaround_time(self): return sum(p.turnaround_time for p in self.processes)/len(self.processes) if self.processes else 0.0

def _prepare(items):
    if not items: raise ValueError("At least one process is required")
    return [deepcopy(p) for p in items]
def _finish(ps,timeline,name):
    for p in ps:
        if p.completion_time is None: raise RuntimeError(f"Process {p.pid} was not completed")
        p.turnaround_time=p.completion_time-p.arrival_time; p.waiting_time=p.turnaround_time-p.burst_time; p.state=ProcessState.TERMINATED
    return ScheduleResult(name,timeline,sorted(ps,key=lambda p:p.pid))
def fcfs(items):
    ps=_prepare(items); t=0; tl=[]
    for p in sorted(ps,key=lambda x:(x.arrival_time,x.pid)):
        t=max(t,p.arrival_time); p.state=ProcessState.RUNNING; p.start_time=t; p.response_time=t-p.arrival_time; tl.append((p.pid,t,t+p.burst_time)); t+=p.burst_time; p.completion_time=t
    return _finish(ps,tl,"FCFS")
def sjf(items):
    ps=_prepare(items); t=0; done=set(); tl=[]
    while len(done)<len(ps):
        ready=[p for p in ps if p.pid not in done and p.arrival_time<=t]
        if not ready: t=min(p.arrival_time for p in ps if p.pid not in done); continue
        p=min(ready,key=lambda x:(x.burst_time,x.arrival_time,x.pid)); p.state=ProcessState.RUNNING; p.start_time=t; p.response_time=t-p.arrival_time; tl.append((p.pid,t,t+p.burst_time)); t+=p.burst_time; p.completion_time=t; done.add(p.pid)
    return _finish(ps,tl,"SJF (non-preemptive)")
def priority(items):
    ps=_prepare(items); t=0; done=set(); tl=[]
    while len(done)<len(ps):
        ready=[p for p in ps if p.pid not in done and p.arrival_time<=t]
        if not ready: t=min(p.arrival_time for p in ps if p.pid not in done); continue
        p=min(ready,key=lambda x:(x.priority,x.arrival_time,x.pid)); p.state=ProcessState.RUNNING; p.start_time=t; p.response_time=t-p.arrival_time; tl.append((p.pid,t,t+p.burst_time)); t+=p.burst_time; p.completion_time=t; done.add(p.pid)
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
