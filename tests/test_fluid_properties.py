import unittest

from core.fluid_properties import get_fluid_properties


class TestFluidProperties(unittest.TestCase):
    def test_freshwater_at_20_c(self):
        water = get_fluid_properties("freshwater", temperature_c=20)
        self.assertAlmostEqual(water.density_kg_m3, 998.21, places=2)
        self.assertAlmostEqual(water.dynamic_viscosity_pa_s, 1.002e-3, places=7)
        self.assertAlmostEqual(
            water.kinematic_viscosity_m2_s,
            water.dynamic_viscosity_pa_s / water.density_kg_m3,
        )

    def test_freshwater_interpolation(self):
        water = get_fluid_properties("freshwater", temperature_c=22.5)
        self.assertGreater(water.density_kg_m3, 997.0)
        self.assertLess(water.density_kg_m3, 998.3)

    def test_seawater_reference(self):
        water = get_fluid_properties("seawater", temperature_c=25, salinity_g_kg=35)
        self.assertAlmostEqual(water.density_kg_m3, 1023.3, places=1)
        self.assertAlmostEqual(water.dynamic_viscosity_pa_s, 0.9591e-3, places=7)

    def test_seawater_rejects_unsupported_conditions(self):
        with self.assertRaises(ValueError):
            get_fluid_properties("seawater", temperature_c=20, salinity_g_kg=35)

    def test_custom_properties(self):
        fluid = get_fluid_properties(
            "custom", temperature_c=30,
            density_kg_m3=1000, dynamic_viscosity_pa_s=0.001
        )
        self.assertAlmostEqual(fluid.kinematic_viscosity_m2_s, 1e-6)

    def test_invalid_custom_properties(self):
        with self.assertRaises(ValueError):
            get_fluid_properties("custom", density_kg_m3=1000)


if __name__ == "__main__":
    unittest.main()
