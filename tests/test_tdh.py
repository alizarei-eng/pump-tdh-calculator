import unittest
from core.minor_losses import calculate_minor_loss, pressure_drop_to_head
from core.tdh import calculate_tdh

class TestMinorLosses(unittest.TestCase):
    def test_k_loss(self):
        self.assertAlmostEqual(calculate_minor_loss(total_k=2, velocity_m_s=2), 2*4/(2*9.80665))
    def test_pressure_drop_conversion(self):
        self.assertAlmostEqual(pressure_drop_to_head(pressure_drop_bar=1, density_kg_m3=1000),
                               100000/(1000*9.80665))

class TestTDH(unittest.TestCase):
    def test_simple_horizontal_pipe(self):
        r = calculate_tdh(flow_m3_h=10, pipe_length_m=0, internal_diameter_mm=100,
            roughness_mm=0, density_kg_m3=1000, kinematic_viscosity_m2_s=1e-6,
            total_fitting_k=0, equipment_pressure_drop_bar=0)
        self.assertAlmostEqual(r["static_head_m"], 0)
        self.assertAlmostEqual(r["total_tdh_m"], 0)
    def test_tdh_adds_all_components(self):
        r = calculate_tdh(flow_m3_h=10, pipe_length_m=100, internal_diameter_mm=100,
            roughness_mm=0.01, density_kg_m3=1000, kinematic_viscosity_m2_s=1e-6,
            total_fitting_k=2, equipment_pressure_drop_bar=0.2,
            elevation_difference_m=10, pressure_start_kpa=0, pressure_end_kpa=0)
        self.assertGreater(r["total_tdh_m"], 10)
        self.assertGreater(r["major_loss_m"], 0)
        self.assertGreater(r["fitting_loss_m"], 0)
        self.assertGreater(r["equipment_loss_m"], 0)
    def test_open_tanks_pressure_terms_cancel(self):
        r = calculate_tdh(flow_m3_h=10, pipe_length_m=0, internal_diameter_mm=100,
            roughness_mm=0, density_kg_m3=1000, kinematic_viscosity_m2_s=1e-6,
            pressure_start_kpa=0, pressure_end_kpa=0)
        self.assertEqual(r["pressure_head_m"], 0)

if __name__ == "__main__":
    unittest.main()
