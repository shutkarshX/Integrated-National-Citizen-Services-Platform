import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from citizen_os.deadlock import (
    bankers_request, bankers_safety, deadlock_conditions_and_prevention, detect_deadlock,
    find_directed_cycle, recover_by_terminating_victim, resource_allocation_graph_demo,
    run_bankers_demo,
)


class ResourceAllocationGraphTests(unittest.TestCase):
    def test_cycle_is_detected(self):
        result = resource_allocation_graph_demo()
        self.assertTrue(result["cycle_detected"])
        self.assertEqual(result["cycle"][0], result["cycle"][-1])

    def test_acyclic_graph_has_no_cycle(self):
        self.assertIsNone(find_directed_cycle({"P1": ["R1"], "R1": ["P2"], "P2": []}))


class BankersAlgorithmTests(unittest.TestCase):
    def test_classic_example_is_safe(self):
        result = run_bankers_demo()
        self.assertTrue(result["safe"])
        self.assertEqual(result["safe_sequence"], [1, 3, 4, 0, 2])

    def test_request_is_granted_when_safe(self):
        allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
        maximum = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
        result = bankers_request(allocation, maximum, [3, 3, 2], 1, [1, 0, 2])
        self.assertEqual(result["status"], "granted")

    def test_request_exceeding_need_is_rejected(self):
        result = bankers_request([[0]], [[1]], [1], 0, [2])
        self.assertEqual(result["status"], "rejected")

    def test_request_waits_if_not_available(self):
        result = bankers_request([[0]], [[2]], [1], 0, [2])
        self.assertEqual(result["status"], "waiting")

    def test_unsafe_state_is_reported(self):
        result = bankers_safety([[1], [1]], [[2], [2]], [0])
        self.assertFalse(result["safe"])


class DetectionAndRecoveryTests(unittest.TestCase):
    def test_detection_finds_deadlocked_processes(self):
        result = detect_deadlock([0, 0], [[1, 0], [0, 1]], [[0, 1], [1, 0]])
        self.assertTrue(result["deadlock_detected"])
        self.assertEqual(result["deadlocked_processes"], [0, 1])

    def test_detection_finds_no_deadlock_when_request_can_be_met(self):
        result = detect_deadlock([1], [[1], [0]], [[1], [0]])
        self.assertFalse(result["deadlock_detected"])

    def test_recovery_selects_largest_holder(self):
        result = recover_by_terminating_victim([[1, 0], [0, 3]], [0, 1])
        self.assertEqual(result["victim_process"], 1)
        self.assertEqual(result["released_resources"], [0, 3])

    def test_four_coffman_conditions_are_documented(self):
        result = deadlock_conditions_and_prevention()
        self.assertEqual(len(result["necessary_conditions"]), 4)
        self.assertEqual(len(result["prevention_strategies"]), 4)


if __name__ == "__main__":
    unittest.main()
