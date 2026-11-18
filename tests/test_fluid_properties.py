import unittest
from core.fluid_properties import estimate_from_ec


class TestECFluidProperties(unittest.TestCase):
    def test_tds_from_ec(self):
        water = estimate_from_ec(10.0, 25.0)
        self.assertAlmostEqual(water.tds_mg_l, 6500.0)
        self.assertGreater(water.density_kg_m3, 997.0)
        self.assertGreater(water.dynamic_viscosity_pa_s, 0.00089)

    def test_kinematic_viscosity_identity(self):
        water = estimate_from_ec(2.0, 20.0)
        self.assertAlmostEqual(
            water.kinematic_viscosity_m2_s,
            water.dynamic_viscosity_pa_s / water.density_kg_m3,
        )

    def test_generic_profile_does_not_invent_ions(self):
        water = estimate_from_ec(3.0, 25.0)
        self.assertIsNone(water.estimated_ions_mg_l)

    def test_seawater_profile_reports_assumed_ions(self):
        water = estimate_from_ec(53.0, 25.0, composition_profile="natural_seawater")
        self.assertIn("sodium", water.estimated_ions_mg_l)
        self.assertIn("calcium_hardness_as_CaCO3", water.estimated_ions_mg_l)
        self.assertTrue(any("Iron is not estimated" in item for item in water.warnings))

    def test_rejects_invalid_values(self):
        with self.assertRaises(ValueError):
            estimate_from_ec(-1.0)
        with self.assertRaises(ValueError):
            estimate_from_ec(1.0, 110.0)


if __name__ == "__main__":
    unittest.main()
