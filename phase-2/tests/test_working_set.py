import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from citizen_os.working_set import analyze_working_set, run_working_set_demo, run_thrashing_demo


class WorkingSetTests(unittest.TestCase):
    def test_trailing_working_set_uses_distinct_pages(self):
        result = analyze_working_set([1, 2, 1, 3], 3, 3)
        self.assertEqual(result["trace"][-1]["working_set"], [1, 2, 3])
        self.assertEqual(result["trace"][-1]["working_set_size"], 3)

    def test_window_slides_forward(self):
        result = analyze_working_set([1, 2, 3, 4], 2, 2)
        self.assertEqual(result["trace"][-1]["window_references"], [3, 4])
        self.assertEqual(result["trace"][-1]["working_set"], [3, 4])

    def test_frame_pressure_flags_oversized_working_set(self):
        result = analyze_working_set([1, 2, 3, 4], 4, 3)
        self.assertTrue(result["thrashing_risk_observed"])
        self.assertEqual(result["memory_pressure_steps"], 1)

    def test_sufficient_frames_do_not_flag_pressure(self):
        result = analyze_working_set([1, 2, 3, 1], 4, 3)
        self.assertFalse(result["thrashing_risk_observed"])
        self.assertEqual(result["peak_working_set"], 3)

    def test_empty_reference_string(self):
        result = analyze_working_set([], 3, 2)
        self.assertEqual(result["trace"], [])
        self.assertFalse(result["thrashing_risk_observed"])

    def test_invalid_window_size_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze_working_set([1], 0, 2)

    def test_invalid_frame_count_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze_working_set([1], 2, 0)

    def test_negative_page_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze_working_set([-1], 2, 2)

    def test_working_set_demo_exposes_pressure(self):
        result = run_working_set_demo()
        self.assertTrue(result["thrashing_risk_observed"])
        self.assertEqual(result["peak_working_set"], 5)

    def test_thrashing_demo_runs(self):
        result = run_thrashing_demo()
        self.assertTrue(result["thrashing_risk_observed"])
        self.assertEqual(result["allocated_frames"], 3)


if __name__ == "__main__":
    unittest.main()