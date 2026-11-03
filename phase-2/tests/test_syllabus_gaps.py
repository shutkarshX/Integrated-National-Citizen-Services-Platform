import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from citizen_os.concurrency_concepts import simulate_lock_variable_race, explain_process_types
from citizen_os.demand_paging_performance import effective_access_time, compare_demand_paging_scenarios

class SyllabusGapTests(unittest.TestCase):
    def test_lock_variable_race_allows_both_processes_to_enter(self):
        result = simulate_lock_variable_race()
        self.assertEqual(result["processes_entered_critical_section"], ["P1", "P2"])
        self.assertTrue(result["mutual_exclusion_violated"])

    def test_process_type_explanation_has_common_classifications(self):
        result = explain_process_types()
        self.assertIn("independent_process", result)
        self.assertIn("cooperating_process", result)
        self.assertIn("cpu_bound_process", result)
        self.assertIn("io_bound_process", result)

    def test_effective_access_time_when_no_page_faults(self):
        result = effective_access_time(100, 0, 8000000)
        self.assertEqual(result["effective_access_time"], 100)

    def test_effective_access_time_increases_with_fault_rate(self):
        low = effective_access_time(100, 0.000001, 8000000)
        high = effective_access_time(100, 0.001, 8000000)
        self.assertGreater(high["effective_access_time"], low["effective_access_time"])

    def test_effective_access_time_validates_inputs(self):
        with self.assertRaises(ValueError):
            effective_access_time(100, 1.1, 8000000)
        with self.assertRaises(ValueError):
            effective_access_time(0, 0.01, 8000000)

    def test_scenario_comparison_has_four_fault_rates(self):
        result = compare_demand_paging_scenarios()
        self.assertEqual(len(result["scenarios"]), 4)
        self.assertEqual(result["scenarios"][0]["effective_access_time"], 100)

if __name__ == "__main__":
    unittest.main()
