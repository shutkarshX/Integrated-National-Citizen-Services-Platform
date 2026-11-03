import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from citizen_os.loading_linking import (
    bind_address, link_modules, load_modules, run_loading_linking_demo,
)


class AddressBindingTests(unittest.TestCase):
    def test_load_base_is_added_to_relative_address(self):
        self.assertEqual(bind_address(32, 4096, 128), 4128)

    def test_relative_address_at_segment_limit_is_rejected(self):
        with self.assertRaises(ValueError):
            bind_address(128, 4096, 128)

    def test_negative_values_are_rejected(self):
        with self.assertRaises(ValueError):
            bind_address(-1, 4096, 128)


class LinkingTests(unittest.TestCase):
    def test_resolves_external_symbol_across_modules(self):
        modules = [
            {"name": "app", "exports": {"main": 0}, "requires": ["helper"]},
            {"name": "lib", "exports": {"helper": 12}, "requires": []},
        ]
        result = link_modules(modules)
        self.assertEqual(result["resolutions"]["app:helper"]["module"], "lib")
        self.assertTrue(result["linked"])

    def test_unresolved_external_symbol_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unresolved external"):
            link_modules([{"name": "app", "exports": {}, "requires": ["missing"]}])

    def test_duplicate_export_is_rejected(self):
        modules = [
            {"name": "one", "exports": {"shared": 0}},
            {"name": "two", "exports": {"shared": 4}},
        ]
        with self.assertRaisesRegex(ValueError, "duplicate symbol"):
            link_modules(modules)

    def test_negative_export_address_is_rejected(self):
        with self.assertRaises(ValueError):
            link_modules([{"name": "lib", "exports": {"func": -1}}])


class LoadingTests(unittest.TestCase):
    def test_modules_receive_consecutive_load_bases(self):
        modules = [{"name": "a", "size": 100}, {"name": "b", "size": 50}]
        result = load_modules(modules, 1000)
        self.assertEqual(result["placements"]["a"]["load_base"], 1000)
        self.assertEqual(result["placements"]["b"]["load_base"], 1100)

    def test_export_is_relocated_to_absolute_address(self):
        result = load_modules([{"name": "lib", "size": 64, "exports": {"f": 12}}], 2000)
        self.assertEqual(result["relocated_symbols"]["f"], 2012)

    def test_export_outside_module_is_rejected(self):
        with self.assertRaises(ValueError):
            load_modules([{"name": "lib", "size": 64, "exports": {"f": 64}}])


class LoadingLinkingDemoTests(unittest.TestCase):
    def test_demo_resolves_and_relocates_external_function(self):
        result = run_loading_linking_demo()
        self.assertEqual(result["loading"]["relocated_symbols"]["calculate_tax"], 4384)
        self.assertEqual(result["address_binding_example"]["absolute_address"], 4384)


if __name__ == "__main__":
    unittest.main()