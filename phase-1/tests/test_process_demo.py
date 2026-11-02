import unittest
from citizen_os.process_demo import run_process_demo

class ProcessDemoTests(unittest.TestCase):
    def test_launches_real_child_processes(self):
        results = run_process_demo()
        self.assertEqual(len(results), 2)
        self.assertTrue(all(item["pid"] > 0 for item in results))
        self.assertTrue(all(item["return_code"] == 0 for item in results))
        self.assertTrue(all(item["output"] for item in results))

if __name__ == "__main__":
    unittest.main()
