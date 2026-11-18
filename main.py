"""Initial command-line entry point for Pump TDH Calculator."""
from core.fluid_properties import estimate_from_ec
from core.elevation import calculate_static_head, calculate_static_head_from_difference


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

    try:
        fluid = estimate_from_ec(
            ec_ms_cm=ec,
            temperature_c=temperature,
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

    print("\nGROUP 4: ELEVATION / STATIC HEAD")
    print("Choose elevation input method:")
    print("  1) Enter elevation difference directly (destination - start)")
    print("  2) Enter start and destination elevations")
    while True:
        method = input("Enter 1 or 2: ").strip()
        if method in ("1", "2"):
            break
        print("Invalid selection. Enter 1 or 2.")

    def read_signed_finite_float(prompt: str) -> float:
        while True:
            try:
                value = float(input(prompt).strip().replace(",", "."))
                if value == value and value not in (float("inf"), float("-inf")):
                    return value
            except ValueError:
                pass
            print("Enter a valid finite number.")

    if method == "1":
        delta_z = calculate_static_head_from_difference(
            read_signed_finite_float("Elevation difference Δz (m; positive uphill, negative downhill): ")
        )
        method_label = "Direct elevation difference"
    else:
        print("Enter both elevations relative to the SAME vertical datum.")
        z1 = read_signed_finite_float("Start elevation z1 (m): ")
        z2 = read_signed_finite_float("Destination elevation z2 (m): ")
        delta_z = calculate_static_head(elevation_start_m=z1, elevation_end_m=z2)
        method_label = "Start/end elevations"

    print("\nSTATIC HEAD RESULT")
    print(f"Input method       : {method_label}")
    print(f"Static head (Δz)   : {delta_z:+.3f} m")
    if delta_z > 0:
        print("Elevation effect   : Uphill; adds to required pump head.")
    elif delta_z < 0:
        print("Elevation effect   : Downhill; assists flow and reduces required pump head.")
    else:
        print("Elevation effect   : No net elevation difference.")
    print("Note: this is only the elevation term, not the complete pump TDH.")


if __name__ == "__main__":
    main()
