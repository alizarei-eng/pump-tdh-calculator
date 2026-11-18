import unittest

from core.elevation import calculate_static_head, calculate_static_head_from_difference


class TestStaticHead(unittest.TestCase):
    def test_uphill_destination(self):
        self.assertEqual(calculate_static_head(elevation_start_m=10, elevation_end_m=35), 25.0)

    def test_downhill_destination(self):
        self.assertEqual(calculate_static_head(elevation_start_m=35, elevation_end_m=10), -25.0)

    def test_same_elevation(self):
        self.assertEqual(calculate_static_head(elevation_start_m=12, elevation_end_m=12), 0.0)

    def test_negative_elevation_is_valid(self):
        self.assertEqual(calculate_static_head(elevation_start_m=-5, elevation_end_m=8), 13.0)

    def test_direct_difference(self):
        self.assertEqual(calculate_static_head_from_difference(-12.5), -12.5)

    def test_non_finite_values_are_rejected(self):
        with self.assertRaises(ValueError):
            calculate_static_head(elevation_start_m=0, elevation_end_m=float("inf"))
        with self.assertRaises(ValueError):
            calculate_static_head_from_difference(float("nan"))


if __name__ == "__main__":
    unittest.main()
