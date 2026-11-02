import unittest
from citizen_os.thread_demo import run_thread_demo

class ThreadDemoTests(unittest.TestCase):
    def test_locked_counter_matches_expected_total(self):
        result = run_thread_demo(workers=5, increments_per_worker=500)
        self.assertEqual(result["actual_total"], 2500)
        self.assertEqual(result["actual_total"], result["expected_total"])

    def test_invalid_worker_count(self):
        with self.assertRaises(ValueError):
            run_thread_demo(workers=0)

if __name__ == "__main__":
    unittest.main()
