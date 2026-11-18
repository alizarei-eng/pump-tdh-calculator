import unittest
from core.minor_losses import calculate_minor_loss, pressure_drop_to_head
from core.tdh import calculate_tdh
from core.pipe_database import available_grades, available_sdrs, available_ods, get_pe_pipe, get_material_roughness

class TestPipeDatabase(unittest.TestCase):
    def test_pe100_sdr11_od110_geometry(self):
        pipe = get_pe_pipe("PE100", 11, 110)
        self.assertAlmostEqual(pipe["internal_diameter_mm"], 90.0, places=1)
        self.assertAlmostEqual(pipe["wall_thickness_mm"], 10.0, places=1)
    def test_available_pipe_catalogue_options(self):
        self.assertIn("PE100", available_grades())
        self.assertIn(11.0, available_sdrs("PE100"))
        self.assertIn(110.0, available_ods("PE100", 11))
    def test_hdpe_roughness_is_loaded(self):
        roughness, name, label = get_material_roughness(1)
        self.assertAlmostEqual(roughness, 0.0015)
        self.assertEqual(name, "HDPE")

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
