import unittest

from os_platform.models import RequestState, ServiceRequest
from os_platform.scheduler import run_fcfs


class FCFSSchedulerTests(unittest.TestCase):
    def test_requests_run_in_input_order(self):
        requests = [
            ServiceRequest("A", "Certificate", "Citizen A", 3),
            ServiceRequest("B", "Identity", "Citizen B", 2),
            ServiceRequest("C", "Tax", "Citizen C", 1),
        ]

        results = run_fcfs(requests)

        self.assertEqual([r.request_id for r in results], ["A", "B", "C"])
        self.assertEqual(
            [(r.start_time, r.finish_time) for r in results],
            [(0, 3), (3, 5), (5, 6)],
        )

    def test_all_processed_requests_terminate(self):
        request = ServiceRequest("A", "Certificate", "Citizen A", 2)
        run_fcfs([request])
        self.assertEqual(request.state, RequestState.TERMINATED)

    def test_waiting_and_turnaround_times_are_calculated(self):
        first = ServiceRequest("A", "Certificate", "Citizen A", 3)
        second = ServiceRequest("B", "Identity", "Citizen B", 2)

        run_fcfs([first, second])

        self.assertEqual((first.waiting_time, first.turnaround_time), (0, 3))
        self.assertEqual((second.waiting_time, second.turnaround_time), (3, 5))

    def test_late_arrival_leaves_cpu_idle_until_arrival(self):
        request = ServiceRequest("LATE", "Tax", "Citizen X", 2, arrival_time=5)

        run_fcfs([request])

        self.assertEqual((request.start_time, request.finish_time), (5, 7))
        self.assertEqual((request.waiting_time, request.turnaround_time), (0, 2))

    def test_negative_arrival_time_is_rejected(self):
        with self.assertRaises(ValueError):
            ServiceRequest("BAD", "Tax", "Citizen X", 2, arrival_time=-1)

    def test_empty_input(self):
        self.assertEqual(run_fcfs([]), [])

    def test_repeated_run_resets_terminated_schedule(self):
        request = ServiceRequest("A", "Certificate", "Citizen A", 2)
        run_fcfs([request])
        run_fcfs([request])
        self.assertEqual((request.start_time, request.finish_time), (0, 2))
        self.assertEqual((request.waiting_time, request.turnaround_time), (0, 2))


if __name__ == "__main__":
    unittest.main()
