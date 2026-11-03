import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from citizen_os.memory_management_concepts import explain_memory_management_functions

class MemoryManagementConceptTests(unittest.TestCase):
    def test_explanation_covers_core_responsibilities(self):
        result = explain_memory_management_functions()
        for key in ("tracking", "allocation", "address_translation", "protection", "sharing", "virtual_memory", "fragmentation_management"):
            self.assertIn(key, result)
            self.assertTrue(result[key])

    def test_scope_limitation_is_explicit(self):
        result = explain_memory_management_functions()
        self.assertIn("does not implement a kernel memory manager", result["note"])

if __name__ == "__main__":
    unittest.main()
