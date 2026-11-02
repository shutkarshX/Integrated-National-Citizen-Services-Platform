import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from citizen_os.concurrency.patterns import (
    run_dining_philosophers, run_readers_writers, run_semaphore_demo, run_sleeping_barber,
)


class SemaphoreTests(unittest.TestCase):
    def test_binary_semaphore_limits_to_one(self):
        result = run_semaphore_demo(workers=5, permits=1, iterations=10)
        self.assertEqual(result["operations_completed"], 50)
        self.assertLessEqual(result["maximum_concurrent"], 1)

    def test_counting_semaphore_respects_permits(self):
        result = run_semaphore_demo(workers=6, permits=3, iterations=10)
        self.assertEqual(result["operations_completed"], 60)
        self.assertLessEqual(result["maximum_concurrent"], 3)

    def test_invalid_semaphore_configuration(self):
        with self.assertRaises(ValueError):
            run_semaphore_demo(workers=2, permits=3)


class MonitorAndClassicalProblemTests(unittest.TestCase):
    def test_readers_writers_monitor_excludes_writer_overlap(self):
        result = run_readers_writers(readers=4, writers=2, iterations=15)
        self.assertEqual(result["reads_completed"], 60)
        self.assertEqual(result["writes_completed"], 30)
        self.assertEqual(result["synchronization_violations"], 0)

    def test_dining_philosophers_all_finish(self):
        result = run_dining_philosophers(philosophers=5, meals=4)
        self.assertEqual(result["meals_completed"], 20)

    def test_sleeping_barber_accounts_for_every_customer(self):
        result = run_sleeping_barber(customers=12, waiting_chairs=3)
        self.assertEqual(result["accounted_for"], 12)
        self.assertEqual(result["served"] + result["turned_away"], 12)

    def test_sleeping_barber_without_waiting_chairs(self):
        result = run_sleeping_barber(customers=5, waiting_chairs=0)
        self.assertEqual(result["served"], 0)
        self.assertEqual(result["turned_away"], 5)


if __name__ == "__main__":
    unittest.main()
