import unittest
from core.pump_power import calculate_power, interpolate_curve, validate_pump_curve


class TestPumpPower(unittest.TestCase):
    def test_power_with_manual_efficiencies(self):
        result = calculate_power(
            flow_m3_h=50, required_tdh_m=40, density_kg_m3=1000,
            pump_efficiency=0.78, motor_efficiency=0.92)
        self.assertAlmostEqual(result["hydraulic_power_kw"], 5.448, places=2)
        self.assertGreater(result["shaft_power_kw"], result["hydraulic_power_kw"])
        self.assertGreater(result["electric_power_kw"], result["shaft_power_kw"])

    def test_default_efficiencies_are_idealized(self):
        result = calculate_power(
            flow_m3_h=50, required_tdh_m=40, density_kg_m3=1000)
        self.assertAlmostEqual(result["shaft_power_kw"], result["hydraulic_power_kw"])
        self.assertAlmostEqual(result["electric_power_kw"], result["hydraulic_power_kw"])

    def test_interpolates_head_and_efficiency(self):
        points = [
            {"flow_m3_h": 20, "head_m": 55, "pump_efficiency": 0.62, "shaft_power_kw": None},
            {"flow_m3_h": 40, "head_m": 44, "pump_efficiency": 0.78, "shaft_power_kw": None},
            {"flow_m3_h": 60, "head_m": 27, "pump_efficiency": 0.74, "shaft_power_kw": None},
        ]
        validate_pump_curve(points)
        self.assertAlmostEqual(interpolate_curve(points, 30, "head_m"), 49.5)
        self.assertAlmostEqual(interpolate_curve(points, 30, "pump_efficiency"), 0.70)

    def test_no_curve_extrapolation(self):
        points = [
            {"flow_m3_h": 20, "head_m": 55},
            {"flow_m3_h": 40, "head_m": 44},
        ]
        self.assertIsNone(interpolate_curve(points, 50, "head_m"))

    def test_duplicate_flow_is_rejected(self):
        points = [{"flow_m3_h": 20, "head_m": 55}, {"flow_m3_h": 20, "head_m": 50}]
        with self.assertRaises(ValueError):
            validate_pump_curve(points)

    def test_efficiency_out_of_range_is_rejected(self):
        points = [
            {"flow_m3_h": 20, "head_m": 55, "pump_efficiency": 1.1},
            {"flow_m3_h": 40, "head_m": 44},
        ]
        with self.assertRaises(ValueError):
            validate_pump_curve(points)


if __name__ == "__main__":
    unittest.main()
