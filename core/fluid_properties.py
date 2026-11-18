"""EC-based screening estimates for water properties.

EC alone cannot uniquely determine individual ion concentrations. This module
estimates TDS from EC using an explicit conversion factor, then estimates
density and viscosity for hydraulic screening. Optional seawater ion ratios
are reported ONLY when the user explicitly selects the natural-seawater
composition profile; they are not inferred for arbitrary groundwater/brine.
"""
from dataclasses import dataclass
import math

_FRESHWATER_TABLE = {
    0.0: (999.84, 1.792e-3), 5.0: (999.97, 1.519e-3),
    10.0: (999.70, 1.307e-3), 15.0: (999.10, 1.138e-3),
    20.0: (998.21, 1.002e-3), 25.0: (997.05, 0.890e-3),
    30.0: (995.65, 0.798e-3), 40.0: (992.22, 0.653e-3),
    50.0: (988.04, 0.547e-3), 60.0: (983.20, 0.467e-3),
    80.0: (971.80, 0.355e-3), 100.0: (958.35, 0.282e-3),
}

# Approximate standard natural-seawater composition at salinity about 35 g/kg.
_SEAWATER_IONS_MG_L_AT_35 = {
    "chloride": 19354.0, "sodium": 10770.0, "sulfate": 2712.0,
    "magnesium": 1290.0, "calcium": 412.0, "potassium": 399.0,
    "bicarbonate": 142.0, "bromide": 67.0, "boron": 4.5,
    "strontium": 8.0,
}


@dataclass(frozen=True)
class FluidProperties:
    fluid_type: str
    temperature_c: float
    ec_ms_cm: float
    ec_reference_temperature_c: float
    tds_factor: float
    tds_mg_l: float
    density_kg_m3: float
    dynamic_viscosity_pa_s: float
    kinematic_viscosity_m2_s: float
    estimated_ions_mg_l: dict[str, float] | None
    estimate_level: str
    warnings: tuple[str, ...]

    def as_dict(self) -> dict:
        return {
            "fluid_type": self.fluid_type,
            "temperature_c": self.temperature_c,
            "ec_ms_cm": self.ec_ms_cm,
            "ec_reference_temperature_c": self.ec_reference_temperature_c,
            "tds_factor": self.tds_factor,
            "tds_mg_l": self.tds_mg_l,
            "density_kg_m3": self.density_kg_m3,
            "dynamic_viscosity_pa_s": self.dynamic_viscosity_pa_s,
            "kinematic_viscosity_m2_s": self.kinematic_viscosity_m2_s,
            "estimated_ions_mg_l": self.estimated_ions_mg_l,
            "estimate_level": self.estimate_level,
            "warnings": list(self.warnings),
        }


def _freshwater_base(temperature_c: float) -> tuple[float, float]:
    if not math.isfinite(temperature_c) or not 0.0 <= temperature_c <= 100.0:
        raise ValueError("Temperature must be between 0 and 100 °C.")
    points = sorted(_FRESHWATER_TABLE)
    for t in points:
        if temperature_c == t:
            return _FRESHWATER_TABLE[t]
    for lo, hi in zip(points, points[1:]):
        if lo <= temperature_c <= hi:
            f = (temperature_c - lo) / (hi - lo)
            rho1, mu1 = _FRESHWATER_TABLE[lo]
            rho2, mu2 = _FRESHWATER_TABLE[hi]
            return rho1 + f * (rho2-rho1), mu1 + f * (mu2-mu1)
    raise ValueError("Temperature is outside the supported range.")


def estimate_from_ec(
    ec_ms_cm: float,
    temperature_c: float = 25.0,
    *,
    tds_factor: float = 0.65,
    composition_profile: str = "generic",
    ec_reference_temperature_c: float = 25.0,
) -> FluidProperties:
    """Estimate TDS, density and viscosity from temperature-compensated EC.

    EC must already be compensated to ec_reference_temperature_c (normally
    25 °C). TDS ≈ EC(µS/cm) × tds_factor. Density and viscosity are approximate
    screening correlations; concentrated brine needs validated properties.
    """
    vals = (ec_ms_cm, temperature_c, tds_factor, ec_reference_temperature_c)
    if any(not math.isfinite(float(v)) for v in vals):
        raise ValueError("All inputs must be finite numbers.")
    if ec_ms_cm < 0:
        raise ValueError("EC cannot be negative.")
    if not 0.0 < tds_factor <= 1.2:
        raise ValueError("TDS factor must be greater than 0 and at most 1.2.")
    if not 0.0 <= ec_reference_temperature_c <= 100.0:
        raise ValueError("EC reference temperature must be between 0 and 100 °C.")
    if composition_profile not in {"generic", "natural_seawater"}:
        raise ValueError("composition_profile must be 'generic' or 'natural_seawater'.")

    tds_mg_l = ec_ms_cm * 1000.0 * tds_factor
    tds_g_l = tds_mg_l / 1000.0
    rho_water, mu_water = _freshwater_base(float(temperature_c))

    # Engineering screening corrections, not a universal electrolyte model.
    density = rho_water + 0.70 * tds_g_l
    dynamic_viscosity = mu_water * (1.0 + 0.0022 * tds_g_l)
    kinematic_viscosity = dynamic_viscosity / density

    warnings = [
        "EC-to-TDS factor depends on ionic composition; 0.65 is a default estimate, not universal.",
        "Density and viscosity are approximate screening estimates, not a validated equation of state.",
        "EC must be temperature-compensated to the stated reference temperature (normally 25 °C).",
        "Individual ion concentrations cannot be uniquely calculated from EC alone.",
    ]

    ions = None
    estimate_level = "EC/TDS-based screening estimate"
    if composition_profile == "natural_seawater":
        scale = tds_mg_l / 35000.0
        ions = {name: value * scale for name, value in _SEAWATER_IONS_MG_L_AT_35.items()}
        ions["calcium_hardness_as_CaCO3"] = ions["calcium"] * 2.497
        ions["bicarbonate_alkalinity_as_CaCO3"] = ions["bicarbonate"] * (50.0 / 61.0)
        estimate_level = "EC/TDS plus assumed natural-seawater ionic ratios"
        warnings.extend([
            "Ion values assume standard natural seawater ratios; do not apply to groundwater or RO concentrate without laboratory confirmation.",
            "Iron is not estimated because it is a trace/variable constituent and cannot be inferred from EC.",
            "Lime is not a dissolved ion; calcium hardness and alkalinity are reported as CaCO3 equivalents only under the seawater-profile assumption.",
        ])

    if ec_ms_cm > 70.0:
        warnings.append("EC exceeds 70 mS/cm; concentrated-brine behaviour may fall outside these screening correlations.")

    return FluidProperties(
        fluid_type="water" if composition_profile == "generic" else "natural_seawater_profile",
        temperature_c=float(temperature_c),
        ec_ms_cm=float(ec_ms_cm),
        ec_reference_temperature_c=float(ec_reference_temperature_c),
        tds_factor=float(tds_factor),
        tds_mg_l=float(tds_mg_l),
        density_kg_m3=float(density),
        dynamic_viscosity_pa_s=float(dynamic_viscosity),
        kinematic_viscosity_m2_s=float(kinematic_viscosity),
        estimated_ions_mg_l=ions,
        estimate_level=estimate_level,
        warnings=tuple(warnings),
    )
