import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from citizen_os.concurrency.synchronization import run_pipe_ipc, run_producer_consumer


class ProducerConsumerTests(unittest.TestCase):
    def test_bounded_buffer_transfers_every_item(self):
        result = run_producer_consumer(items=50, capacity=3)
        self.assertEqual(result["items_consumed"], 50)
        self.assertEqual(result["consumed_sum"], result["expected_sum"])
        self.assertTrue(result["buffer_empty"])

    def test_zero_items_is_valid(self):
        result = run_producer_consumer(items=0, capacity=2)
        self.assertEqual(result["items_consumed"], 0)
        self.assertEqual(result["consumed_sum"], 0)
        self.assertTrue(result["buffer_empty"])

    def test_invalid_buffer_arguments(self):
        with self.assertRaises(ValueError):
            run_producer_consumer(items=-1)
        with self.assertRaises(ValueError):
            run_producer_consumer(capacity=0)


class PipeIPCTests(unittest.TestCase):
    def test_parent_child_message_round_trip(self):
        result = run_pipe_ipc("citizen services")
        self.assertEqual(result["sent"], "citizen services")
        self.assertEqual(result["received"], "citizen services")
        self.assertEqual(result["response"], "CITIZEN SERVICES")

    def test_empty_message_is_rejected(self):
        with self.assertRaises(ValueError):
            run_pipe_ipc("")


if __name__ == "__main__":
    unittest.main()
