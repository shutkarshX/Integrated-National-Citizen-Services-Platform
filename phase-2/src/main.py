#!/usr/bin/env python3
"""Command-line entry point for Phase 2 OS demonstrations."""
import argparse
from citizen_os.concurrency.counters import run_locked_counter, run_race_demo
from citizen_os.concurrency.locks import run_lock_demo
from citizen_os.concurrency.synchronization import run_pipe_ipc, run_producer_consumer
from citizen_os.memory_allocation import run_fixed_partition_demo, run_variable_partition_demo
from citizen_os.address_translation import run_paging_demo, run_segmentation_demo, run_segmented_paging_demo
from citizen_os.page_replacement import run_demand_paging_demo, run_page_replacement_comparison, run_belady_anomaly_demo
from citizen_os.working_set import run_working_set_demo, run_thrashing_demo
from citizen_os.loading_linking import run_loading_linking_demo
from citizen_os.file_disk import run_file_management_demo, run_disk_scheduling_demo
from citizen_os.virtualization_cuda import run_virtualization_demo, run_cuda_demo
from citizen_os.deadlock import (
    database_transaction_deadlock_case_study, deadlock_conditions_and_prevention, detect_deadlock, recover_by_terminating_victim,
    resource_allocation_graph_demo, run_bankers_demo,
)
from citizen_os.concurrency.patterns import (
    run_dining_philosophers, run_readers_writers, run_semaphore_demo, run_sleeping_barber,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 2: concurrency, synchronization and IPC demos")
    sub = parser.add_subparsers(dest="command", required=True)

    race = sub.add_parser("race-demo", help="reproduce a shared-counter race condition")
    race.add_argument("--iterations", type=int, default=100)
    locked = sub.add_parser("locked-demo", help="run a mutex-protected shared counter")
    locked.add_argument("--workers", type=int, default=4)
    locked.add_argument("--iterations", type=int, default=1000)
    lock = sub.add_parser("lock-demo", help="run a mutual-exclusion algorithm")
    lock.add_argument("--algorithm", choices=["peterson", "strict-alternation", "bakery", "test-and-set"], default="peterson")
    lock.add_argument("--workers", type=int, default=2)
    lock.add_argument("--iterations", type=int, default=500)
    pc = sub.add_parser("producer-consumer", help="run a bounded-buffer producer-consumer demo")
    pc.add_argument("--items", type=int, default=20)
    pc.add_argument("--capacity", type=int, default=5)
    ipc = sub.add_parser("ipc-demo", help="exchange a message between parent and child processes using a Pipe")
    ipc.add_argument("--message", default="hello from parent")
    sem = sub.add_parser("semaphore-demo", help="demonstrate binary or counting semaphore capacity")
    sem.add_argument("--workers", type=int, default=6)
    sem.add_argument("--permits", type=int, default=2)
    sem.add_argument("--iterations", type=int, default=20)
    rw = sub.add_parser("readers-writers", help="run the writer-preference readers-writers monitor")
    rw.add_argument("--readers", type=int, default=4)
    rw.add_argument("--writers", type=int, default=2)
    rw.add_argument("--iterations", type=int, default=10)
    dp = sub.add_parser("dining-philosophers", help="run deadlock-avoiding dining philosophers")
    dp.add_argument("--philosophers", type=int, default=5)
    dp.add_argument("--meals", type=int, default=3)
    barber = sub.add_parser("sleeping-barber", help="simulate a barber and finite waiting room")
    barber.add_argument("--customers", type=int, default=10)
    barber.add_argument("--chairs", type=int, default=3)
    sub.add_parser("rag-demo", help="show a single-instance resource-allocation graph cycle")
    sub.add_parser("banker-demo", help="run the classic Banker's safety example")
    sub.add_parser("deadlock-detection", help="run a multi-instance deadlock detection example")
    sub.add_parser("deadlock-prevention", help="list Coffman conditions and prevention strategies")
    sub.add_parser("deadlock-recovery", help="demonstrate victim selection and resource release")
    sub.add_parser("database-deadlock", help="show a two-transaction database lock cycle")
    sub.add_parser("fixed-partitions", help="compare first, best and worst fit for fixed partitions")
    variable = sub.add_parser("variable-partitions", help="run variable-partition allocation with a fit strategy")
    variable.add_argument("--strategy", choices=["first-fit", "best-fit", "worst-fit"], default="first-fit")
    sub.add_parser("paging-demo", help="translate a logical address using a page table")
    sub.add_parser("segmentation-demo", help="translate a segment:offset address using base and limit")
    sub.add_parser("segmented-paging-demo", help="translate an address using segmentation followed by paging")
    sub.add_parser("demand-paging-demo", help="demonstrate demand loading and page faults")
    sub.add_parser("page-replacement-demo", help="compare FIFO, LRU, Optimal and LFU page replacement")
    sub.add_parser("belady-anomaly-demo", help="demonstrate Belady anomaly with FIFO")
    sub.add_parser("working-set-demo", help="show trailing working sets and frame pressure")
    sub.add_parser("thrashing-demo", help="demonstrate thrashing risk using the working-set model")
    sub.add_parser("loading-linking-demo", help="demonstrate symbol linking, module loading and address binding")
    sub.add_parser("file-management-demo", help="demonstrate file access and allocation methods")
    sub.add_parser("disk-scheduling-demo", help="compare FCFS, SSTF, SCAN, C-SCAN, LOOK and C-LOOK")
    sub.add_parser("virtualization-demo", help="demonstrate VM resource configuration and hypervisor types")
    sub.add_parser("cuda-demo", help="simulate CUDA grid, block and thread indexing with vector addition")

    args = parser.parse_args()
    if args.command == "race-demo":
        result = run_race_demo(args.iterations)
        label = "Race condition demonstration"
    elif args.command == "locked-demo":
        result = run_locked_counter(args.workers, args.iterations)
        label = "Mutex-protected counter demonstration"
    elif args.command == "lock-demo":
        result = run_lock_demo(args.algorithm, args.workers, args.iterations)
        label = f"Mutual exclusion demonstration: {args.algorithm}"
    elif args.command == "producer-consumer":
        result = run_producer_consumer(args.items, args.capacity)
        label = "Bounded-buffer Producer–Consumer demonstration"
    elif args.command == "ipc-demo":
        result = run_pipe_ipc(args.message)
        label = "Parent-child IPC demonstration using multiprocessing.Pipe"
    elif args.command == "semaphore-demo":
        result = run_semaphore_demo(args.workers, args.permits, args.iterations)
        label = "Counting semaphore demonstration (use --permits 1 for binary semaphore)"
    elif args.command == "readers-writers":
        result = run_readers_writers(args.readers, args.writers, args.iterations)
        label = "Readers–Writers monitor demonstration (writer preference)"
    elif args.command == "dining-philosophers":
        result = run_dining_philosophers(args.philosophers, args.meals)
        label = "Dining Philosophers demonstration (N-1 room semaphore)"
    elif args.command == "rag-demo":
        result = resource_allocation_graph_demo()
        label = "Resource Allocation Graph cycle demonstration (single-instance resources)"
    elif args.command == "banker-demo":
        result = run_bankers_demo()
        label = "Banker's Algorithm safety demonstration"
    elif args.command == "deadlock-detection":
        result = detect_deadlock([0, 0], [[1, 0], [0, 1]], [[0, 1], [1, 0]])
        label = "Multi-instance deadlock detection demonstration"
    elif args.command == "deadlock-prevention":
        result = deadlock_conditions_and_prevention()
        label = "Coffman conditions and deadlock prevention strategies"
    elif args.command == "deadlock-recovery":
        result = recover_by_terminating_victim([[1, 0], [0, 3]], [0, 1])
        label = "Deadlock recovery demonstration (largest-allocation victim policy)"
    elif args.command == "database-deadlock":
        result = database_transaction_deadlock_case_study()
        label = "Database transaction deadlock case study (wait-for graph)"
    elif args.command == "fixed-partitions":
        result = run_fixed_partition_demo()
        label = "Fixed partition allocation comparison"
    elif args.command == "variable-partitions":
        result = run_variable_partition_demo(args.strategy)
        label = f"Variable partition allocation: {args.strategy}"
    elif args.command == "paging-demo":
        result = run_paging_demo()
        label = "Paging address translation demonstration"
    elif args.command == "segmentation-demo":
        result = run_segmentation_demo()
        label = "Segmentation address translation demonstration"
    elif args.command == "segmented-paging-demo":
        result = run_segmented_paging_demo()
        label = "Segmented paging address translation demonstration"
    elif args.command == "demand-paging-demo":
        result = run_demand_paging_demo()
        label = "Demand paging demonstration"
    elif args.command == "page-replacement-demo":
        result = run_page_replacement_comparison()
        label = "Page replacement algorithm comparison"
    elif args.command == "belady-anomaly-demo":
        result = run_belady_anomaly_demo()
        label = "Belady anomaly demonstration (FIFO)"
    elif args.command == "working-set-demo":
        result = run_working_set_demo()
        label = "Working-set model demonstration"
    elif args.command == "thrashing-demo":
        result = run_thrashing_demo()
        label = "Thrashing risk demonstration (working-set model)"
    elif args.command == "loading-linking-demo":
        result = run_loading_linking_demo()
        label = "Loading, linking and address-binding demonstration"
    elif args.command == "file-management-demo":
        result = run_file_management_demo()
        label = "File access and allocation demonstration"
    elif args.command == "disk-scheduling-demo":
        result = run_disk_scheduling_demo()
        label = "Disk scheduling algorithm comparison"
    elif args.command == "virtualization-demo":
        result = run_virtualization_demo()
        label = "Virtual machine and hypervisor demonstration"
    elif args.command == "cuda-demo":
        result = run_cuda_demo()
        label = "CUDA execution model and vector-addition simulation"
    else:
        result = run_sleeping_barber(args.customers, args.chairs)
        label = "Sleeping Barber finite waiting-room demonstration"
    print(label)
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
