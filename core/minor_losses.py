"""K-based fitting losses and measured equipment differential-pressure losses."""
from __future__ import annotations
import math

GRAVITY_M_S2 = 9.80665

def calculate_minor_loss(*, total_k: float, velocity_m_s: float) -> float:
    if not math.isfinite(total_k) or not math.isfinite(velocity_m_s):
        raise ValueError("Inputs must be finite.")
    if total_k < 0 or velocity_m_s < 0:
        raise ValueError("K and velocity cannot be negative.")
    return total_k * velocity_m_s**2 / (2.0 * GRAVITY_M_S2)

def pressure_drop_to_head(*, pressure_drop_bar: float, density_kg_m3: float) -> float:
    if not math.isfinite(pressure_drop_bar) or not math.isfinite(density_kg_m3):
        raise ValueError("Inputs must be finite.")
    if pressure_drop_bar < 0 or density_kg_m3 <= 0:
        raise ValueError("Pressure drop cannot be negative and density must be positive.")
    return pressure_drop_bar * 100000.0 / (density_kg_m3 * GRAVITY_M_S2)
