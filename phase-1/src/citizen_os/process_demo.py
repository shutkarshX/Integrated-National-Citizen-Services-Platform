"""Real user-space process demonstration using Python's subprocess module."""
from __future__ import annotations
import subprocess
import sys
import time

def run_process_demo() -> list[dict[str, int | str]]:
    """Launch and wait for two real child processes; no shell or system changes."""
    jobs = [
        ("citizen-record-check", "print('Citizen record check completed')"),
        ("document-indexer", "print('Document indexing completed')"),
    ]
    results = []
    for label, code in jobs:
        started = time.monotonic()
        child = subprocess.Popen(
            [sys.executable, "-c", code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = child.communicate(timeout=10)
        results.append({
            "name": label,
            "pid": child.pid,
            "return_code": child.returncode,
            "duration_ms": round((time.monotonic() - started) * 1000),
            "output": stdout.strip(),
            "error": stderr.strip(),
        })
        if child.returncode != 0:
            raise RuntimeError(f"{label} failed: {stderr.strip()}")
    return results
