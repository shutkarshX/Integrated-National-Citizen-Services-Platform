"""File access/allocation and disk-scheduling teaching simulations."""
from collections.abc import Sequence

ACCESS_METHODS = ("sequential", "direct", "indexed")
DISK_ALGORITHMS = ("fcfs", "sstf", "scan", "c-scan", "look", "c-look")


def read_record(records: Sequence[object], method: str, *, position: int = 0, index: dict | None = None, key: object = None) -> dict[str, object]:
    """Read one record using sequential, direct or indexed access semantics."""
    if method not in ACCESS_METHODS:
        raise ValueError(f"method must be one of: {', '.join(ACCESS_METHODS)}")
    if method == "sequential":
        if not isinstance(position, int) or isinstance(position, bool) or not 0 <= position < len(records):
            raise ValueError("sequential position is outside the record sequence")
        return {"method": method, "record_number": position, "record": records[position],
                "records_scanned": position + 1}
    if method == "direct":
        if not isinstance(position, int) or isinstance(position, bool) or not 0 <= position < len(records):
            raise ValueError("direct record number is outside the record sequence")
        return {"method": method, "record_number": position, "record": records[position],
                "records_scanned": 1}
    if not isinstance(index, dict) or key not in index:
        raise ValueError("indexed access requires an index containing the requested key")
    record_number = index[key]
    if not isinstance(record_number, int) or isinstance(record_number, bool) or not 0 <= record_number < len(records):
        raise ValueError("index points outside the record sequence")
    return {"method": method, "key": key, "record_number": record_number,
            "record": records[record_number], "records_scanned": 1}


def allocate_file_blocks(method: str, file_name: str, block_count: int, disk_blocks: int = 20, start_block: int = 2) -> dict[str, object]:
    """Illustrate contiguous, linked and indexed allocation for one file."""
    if method not in ("contiguous", "linked", "indexed"):
        raise ValueError("method must be contiguous, linked or indexed")
    if not isinstance(file_name, str) or not file_name:
        raise ValueError("file_name must be a non-empty string")
    if any(not isinstance(v, int) or isinstance(v, bool) for v in (block_count, disk_blocks, start_block)):
        raise ValueError("block counts and start block must be integers")
    if block_count <= 0 or disk_blocks <= 0 or not 0 <= start_block < disk_blocks:
        raise ValueError("invalid block count, disk size or start block")
    if block_count > disk_blocks:
        raise ValueError("file cannot contain more blocks than the disk")
    if method == "contiguous":
        if start_block + block_count > disk_blocks:
            raise ValueError("contiguous file allocation exceeds disk boundary")
        blocks = list(range(start_block, start_block + block_count))
        return {"method": method, "file": file_name, "start_block": start_block,
                "length": block_count, "allocated_blocks": blocks,
                "access": "block n is at start_block + n"}
    available = [block for block in range(disk_blocks) if block != start_block]
    if method == "linked":
        blocks = available[:block_count]
        links = {block: (blocks[i + 1] if i + 1 < len(blocks) else None)
                 for i, block in enumerate(blocks)}
        return {"method": method, "file": file_name, "first_block": blocks[0],
                "allocated_blocks": blocks, "next_pointer": links,
                "access": "follow each block pointer; the final pointer is None"}
    index_block = start_block
    blocks = [block for block in available if block != index_block][:block_count]
    if len(blocks) != block_count:
        raise ValueError("not enough data blocks remain after reserving the index block")
    return {"method": method, "file": file_name, "index_block": index_block,
            "allocated_blocks": blocks, "index_entries": list(blocks),
            "access": "read the index block to locate each data block"}


def schedule_disk_requests(requests: Sequence[int], head: int, algorithm: str,
                           disk_size: int = 200, direction: str = "right") -> dict[str, object]:
    """Schedule disk cylinder requests and calculate total head movement."""
    if algorithm not in DISK_ALGORITHMS:
        raise ValueError(f"algorithm must be one of: {', '.join(DISK_ALGORITHMS)}")
    if not isinstance(disk_size, int) or isinstance(disk_size, bool) or disk_size <= 0:
        raise ValueError("disk_size must be a positive integer")
    if not isinstance(head, int) or isinstance(head, bool) or not 0 <= head < disk_size:
        raise ValueError("head must be a valid cylinder")
    if direction not in ("left", "right"):
        raise ValueError("direction must be left or right")
    if any(not isinstance(r, int) or isinstance(r, bool) or not 0 <= r < disk_size for r in requests):
        raise ValueError("all requests must be valid disk cylinders")
    pending = list(requests)
    current = head
    path = [head]
    service_order = []

    if algorithm == "fcfs":
        service_order = pending[:]
    elif algorithm == "sstf":
        while pending:
            chosen = min(pending, key=lambda r: (abs(r - current), r))
            service_order.append(chosen)
            pending.remove(chosen)
            current = chosen
    else:
        left = sorted((r for r in pending if r < head), reverse=True)
        right = sorted(r for r in pending if r >= head)
        if algorithm == "scan":
            if direction == "right":
                service_order = right + ([disk_size - 1] if not right or right[-1] != disk_size - 1 else []) + left
            else:
                service_order = left + ([0] if not left or left[-1] != 0 else []) + list(reversed(right))
        elif algorithm == "c-scan":
            if direction == "right":
                service_order = right + [disk_size - 1, 0] + sorted(left)
            else:
                service_order = left + [0, disk_size - 1] + sorted(right, reverse=True)
        elif algorithm == "look":
            service_order = (right + left) if direction == "right" else (left + list(reversed(right)))
        else:  # C-LOOK
            service_order = (right + sorted(left)) if direction == "right" else (left + sorted(right, reverse=True))

    # Add each service point/boundary to the physical head path.
    path.extend(service_order)
    total = sum(abs(path[i] - path[i - 1]) for i in range(1, len(path)))
    return {"algorithm": algorithm.upper(), "initial_head": head, "direction": direction,
            "disk_cylinders": f"0-{disk_size - 1}", "request_order": service_order,
            "movement_path": path, "total_head_movement": total,
            "average_movement_per_request": total / len(requests) if requests else 0.0}

def run_file_management_demo() -> dict[str, object]:
    records = ["Asha", "Ravi", "Mina", "Kabir", "Zoya"]
    index = {"STU-104": 1, "STU-105": 2, "STU-109": 4}
    return {
        "access_methods": {
            "sequential": read_record(records, "sequential", position=3),
            "direct": read_record(records, "direct", position=3),
            "indexed": read_record(records, "indexed", index=index, key="STU-109"),
        },
        "allocation_methods": {
            name: allocate_file_blocks(name, "student_records.dat", 4, 20, 2)
            for name in ("contiguous", "linked", "indexed")
        },
        "scope": "In-memory educational models; no real filesystem or disk blocks are modified.",
    }


def run_disk_scheduling_demo() -> dict[str, object]:
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    return {"requests": requests, "initial_head": 53, "disk_size": 200,
            "results": {name: schedule_disk_requests(requests, 53, name, 200, "right")
                        for name in DISK_ALGORITHMS},
            "scope": "Cylinder-level scheduling simulation; movement includes SCAN/C-SCAN boundary travel."}