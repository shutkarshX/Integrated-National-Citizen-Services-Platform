"""CLI entry point for the citizen services OS simulator."""

from pathlib import Path

from os_platform.models import ServiceRequest
from os_platform.scheduler import run_fcfs
from os_platform.storage import load_requests, save_requests

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "demo_requests.json"


def initial_demo_requests():
    """Return synthetic requests used by the initial demonstration."""
    return [
        ServiceRequest("REQ-001", "Certificate", "Citizen A", burst_time=3),
        ServiceRequest("REQ-002", "Identity", "Citizen B", burst_time=2),
        ServiceRequest("REQ-003", "Grievance", "Citizen C", burst_time=4),
        ServiceRequest("REQ-004", "Tax", "Citizen D", burst_time=1),
    ]


def main():
    requests = load_requests(DATA_FILE)
    if not requests:
        requests = initial_demo_requests()

    print("Integrated National Citizen Services Platform")
    print("Educational OS simulation — synthetic demo records only")
    print("\nFCFS processing order:")
    results = run_fcfs(requests)
    for request in results:
        print(
            f"{request.request_id}: {request.service_type:<12} "
            f"state={request.state.value:<12} "
            f"start={request.start_time} finish={request.finish_time}"
        )

    save_requests(DATA_FILE, results)
    print(f"\nSaved demonstration state to {DATA_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
