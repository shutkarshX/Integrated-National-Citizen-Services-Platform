import sys
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from citizen_os.concurrency.counters import run_locked_counter, run_race_demo
from citizen_os.concurrency.locks import BakeryLock, PetersonLock, StrictAlternationLock, TestAndSetLock


class CounterDemonstrationTests(unittest.TestCase):
    def test_race_demo_reproduces_lost_updates(self):
        result = run_race_demo(25)
        self.assertEqual(result["expected_total"], 50)
        self.assertEqual(result["actual_total"], 25)
        self.assertEqual(result["lost_updates"], 25)

    def test_mutex_counter_has_no_lost_updates(self):
        result = run_locked_counter(workers=5, increments_per_worker=400)
        self.assertEqual(result["actual_total"], 2000)
        self.assertEqual(result["actual_total"], result["expected_total"])

    def test_invalid_counter_arguments(self):
        with self.assertRaises(ValueError):
            run_race_demo(0)
        with self.assertRaises(ValueError):
            run_locked_counter(workers=0)


class MutualExclusionTests(unittest.TestCase):
    def _check_lock(self, lock, participants, iterations=150):
        inside = 0
        violations = []
        guard = threading.Lock()

        def worker(pid):
            nonlocal inside
            for _ in range(iterations):
                context = lock.hold(pid) if isinstance(lock, (PetersonLock, StrictAlternationLock, BakeryLock)) else lock.hold()
                with context:
                    with guard:
                        inside += 1
                        if inside != 1:
                            violations.append(inside)
                    # Encourage thread interleaving while inside the critical section.
                    threading.Event().wait(0.00001)
                    with guard:
                        inside -= 1

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(participants)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=5)
        self.assertTrue(all(not thread.is_alive() for thread in threads), "lock demo did not terminate")
        self.assertEqual(violations, [])

    def test_peterson_two_participants(self):
        self._check_lock(PetersonLock(), 2)

    def test_strict_alternation_two_participants(self):
        self._check_lock(StrictAlternationLock(), 2)

    def test_bakery_multiple_participants(self):
        self._check_lock(BakeryLock(4), 4)

    def test_test_and_set_lock(self):
        self._check_lock(TestAndSetLock(), 4)

    def test_invalid_participants(self):
        with self.assertRaises(ValueError):
            with PetersonLock().hold(2):
                pass
        with self.assertRaises(ValueError):
            BakeryLock(0)


if __name__ == "__main__":
    unittest.main()
