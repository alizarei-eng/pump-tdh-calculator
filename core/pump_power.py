"""Pump and motor power calculations plus pump-curve interpolation."""
from __future__ import annotations

import math

GRAVITY_M_S2 = 9.80665


def interpolate_curve(points: list[dict], flow_m3_h: float, key: str) -> float | None:
    """Linearly interpolate a curve column; never extrapolate beyond supplied points."""
    usable = sorted(
        (float(p["flow_m3_h"]), float(p[key]))
        for p in points if p.get(key) is not None
    )
    if len(usable) < 2:
        return None
    if flow_m3_h < usable[0][0] or flow_m3_h > usable[-1][0]:
        return None
    for (q1, y1), (q2, y2) in zip(usable, usable[1:]):
        if q1 <= flow_m3_h <= q2:
            if q2 == q1:
                raise ValueError("Pump-curve flow values must be unique.")
            ratio = (flow_m3_h - q1) / (q2 - q1)
            return y1 + ratio * (y2 - y1)
    return None


def validate_pump_curve(points: list[dict]) -> None:
    if len(points) < 2:
        raise ValueError("At least two pump-curve points are required.")
    flows = [float(p["flow_m3_h"]) for p in points]
    if any(not math.isfinite(q) or q <= 0 for q in flows):
        raise ValueError("Pump-curve flow values must be finite and positive.")
    if len(set(flows)) != len(flows):
        raise ValueError("Pump-curve flow values must be unique.")
    for point in points:
        head = float(point["head_m"])
        if not math.isfinite(head) or head < 0:
            raise ValueError("Pump-curve head values must be finite and non-negative.")
        eta = point.get("pump_efficiency")
        if eta is not None and (not math.isfinite(float(eta)) or not 0 < float(eta) <= 1):
            raise ValueError("Pump efficiency values must be greater than 0 and at most 1.")
        power = point.get("shaft_power_kw")
        if power is not None and (not math.isfinite(float(power)) or float(power) <= 0):
            raise ValueError("Shaft power values must be finite and positive.")


def calculate_power(
    *,
    flow_m3_h: float,
    required_tdh_m: float,
    density_kg_m3: float,
    pump_efficiency: float = 1.0,
    motor_efficiency: float = 1.0,
    shaft_power_kw: float | None = None,
) -> dict:
    """Calculate hydraulic, shaft and electrical input power.

    If shaft power is supplied from a manufacturer curve, it is used directly.
    Otherwise shaft power is calculated from pump efficiency. Efficiencies are
    fractions (0..1), not percentages.
    """
    values = (flow_m3_h, required_tdh_m, density_kg_m3,
              pump_efficiency, motor_efficiency)
    if any(not math.isfinite(float(v)) for v in values):
        raise ValueError("Power inputs must be finite.")
    if flow_m3_h <= 0 or required_tdh_m < 0 or density_kg_m3 <= 0:
        raise ValueError("Flow and density must be positive; TDH cannot be negative.")
    if not 0 < pump_efficiency <= 1 or not 0 < motor_efficiency <= 1:
        raise ValueError("Efficiencies must be greater than 0 and at most 1.")
    hydraulic_kw = density_kg_m3 * GRAVITY_M_S2 * (flow_m3_h / 3600.0) * required_tdh_m / 1000.0
    if shaft_power_kw is not None:
        if not math.isfinite(float(shaft_power_kw)) or shaft_power_kw <= 0:
            raise ValueError("Shaft power must be finite and positive.")
        shaft_kw = float(shaft_power_kw)
        implied_pump_efficiency = hydraulic_kw / shaft_kw if shaft_kw else None
        consistency_warning = None
        if implied_pump_efficiency is not None and implied_pump_efficiency > 1.0 + 1e-9:
            consistency_warning = (
                "Manufacturer shaft power is below the hydraulic power required by "
                "the system; check the curve data, flow, head and units."
            )
        elif abs(implied_pump_efficiency - pump_efficiency) > 0.05:
            consistency_warning = (
                "Interpolated shaft power and pump efficiency differ by more than "
                "5 percentage points; verify the manufacturer data."
            )
    else:
        shaft_kw = hydraulic_kw / pump_efficiency
        implied_pump_efficiency = pump_efficiency
        consistency_warning = None
    electric_kw = shaft_kw / motor_efficiency
    return {
        "hydraulic_power_kw": hydraulic_kw,
        "shaft_power_kw": shaft_kw,
        "electric_power_kw": electric_kw,
        "pump_efficiency": pump_efficiency,
        "motor_efficiency": motor_efficiency,
        "implied_pump_efficiency": implied_pump_efficiency,
        "consistency_warning": consistency_warning,
    }
