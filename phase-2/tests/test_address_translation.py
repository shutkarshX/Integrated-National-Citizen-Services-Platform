import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from citizen_os.address_translation import (
    translate_paging, translate_segmentation, translate_segmented_paging,
    run_paging_demo, run_segmentation_demo, run_segmented_paging_demo,
)


class PagingTests(unittest.TestCase):
    def test_translates_page_and_offset(self):
        result = translate_paging(2500, 1024, [5, 9, 2, 7], 4096)
        self.assertEqual((result["page_number"], result["offset"]), (2, 452))
        self.assertEqual(result["physical_address"], 2500)

    def test_rejects_address_outside_logical_space(self):
        with self.assertRaises(ValueError):
            translate_paging(4096, 1024, [5, 9, 2, 7], 4096)

    def test_rejects_missing_page(self):
        with self.assertRaises(ValueError):
            translate_paging(2048, 1024, [0, 1])

    def test_rejects_invalid_page_size(self):
        with self.assertRaises(ValueError):
            translate_paging(0, 0, [0])


class SegmentationTests(unittest.TestCase):
    def test_translates_valid_segment_offset(self):
        result = translate_segmentation(1_000_120, [{"base": 1000, "limit": 400}, {"base": 5000, "limit": 800}])
        self.assertEqual(result["physical_address"], 5120)

    def test_rejects_segment_limit_violation(self):
        with self.assertRaises(ValueError):
            translate_segmentation(1_000_800, [{"base": 1000, "limit": 400}, {"base": 5000, "limit": 800}])

    def test_rejects_unknown_segment(self):
        with self.assertRaises(ValueError):
            translate_segmentation(2_000_000, [{"base": 100, "limit": 50}])


class SegmentedPagingTests(unittest.TestCase):
    def test_translates_segment_page_and_offset(self):
        result = translate_segmented_paging(1, 1500, 1024, [[4, 1], [8, 3, 6]], [1500, 2500])
        self.assertEqual((result["page_number"], result["page_offset"], result["frame_number"]), (1, 476, 3))
        self.assertEqual(result["physical_address"], 3548)

    def test_rejects_offset_beyond_segment_limit(self):
        with self.assertRaises(ValueError):
            translate_segmented_paging(0, 1500, 1024, [[4, 1]], [1500])

    def test_rejects_missing_segment_page(self):
        with self.assertRaises(ValueError):
            translate_segmented_paging(0, 1200, 1024, [[4]], [1500])


class AddressTranslationDemoTests(unittest.TestCase):
    def test_all_demos_run(self):
        self.assertEqual(run_paging_demo()["physical_address"], 2500)
        self.assertEqual(run_segmentation_demo()["physical_address"], 5120)
        self.assertEqual(run_segmented_paging_demo()["physical_address"], 3548)


if __name__ == "__main__":
    unittest.main()
