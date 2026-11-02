"""Paging, segmentation and segmented-paging address translation simulations."""
from __future__ import annotations

from collections.abc import Sequence


def _positive_int(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")


def translate_paging(logical_address: int, page_size: int, page_table: Sequence[int],
                     logical_space_size: int | None = None) -> dict[str, int]:
    """Translate a logical address through a page table of page-to-frame mappings."""
    _positive_int(page_size, "page_size")
    if not isinstance(logical_address, int) or isinstance(logical_address, bool) or logical_address < 0:
        raise ValueError("logical_address must be a non-negative integer")
    if logical_space_size is not None:
        _positive_int(logical_space_size, "logical_space_size")
        if logical_address >= logical_space_size:
            raise ValueError("logical address is outside the logical address space")
    page_number, offset = divmod(logical_address, page_size)
    if page_number >= len(page_table):
        raise ValueError("page number is not present in the page table")
    frame_number = page_table[page_number]
    if not isinstance(frame_number, int) or isinstance(frame_number, bool) or frame_number < 0:
        raise ValueError("page table frame numbers must be non-negative integers")
    physical_address = frame_number * page_size + offset
    return {"logical_address": logical_address, "page_number": page_number,
            "offset": offset, "frame_number": frame_number,
            "physical_address": physical_address}


def translate_segmentation(logical_address: int, segments: Sequence[dict[str, int]]) -> dict[str, int]:
    """Translate a segment:offset logical address using base and limit registers."""
    if not isinstance(logical_address, int) or isinstance(logical_address, bool) or logical_address < 0:
        raise ValueError("logical_address must be a non-negative integer")
    segment_number, offset = divmod(logical_address, 1_000_000)
    if segment_number >= len(segments):
        raise ValueError("segment number is not present in the segment table")
    segment = segments[segment_number]
    base, limit = segment["base"], segment["limit"]
    if any(not isinstance(v, int) or isinstance(v, bool) for v in (base, limit)) or base < 0 or limit <= 0:
        raise ValueError("segment base must be non-negative and limit must be positive")
    if offset >= limit:
        raise ValueError("segment limit violation")
    return {"logical_address": logical_address, "segment_number": segment_number,
            "offset": offset, "base": base, "limit": limit,
            "physical_address": base + offset}


def translate_segmented_paging(segment_number: int, offset: int, page_size: int,
                               segment_page_tables: Sequence[Sequence[int]],
                               segment_lengths: Sequence[int]) -> dict[str, int]:
    """Translate a segment number and offset through that segment's page table."""
    _positive_int(page_size, "page_size")
    if not isinstance(segment_number, int) or isinstance(segment_number, bool) or not 0 <= segment_number < len(segment_page_tables):
        raise ValueError("segment number is not present in the segment table")
    if not isinstance(offset, int) or isinstance(offset, bool) or offset < 0:
        raise ValueError("offset must be a non-negative integer")
    if segment_number >= len(segment_lengths) or offset >= segment_lengths[segment_number]:
        raise ValueError("offset is outside the segment limit")
    page_number, page_offset = divmod(offset, page_size)
    page_table = segment_page_tables[segment_number]
    if page_number >= len(page_table):
        raise ValueError("page is not present in this segment's page table")
    frame_number = page_table[page_number]
    if not isinstance(frame_number, int) or isinstance(frame_number, bool) or frame_number < 0:
        raise ValueError("frame numbers must be non-negative integers")
    return {"segment_number": segment_number, "offset": offset,
            "page_number": page_number, "page_offset": page_offset,
            "frame_number": frame_number,
            "physical_address": frame_number * page_size + page_offset}


def run_paging_demo() -> dict[str, object]:
    return {"page_size": 1024, "page_table": [5, 9, 2, 7],
            **translate_paging(2500, 1024, [5, 9, 2, 7], 4096),
            "note": "Paging divides logical memory into pages and physical memory into equal-sized frames; a page table maps pages to frames."}


def run_segmentation_demo() -> dict[str, object]:
    segments = [{"base": 1000, "limit": 400}, {"base": 5000, "limit": 800},
                {"base": 9000, "limit": 600}]
    return {"segment_table": segments, **translate_segmentation(1_000_120, segments),
            "note": "Segmentation uses variable-sized logical segments; each segment has a base and a limit."}


def run_segmented_paging_demo() -> dict[str, object]:
    tables = [[4, 1], [8, 3, 6], [2]]
    lengths = [1500, 2500, 700]
    return {"page_size": 1024, "segment_page_tables": tables,
            **translate_segmented_paging(1, 1500, 1024, tables, lengths),
            "note": "Segmented paging first selects a segment, then uses that segment's page table to map its page to a frame."}
