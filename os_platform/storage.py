"""JSON persistence helpers for the synthetic demonstration data."""

import json
from pathlib import Path

from .models import ServiceRequest


def save_requests(path: str | Path, requests: list[ServiceRequest]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = [request.to_dict() for request in requests]
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_requests(path: str | Path) -> list[ServiceRequest]:
    source = Path(path)
    if not source.exists():
        return []
    raw = source.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError("request data must be a JSON list")
    return [ServiceRequest.from_dict(item) for item in data]
