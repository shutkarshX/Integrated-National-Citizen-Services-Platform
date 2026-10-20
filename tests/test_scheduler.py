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

    def test_empty_input(self):
        self.assertEqual(run_fcfs([]), [])

    def test_repeated_run_resets_terminated_schedule(self):
        request = ServiceRequest("A", "Certificate", "Citizen A", 2)
        run_fcfs([request])
        run_fcfs([request])
        self.assertEqual((request.start_time, request.finish_time), (0, 2))


if __name__ == "__main__":
    unittest.main()
