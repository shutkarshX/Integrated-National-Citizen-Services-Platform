#!/usr/bin/env python3
"""Command-line entry point for Phase 2 OS demonstrations."""
import argparse
from citizen_os.concurrency.counters import run_locked_counter, run_race_demo


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 2: concurrency and synchronization demos")
    sub = parser.add_subparsers(dest="command", required=True)
    race = sub.add_parser("race-demo", help="reproduce a shared-counter race condition")
    race.add_argument("--iterations", type=int, default=100)
    locked = sub.add_parser("locked-demo", help="run a mutex-protected shared counter")
    locked.add_argument("--workers", type=int, default=4)
    locked.add_argument("--iterations", type=int, default=1000)
    args = parser.parse_args()

    if args.command == "race-demo":
        result = run_race_demo(args.iterations)
        print("Race condition demonstration (two workers, unsynchronized read-modify-write)")
    else:
        result = run_locked_counter(args.workers, args.iterations)
        print("Mutual exclusion demonstration (shared counter protected by mutex)")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
