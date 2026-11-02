#!/usr/bin/env python3
import argparse
from citizen_os.linux_info import collect_system_info
from citizen_os.scheduler import fcfs,sjf,srtf,priority,round_robin
from citizen_os.service_desk import sample_requests
from citizen_os.process_demo import run_process_demo
from citizen_os.thread_demo import run_thread_demo

def main():
    parser=argparse.ArgumentParser(description="Linux-first citizen services OS learning platform")
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("system",help="inspect the actual Linux host")
    sub.add_parser("process-demo",help="launch and monitor real child processes")
    sub.add_parser("thread-demo",help="run concurrent service workers with a lock")
    sch=sub.add_parser("schedule",help="simulate CPU scheduling")
    sch.add_argument("--algorithm",choices=["fcfs","sjf","srtf","priority","rr"],default="fcfs")
    sch.add_argument("--quantum",type=int,default=2)
    args=parser.parse_args()
    if args.command=="system":
        for k,v in collect_system_info().items(): print(f"\\n[{k.upper()}]\\n{v}")
        return
    if args.command=="process-demo":
        print("Real child-process demonstration (user-space subprocesses)")
        for item in run_process_demo():
            print(f"\\n{item['name']}: PID={item['pid']} exit={item['return_code']} duration={item['duration_ms']}ms")
            print(item["output"])
        return
    if args.command=="thread-demo":
        result=run_thread_demo()
        print("Concurrent citizen-service workers (shared counter protected by threading.Lock)")
        for key,value in result.items(): print(f"{key}: {value}")
        return
    jobs=sample_requests()
    funcs={"fcfs":fcfs,"sjf":sjf,"srtf":srtf,"priority":priority}
    result=round_robin(jobs,args.quantum) if args.algorithm=="rr" else funcs[args.algorithm](jobs)
    print(f"\\nAlgorithm: {result.algorithm}\\nPID | Citizen | Service | Arrival | Burst | Completion | Waiting | Turnaround")
    for p in result.processes: print(f"{p.pid} | {p.citizen_name} | {p.service_name} | {p.arrival_time} | {p.burst_time} | {p.completion_time} | {p.waiting_time} | {p.turnaround_time}")
    print("\\nTimeline: "+" -> ".join(f"P{pid}[{start}-{end}]" for pid,start,end in result.timeline))
    print(f"Average waiting time: {result.average_waiting_time:.2f}")
    print(f"Average turnaround time: {result.average_turnaround_time:.2f}")

if __name__=="__main__":
    main()
