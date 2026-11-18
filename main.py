"""Initial command-line entry point for Pump TDH Calculator."""
from core.fluid_properties import estimate_from_ec


def read_float(prompt: str, default: float | None = None) -> float:
    while True:
        raw = input(prompt).strip().replace(",", ".")
        if not raw and default is not None:
            return default
        try:
            value = float(raw)
            if value >= 0:
                return value
        except ValueError:
            pass
        print("Enter a valid non-negative number.")


def main() -> None:
    print("=" * 60)
    print("PUMP TDH CALCULATOR")
    print("Initial module: EC-based Fluid Properties")
    print("=" * 60)
    print("1. Generic water (freshwater / groundwater / brackish water)")
    print("2. Natural seawater ionic-ratio profile")
    choice = input("Select composition profile [1-2]: ").strip()
    profile = "natural_seawater" if choice == "2" else "generic"

    ec = read_float("Electrical conductivity EC (mS/cm, compensated to 25 °C): ")
    temperature = read_float("Water temperature (°C) [25]: ", 25.0)
    factor = read_float("TDS conversion factor [0.65]: ", 0.65)

    try:
        fluid = estimate_from_ec(
            ec_ms_cm=ec,
            temperature_c=temperature,
            tds_factor=factor,
            composition_profile=profile,
            ec_reference_temperature_c=25.0,
        )
    except ValueError as exc:
        print(f"Input error: {exc}")
        return

    print("\nFLUID PROPERTY ESTIMATES")
    print(f"Profile                    : {fluid.fluid_type}")
    print(f"Temperature                : {fluid.temperature_c:.2f} °C")
    print(f"EC                         : {fluid.ec_ms_cm:.3f} mS/cm")
    print(f"Estimated TDS              : {fluid.tds_mg_l:.0f} mg/L")
    print(f"Estimated density          : {fluid.density_kg_m3:.3f} kg/m³")
    print(f"Estimated dynamic viscosity: {fluid.dynamic_viscosity_pa_s:.7g} Pa·s")
    print(f"Estimated kinematic viscosity: {fluid.kinematic_viscosity_m2_s:.7g} m²/s")
    print(f"Estimate level             : {fluid.estimate_level}")
    if fluid.estimated_ions_mg_l:
        print("\nESTIMATED ION CONCENTRATIONS (mg/L; seawater ratios assumed)")
        for ion, concentration in fluid.estimated_ions_mg_l.items():
            print(f"{ion:20s}: {concentration:10.2f}")
    print("\nLIMITATIONS / WARNINGS")
    for warning in fluid.warnings:
        print(f"- {warning}")


if __name__ == "__main__":
    main()
