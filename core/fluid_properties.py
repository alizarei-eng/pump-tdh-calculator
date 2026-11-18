"""Fluid-property utilities for water in hydraulic calculations.

Reference properties are defined at 20 degC for freshwater and 25 degC
for natural seawater. For other conditions, this first version uses
transparent engineering approximations; use laboratory/vendor data for
final design when the fluid is concentrated brine or chemically treated.
"""
from dataclasses import dataclass
from typing import Literal

FluidType = Literal["freshwater", "seawater", "custom"]


@dataclass(frozen=True)
class FluidProperties:
    fluid_type: str
    temperature_c: float
    density_kg_m3: float
    dynamic_viscosity_pa_s: float
    kinematic_viscosity_m2_s: float
    salinity_g_kg: float | None = None
    source_note: str = ""

    def as_dict(self) -> dict:
        return {
            "fluid_type": self.fluid_type,
            "temperature_c": self.temperature_c,
            "density_kg_m3": self.density_kg_m3,
            "dynamic_viscosity_pa_s": self.dynamic_viscosity_pa_s,
            "kinematic_viscosity_m2_s": self.kinematic_viscosity_m2_s,
            "salinity_g_kg": self.salinity_g_kg,
            "source_note": self.source_note,
        }


# Approximate pure-water values at atmospheric pressure.
# Interpolation is linear between tabulated temperatures.
_FRESHWATER_TABLE = {
    0.0:  (999.84, 1.792e-3),
    5.0:  (999.97, 1.519e-3),
    10.0: (999.70, 1.307e-3),
    15.0: (999.10, 1.138e-3),
    20.0: (998.21, 1.002e-3),
    25.0: (997.05, 0.890e-3),
    30.0: (995.65, 0.798e-3),
    40.0: (992.22, 0.653e-3),
    50.0: (988.04, 0.547e-3),
    60.0: (983.20, 0.467e-3),
    80.0: (971.80, 0.355e-3),
    100.0:(958.35, 0.282e-3),
}

# Natural seawater reference near salinity 35 g/kg and atmospheric pressure.
# Values are engineering reference values, not a complete seawater equation of state.
_SEAWATER_REFERENCE = {
    "temperature_c": 25.0,
    "salinity_g_kg": 35.0,
    "density_kg_m3": 1023.3,
    "dynamic_viscosity_pa_s": 0.9591e-3,
}


def _interpolate_freshwater(temperature_c: float) -> tuple[float, float]:
    temps = sorted(_FRESHWATER_TABLE)
    if not temps[0] <= temperature_c <= temps[-1]:
        raise ValueError(
            f"Freshwater temperature must be between {temps[0]} and {temps[-1]} °C."
        )
    if temperature_c in _FRESHWATER_TABLE:
        return _FRESHWATER_TABLE[temperature_c]
    for lower, upper in zip(temps, temps[1:]):
        if lower <= temperature_c <= upper:
            fraction = (temperature_c - lower) / (upper - lower)
            rho1, mu1 = _FRESHWATER_TABLE[lower]
            rho2, mu2 = _FRESHWATER_TABLE[upper]
            return (
                rho1 + fraction * (rho2 - rho1),
                mu1 + fraction * (mu2 - mu1),
            )
    raise RuntimeError("Could not interpolate freshwater properties.")


def get_fluid_properties(
    fluid_type: FluidType = "freshwater",
    temperature_c: float = 20.0,
    salinity_g_kg: float | None = None,
    density_kg_m3: float | None = None,
    dynamic_viscosity_pa_s: float | None = None,
) -> FluidProperties:
    """Return density and viscosity for freshwater, seawater, or custom fluid.

    For seawater, this initial version supports the reference condition
    (25 °C, 35 g/kg) only. Other seawater conditions should use measured or
    validated property data and can be passed through the custom option.
    """
    if density_kg_m3 is not None or dynamic_viscosity_pa_s is not None:
        if density_kg_m3 is None or dynamic_viscosity_pa_s is None:
            raise ValueError("Custom fluid requires both density and dynamic viscosity.")
        fluid_type = "custom"
    if temperature_c <= -273.15:
        raise ValueError("Temperature must be above absolute zero.")

    if fluid_type == "freshwater":
        rho, mu = _interpolate_freshwater(float(temperature_c))
        note = "Approximate pure-water table at atmospheric pressure; linear interpolation."
        salinity = 0.0
    elif fluid_type == "seawater":
        salinity = 35.0 if salinity_g_kg is None else float(salinity_g_kg)
        if abs(float(temperature_c) - 25.0) > 1e-9 or abs(salinity - 35.0) > 1e-9:
            raise ValueError(
                "This initial seawater model is calibrated only for 25 °C and 35 g/kg. "
                "Use measured properties with fluid_type='custom' for other conditions."
            )
        rho = _SEAWATER_REFERENCE["density_kg_m3"]
        mu = _SEAWATER_REFERENCE["dynamic_viscosity_pa_s"]
        note = "Natural seawater reference: 25 °C, 35 g/kg, approximately atmospheric pressure."
    elif fluid_type == "custom":
        if density_kg_m3 is None or dynamic_viscosity_pa_s is None:
            raise ValueError("Custom fluid requires density and dynamic viscosity.")
        rho = float(density_kg_m3)
        mu = float(dynamic_viscosity_pa_s)
        salinity = salinity_g_kg
        note = "User-supplied properties."
    else:
        raise ValueError("fluid_type must be 'freshwater', 'seawater', or 'custom'.")

    if rho <= 0 or mu <= 0:
        raise ValueError("Density and dynamic viscosity must be positive.")

    nu = mu / rho
    return FluidProperties(
        fluid_type=str(fluid_type),
        temperature_c=float(temperature_c),
        density_kg_m3=float(rho),
        dynamic_viscosity_pa_s=float(mu),
        kinematic_viscosity_m2_s=float(nu),
        salinity_g_kg=salinity,
        source_note=note,
    )
