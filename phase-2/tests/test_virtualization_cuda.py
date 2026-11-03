import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from citizen_os.virtualization_cuda import (
    create_virtual_machine, compare_hypervisors, simulate_cuda_vector_add,
    explain_cuda_execution_model, run_virtualization_demo, run_cuda_demo,
)


class VirtualMachineTests(unittest.TestCase):
    def test_creates_valid_vm_configuration(self):
        result = create_virtual_machine("Lab VM", 2, 4, 8, 16)
        self.assertEqual(result["state"], "configured")
        self.assertEqual(result["virtual_cpus"], 2)
        self.assertEqual(result["memory_utilization_of_host_capacity_percent"], 25.0)

    def test_trims_vm_name(self):
        self.assertEqual(create_virtual_machine("  VM  ", 1, 1, 2, 4)["name"], "VM")

    def test_supports_type_two_hypervisor(self):
        result = create_virtual_machine("Desktop VM", 1, 2, 4, 8, "type-2")
        self.assertEqual(result["hypervisor_type"], "type-2")

    def test_rejects_empty_vm_name(self):
        with self.assertRaises(ValueError):
            create_virtual_machine("", 1, 1, 2, 4)

    def test_rejects_unknown_hypervisor_type(self):
        with self.assertRaises(ValueError):
            create_virtual_machine("VM", 1, 1, 2, 4, "type-3")

    def test_rejects_cpu_overcommit(self):
        with self.assertRaises(ValueError):
            create_virtual_machine("VM", 5, 1, 4, 8)

    def test_rejects_memory_overcommit(self):
        with self.assertRaises(ValueError):
            create_virtual_machine("VM", 1, 9, 4, 8)

    def test_rejects_non_integer_resources(self):
        with self.assertRaises(ValueError):
            create_virtual_machine("VM", 1.5, 1, 4, 8)

    def test_rejects_non_positive_resources(self):
        with self.assertRaises(ValueError):
            create_virtual_machine("VM", 0, 1, 4, 8)


class HypervisorConceptTests(unittest.TestCase):
    def test_comparison_contains_both_types(self):
        result = compare_hypervisors()
        self.assertEqual(set(result), {"type-1", "type-2", "note"})
        self.assertIn("physical hardware", result["type-1"]["placement"])
        self.assertIn("host operating system", result["type-2"]["placement"])


class CudaSimulationTests(unittest.TestCase):
    def test_vector_addition_with_exact_block_division(self):
        result = simulate_cuda_vector_add([1, 2, 3, 4], [10, 20, 30, 40], 2)
        self.assertEqual(result["output"], [11, 22, 33, 44])
        self.assertEqual(result["blocks_in_grid"], 2)
        self.assertEqual(result["inactive_threads_due_to_bounds"], 0)

    def test_vector_addition_with_partial_final_block(self):
        result = simulate_cuda_vector_add([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], 4)
        self.assertEqual(result["output"], [6, 6, 6, 6, 6])
        self.assertEqual(result["blocks_in_grid"], 2)
        self.assertEqual(result["launched_threads"], 8)
        self.assertEqual(result["inactive_threads_due_to_bounds"], 3)

    def test_empty_vectors_launch_no_blocks(self):
        result = simulate_cuda_vector_add([], [], 4)
        self.assertEqual(result["output"], [])
        self.assertEqual(result["blocks_in_grid"], 0)

    def test_rejects_mismatched_vector_lengths(self):
        with self.assertRaises(ValueError):
            simulate_cuda_vector_add([1], [1, 2], 1)

    def test_rejects_non_positive_threads_per_block(self):
        with self.assertRaises(ValueError):
            simulate_cuda_vector_add([1], [2], 0)

    def test_rejects_non_numeric_vector_elements(self):
        with self.assertRaises(ValueError):
            simulate_cuda_vector_add(["one"], [2], 1)

    def test_cuda_execution_model_documents_index_formula(self):
        result = explain_cuda_execution_model()
        self.assertIn("blockIdx.x", result["common_global_index"])
        self.assertIn("threadIdx.x", result["common_global_index"])


class VirtualizationCudaDemoTests(unittest.TestCase):
    def test_virtualization_demo_runs(self):
        result = run_virtualization_demo()
        self.assertEqual(result["vm"]["name"], "OS-Lab-VM")

    def test_cuda_demo_runs_and_computes_expected_vector(self):
        result = run_cuda_demo()
        self.assertEqual(result["vector_addition"]["output"], [11, 22, 33, 44, 55, 66, 77])


if __name__ == "__main__":
    unittest.main()