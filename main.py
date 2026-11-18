"""Initial command-line entry point for Pump TDH Calculator."""
from core.fluid_properties import get_fluid_properties


def main() -> None:
    print("=" * 58)
    print("PUMP TDH CALCULATOR")
    print("Initial module: Fluid Properties")
    print("=" * 58)
    print("1. Freshwater")
    print("2. Natural seawater (reference: 25 °C, 35 g/kg)")
    print("3. Custom fluid properties")

    choice = input("Select fluid [1-3]: ").strip()

    try:
        if choice == "1":
            temperature = float(input("Water temperature (°C) [20]: ") or "20")
            props = get_fluid_properties("freshwater", temperature_c=temperature)
        elif choice == "2":
            props = get_fluid_properties("seawater", temperature_c=25.0, salinity_g_kg=35.0)
        elif choice == "3":
            rho = float(input("Density (kg/m³): "))
            mu = float(input("Dynamic viscosity (Pa·s): "))
            temperature = float(input("Temperature (°C): "))
            props = get_fluid_properties(
                "custom",
                temperature_c=temperature,
                density_kg_m3=rho,
                dynamic_viscosity_pa_s=mu,
            )
        else:
            print("Invalid selection.")
            return
    except ValueError as exc:
        print(f"Input error: {exc}")
        return

    print("\nFLUID PROPERTIES")
    print(f"Fluid type                 : {props.fluid_type}")
    print(f"Temperature                : {props.temperature_c:.2f} °C")
    print(f"Density                    : {props.density_kg_m3:.4f} kg/m³")
    print(f"Dynamic viscosity          : {props.dynamic_viscosity_pa_s:.8g} Pa·s")
    print(f"Kinematic viscosity        : {props.kinematic_viscosity_m2_s:.8g} m²/s")
    if props.salinity_g_kg is not None:
        print(f"Salinity                   : {props.salinity_g_kg:.3f} g/kg")
    print(f"Note                       : {props.source_note}")


if __name__ == "__main__":
    main()
