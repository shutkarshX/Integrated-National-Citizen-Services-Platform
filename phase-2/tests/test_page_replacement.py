import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from citizen_os.page_replacement import (
    simulate_page_replacement, compare_page_replacement,
    run_demand_paging_demo, run_page_replacement_comparison,
    run_belady_anomaly_demo,
)


class PageReplacementTests(unittest.TestCase):
    def test_fifo_fault_and_hit_counts(self):
        result = simulate_page_replacement([1, 2, 3, 1, 4], 3, "fifo")
        self.assertEqual((result["page_faults"], result["hits"]), (4, 1))

    def test_lru_replaces_least_recently_used_page(self):
        result = simulate_page_replacement([1, 2, 3, 1, 4], 3, "lru")
        self.assertEqual(result["trace"][-1]["evicted"], 2)

    def test_optimal_replaces_page_used_farthest_in_future(self):
        result = simulate_page_replacement([1, 2, 3, 4, 1, 2, 5], 3, "optimal")
        self.assertEqual(result["trace"][3]["evicted"], 3)

    def test_lfu_tie_uses_least_recently_used(self):
        result = simulate_page_replacement([1, 2, 1, 2, 3], 2, "lfu")
        self.assertEqual(result["trace"][-1]["evicted"], 1)

    def test_empty_reference_string_has_zero_faults(self):
        result = simulate_page_replacement([], 3, "fifo")
        self.assertEqual(result["page_faults"], 0)
        self.assertEqual(result["fault_ratio"], 0.0)

    def test_invalid_frame_count_is_rejected(self):
        with self.assertRaises(ValueError):
            simulate_page_replacement([1], 0, "fifo")

    def test_invalid_algorithm_is_rejected(self):
        with self.assertRaises(ValueError):
            simulate_page_replacement([1], 2, "random")

    def test_negative_page_number_is_rejected(self):
        with self.assertRaises(ValueError):
            simulate_page_replacement([-1], 2, "fifo")

    def test_comparison_contains_all_four_algorithms(self):
        result = compare_page_replacement([1, 2, 3], 2)
        self.assertEqual(set(result), {"fifo", "lru", "optimal", "lfu"})

    def test_demand_paging_demo_runs(self):
        result = run_demand_paging_demo()
        self.assertEqual(result["page_faults"], 6)

    def test_comparison_demo_runs(self):
        result = run_page_replacement_comparison()
        self.assertEqual(set(result["results"]), {"fifo", "lru", "optimal", "lfu"})

    def test_belady_anomaly_is_reproduced(self):
        result = run_belady_anomaly_demo()
        self.assertEqual(result["three_frames_faults"], 9)
        self.assertEqual(result["four_frames_faults"], 10)
        self.assertTrue(result["belady_anomaly_observed"])


if __name__ == "__main__":
    unittest.main()
