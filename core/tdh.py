"""Total Dynamic Head calculation for a single steady-state flow path."""
from __future__ import annotations
import math
from .friction import darcy_friction_factor
from .minor_losses import calculate_minor_loss, pressure_drop_to_head

GRAVITY_M_S2 = 9.80665

def calculate_tdh(*, flow_m3_h: float, pipe_length_m: float, internal_diameter_mm: float,
                  roughness_mm: float, density_kg_m3: float, kinematic_viscosity_m2_s: float,
                  total_fitting_k: float = 0.0, equipment_pressure_drop_bar: float = 0.0,
                  elevation_difference_m: float = 0.0, pressure_start_kpa: float = 0.0,
                  pressure_end_kpa: float = 0.0, velocity_start_m_s: float = 0.0,
                  velocity_end_m_s: float = 0.0) -> dict:
    vals = (flow_m3_h, pipe_length_m, internal_diameter_mm, roughness_mm, density_kg_m3,
            kinematic_viscosity_m2_s, total_fitting_k, equipment_pressure_drop_bar,
            elevation_difference_m, pressure_start_kpa, pressure_end_kpa,
            velocity_start_m_s, velocity_end_m_s)
    if any(not math.isfinite(float(v)) for v in vals):
        raise ValueError("All inputs must be finite.")
    if flow_m3_h <= 0 or pipe_length_m < 0 or internal_diameter_mm <= 0:
        raise ValueError("Flow and diameter must be positive; pipe length cannot be negative.")
    if roughness_mm < 0 or density_kg_m3 <= 0 or kinematic_viscosity_m2_s <= 0:
        raise ValueError("Roughness cannot be negative; fluid properties must be positive.")
    if total_fitting_k < 0 or equipment_pressure_drop_bar < 0:
        raise ValueError("Fitting K and equipment pressure drop cannot be negative.")
    if velocity_start_m_s < 0 or velocity_end_m_s < 0:
        raise ValueError("Boundary velocities cannot be negative.")

    diameter_m = internal_diameter_mm / 1000.0
    flow_m3_s = flow_m3_h / 3600.0
    area_m2 = math.pi * diameter_m**2 / 4.0
    velocity_m_s = flow_m3_s / area_m2
    reynolds = velocity_m_s * diameter_m / kinematic_viscosity_m2_s
    relative_roughness = (roughness_mm / 1000.0) / diameter_m
    friction_factor, warning = darcy_friction_factor(reynolds, relative_roughness)
    velocity_head = velocity_m_s**2 / (2.0 * GRAVITY_M_S2)
    major = friction_factor * (pipe_length_m / diameter_m) * velocity_head
    minor = calculate_minor_loss(total_k=total_fitting_k, velocity_m_s=velocity_m_s)
    equipment = pressure_drop_to_head(pressure_drop_bar=equipment_pressure_drop_bar,
                                      density_kg_m3=density_kg_m3)
    pressure_head = (pressure_end_kpa - pressure_start_kpa) * 1000.0 / (density_kg_m3 * GRAVITY_M_S2)
    velocity_head_difference = (velocity_end_m_s**2 - velocity_start_m_s**2) / (2.0 * GRAVITY_M_S2)
    total = elevation_difference_m + pressure_head + velocity_head_difference + major + minor + equipment
    regime = "Laminar" if reynolds < 2300 else ("Transitional" if reynolds <= 4000 else "Turbulent")
    return {
        "flow_m3_h": flow_m3_h, "internal_diameter_mm": internal_diameter_mm,
        "pipe_velocity_m_s": velocity_m_s, "reynolds": reynolds, "flow_regime": regime,
        "darcy_friction_factor": friction_factor, "velocity_head_m": velocity_head,
        "static_head_m": elevation_difference_m, "pressure_head_m": pressure_head,
        "velocity_head_difference_m": velocity_head_difference, "major_loss_m": major,
        "fitting_loss_m": minor, "equipment_loss_m": equipment,
        "total_tdh_m": total, "friction_warning": warning,
    }
