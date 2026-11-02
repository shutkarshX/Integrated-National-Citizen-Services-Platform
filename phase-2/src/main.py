#!/usr/bin/env python3
"""Command-line entry point for Phase 2 OS demonstrations."""
import argparse
from citizen_os.concurrency.counters import run_locked_counter, run_race_demo
from citizen_os.concurrency.locks import run_lock_demo


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 2: concurrency and synchronization demos")
    sub = parser.add_subparsers(dest="command", required=True)

    race = sub.add_parser("race-demo", help="reproduce a shared-counter race condition")
    race.add_argument("--iterations", type=int, default=100)

    locked = sub.add_parser("locked-demo", help="run a mutex-protected shared counter")
    locked.add_argument("--workers", type=int, default=4)
    locked.add_argument("--iterations", type=int, default=1000)

    lock = sub.add_parser("lock-demo", help="compare a syllabus mutual-exclusion algorithm")
    lock.add_argument("--algorithm", choices=["peterson", "strict-alternation", "bakery", "test-and-set"], default="peterson")
    lock.add_argument("--workers", type=int, default=2)
    lock.add_argument("--iterations", type=int, default=500)

    args = parser.parse_args()
    if args.command == "race-demo":
        result = run_race_demo(args.iterations)
        print("Race condition demonstration (two workers, unsynchronized read-modify-write)")
    elif args.command == "locked-demo":
        result = run_locked_counter(args.workers, args.iterations)
        print("Mutex demonstration (shared counter protected by threading.Lock)")
    else:
        result = run_lock_demo(args.algorithm, args.workers, args.iterations)
        print(f"Mutual exclusion demonstration: {args.algorithm}")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
