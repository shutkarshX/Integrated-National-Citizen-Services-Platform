import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from citizen_os.memory_allocation import (
    allocate_fixed_partitions, allocate_variable_partitions,
    run_fixed_partition_demo, run_variable_partition_demo,
)


class FixedPartitionTests(unittest.TestCase):
    def test_fixed_partitions_report_internal_fragmentation(self):
        result = allocate_fixed_partitions([100, 500, 200], [90, 150])
        self.assertEqual(len(result["allocations"]), 2)
        self.assertEqual(result["total_internal_fragmentation"], 360)

    def test_fixed_best_fit_chooses_smallest_suitable_partition(self):
        result = allocate_fixed_partitions([300, 200, 500], [180], "best-fit")
        self.assertEqual(result["allocations"][0]["partition"], 1)

    def test_fixed_worst_fit_chooses_largest_suitable_partition(self):
        result = allocate_fixed_partitions([300, 200, 500], [180], "worst-fit")
        self.assertEqual(result["allocations"][0]["partition"], 2)

    def test_fixed_partition_holds_only_one_process(self):
        result = allocate_fixed_partitions([200], [100, 50])
        self.assertEqual(result["unallocated_processes"], [1])

    def test_fixed_partition_invalid_inputs(self):
        with self.assertRaises(ValueError):
            allocate_fixed_partitions([100, 0], [10])
        with self.assertRaises(ValueError):
            allocate_fixed_partitions([100], [10], "next-fit")


class VariablePartitionTests(unittest.TestCase):
    def test_first_fit_allocates_from_lowest_address_hole(self):
        result = allocate_variable_partitions(1000, [200, 300], "first-fit")
        self.assertEqual(result["allocations"][0]["start"], 0)
        self.assertEqual(result["allocations"][1]["start"], 200)

    def test_best_and_worst_fit_select_different_holes(self):
        # After the first allocation, the free regions are 200 and 500 bytes.
        sizes = [300, 200, 500]
        processes = [300, 180, 150]
        best = allocate_variable_partitions(1000, processes, "best-fit")
        worst = allocate_variable_partitions(1000, processes, "worst-fit")
        self.assertNotEqual(best["allocations"][1]["start"], worst["allocations"][1]["start"])

    def test_unallocated_process_is_reported(self):
        result = allocate_variable_partitions(100, [101])
        self.assertEqual(result["unallocated_processes"], [0])

    def test_free_memory_and_fragmentation_are_consistent(self):
        result = allocate_variable_partitions(1000, [300, 200])
        self.assertEqual(result["total_free_memory"], 500)
        self.assertEqual(result["largest_free_hole"], 500)
        self.assertEqual(result["external_fragmentation"], 0)

    def test_variable_invalid_inputs(self):
        with self.assertRaises(ValueError):
            allocate_variable_partitions(0, [10])
        with self.assertRaises(ValueError):
            allocate_variable_partitions(100, [10], "invalid")


class MemoryAllocationDemoTests(unittest.TestCase):
    def test_fixed_demo_contains_all_three_strategies(self):
        self.assertEqual(set(run_fixed_partition_demo()), {"first-fit", "best-fit", "worst-fit"})

    def test_variable_demo_runs_for_each_strategy(self):
        for strategy in ("first-fit", "best-fit", "worst-fit"):
            self.assertEqual(run_variable_partition_demo(strategy)["strategy"], strategy)


if __name__ == "__main__":
    unittest.main()
