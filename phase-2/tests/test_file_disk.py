import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from citizen_os.file_disk import (
    read_record, allocate_file_blocks, schedule_disk_requests,
    run_file_management_demo, run_disk_scheduling_demo,
)


class FileAccessTests(unittest.TestCase):
    def setUp(self):
        self.records = ["Asha", "Ravi", "Mina", "Kabir"]

    def test_sequential_access_returns_requested_record(self):
        result = read_record(self.records, "sequential", position=2)
        self.assertEqual(result["record"], "Mina")
        self.assertEqual(result["records_scanned"], 3)

    def test_direct_access_reads_record_by_number(self):
        result = read_record(self.records, "direct", position=2)
        self.assertEqual(result["record"], "Mina")
        self.assertEqual(result["records_scanned"], 1)

    def test_indexed_access_resolves_key(self):
        result = read_record(self.records, "indexed", index={"S-3": 2}, key="S-3")
        self.assertEqual(result["record"], "Mina")

    def test_unknown_access_method_is_rejected(self):
        with self.assertRaises(ValueError):
            read_record(self.records, "random")

    def test_invalid_record_position_is_rejected(self):
        with self.assertRaises(ValueError):
            read_record(self.records, "direct", position=9)

    def test_missing_index_key_is_rejected(self):
        with self.assertRaises(ValueError):
            read_record(self.records, "indexed", index={}, key="missing")


class FileAllocationTests(unittest.TestCase):
    def test_contiguous_allocation_uses_adjacent_blocks(self):
        result = allocate_file_blocks("contiguous", "a.dat", 4, 20, 5)
        self.assertEqual(result["allocated_blocks"], [5, 6, 7, 8])

    def test_contiguous_allocation_rejects_disk_overflow(self):
        with self.assertRaises(ValueError):
            allocate_file_blocks("contiguous", "a.dat", 4, 10, 8)

    def test_linked_allocation_builds_pointer_chain(self):
        result = allocate_file_blocks("linked", "a.dat", 3, 10, 2)
        blocks = result["allocated_blocks"]
        self.assertEqual(result["next_pointer"][blocks[0]], blocks[1])
        self.assertIsNone(result["next_pointer"][blocks[-1]])

    def test_indexed_allocation_reserves_index_block(self):
        result = allocate_file_blocks("indexed", "a.dat", 3, 10, 2)
        self.assertEqual(result["index_block"], 2)
        self.assertEqual(result["index_entries"], result["allocated_blocks"])
        self.assertNotIn(2, result["allocated_blocks"])

    def test_invalid_allocation_method_is_rejected(self):
        with self.assertRaises(ValueError):
            allocate_file_blocks("chained", "a.dat", 2)

    def test_invalid_file_size_is_rejected(self):
        with self.assertRaises(ValueError):
            allocate_file_blocks("linked", "a.dat", 0)


class DiskSchedulingTests(unittest.TestCase):
    def setUp(self):
        self.requests = [98, 183, 37, 122, 14, 124, 65, 67]

    def test_fcfs_total_head_movement(self):
        result = schedule_disk_requests(self.requests, 53, "fcfs")
        self.assertEqual(result["total_head_movement"], 640)

    def test_sstf_total_head_movement(self):
        result = schedule_disk_requests(self.requests, 53, "sstf")
        self.assertEqual(result["total_head_movement"], 236)

    def test_scan_moves_to_disk_boundary_before_reversing(self):
        result = schedule_disk_requests(self.requests, 53, "scan")
        self.assertIn(199, result["movement_path"])
        self.assertEqual(result["total_head_movement"], 331)

    def test_c_scan_wraps_to_opposite_boundary(self):
        result = schedule_disk_requests(self.requests, 53, "c-scan")
        self.assertEqual(result["total_head_movement"], 382)
        self.assertIn(0, result["movement_path"])

    def test_look_reverses_at_last_request(self):
        result = schedule_disk_requests(self.requests, 53, "look")
        self.assertEqual(result["total_head_movement"], 299)

    def test_c_look_wraps_between_extreme_requests(self):
        result = schedule_disk_requests(self.requests, 53, "c-look")
        self.assertEqual(result["total_head_movement"], 322)

    def test_left_direction_is_supported(self):
        result = schedule_disk_requests(self.requests, 53, "scan", direction="left")
        self.assertEqual(result["request_order"][0], 37)
        self.assertIn(0, result["movement_path"])

    def test_invalid_disk_request_is_rejected(self):
        with self.assertRaises(ValueError):
            schedule_disk_requests([250], 53, "fcfs")

    def test_invalid_algorithm_is_rejected(self):
        with self.assertRaises(ValueError):
            schedule_disk_requests(self.requests, 53, "round-robin")

    def test_empty_request_queue_has_zero_movement(self):
        result = schedule_disk_requests([], 53, "fcfs")
        self.assertEqual(result["total_head_movement"], 0)


class FileDiskDemoTests(unittest.TestCase):
    def test_file_management_demo_contains_access_and_allocation_methods(self):
        result = run_file_management_demo()
        self.assertEqual(set(result["access_methods"]), {"sequential", "direct", "indexed"})
        self.assertEqual(set(result["allocation_methods"]), {"contiguous", "linked", "indexed"})

    def test_disk_demo_compares_six_algorithms(self):
        result = run_disk_scheduling_demo()
        self.assertEqual(set(result["results"]), {"fcfs", "sstf", "scan", "c-scan", "look", "c-look"})


if __name__ == "__main__":
    unittest.main()