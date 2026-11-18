"""Interactive CLI for fluid properties and complete steady-state pump TDH."""
import json
from pathlib import Path
from core.fluid_properties import estimate_from_ec
from core.elevation import calculate_static_head, calculate_static_head_from_difference
from core.tdh import calculate_tdh

ROOT = Path(__file__).resolve().parent

def load_json(name):
    with (ROOT / "databases" / name).open(encoding="utf-8") as f:
        return json.load(f)

def read_number(prompt, *, allow_negative=False, minimum=None):
    while True:
        try:
            value = float(input(prompt).strip().replace(",", "."))
            if value != value or value in (float("inf"), float("-inf")):
                raise ValueError
            if not allow_negative and value < 0:
                raise ValueError
            if minimum is not None and value < minimum:
                raise ValueError
            return value
        except ValueError:
            print("Enter a valid finite number within the permitted range.")

def collect_static_head():
    print("\nGROUP: ELEVATION / STATIC HEAD")
    print("1. Enter elevation difference Δz directly")
    print("2. Enter start and destination elevations")
    while True:
        choice = input("Select method [1-2]: ").strip()
        if choice in ("1", "2"):
            break
        print("Choose 1 or 2.")
    if choice == "1":
        return calculate_static_head_from_difference(
            read_number("Δz (m; positive uphill, negative downhill): ", allow_negative=True))
    z1 = read_number("Start elevation z1 (m): ", allow_negative=True)
    z2 = read_number("Destination elevation z2 (m): ", allow_negative=True)
    return calculate_static_head(elevation_start_m=z1, elevation_end_m=z2)

def collect_fittings(fittings):
    print("\nGROUP: FITTINGS AND VALVES")
    for item in fittings:
        print(f"{item['id']}. {item['name']} (K={item['k']:g})")
    print("Enter 0 when finished.")
    total_k = 0.0
    while True:
        try:
            selected_id = int(input("Fitting number: ").strip())
        except ValueError:
            print("Enter a listed number.")
            continue
        if selected_id == 0:
            return total_k
        item = next((x for x in fittings if x["id"] == selected_id), None)
        if item is None:
            print("Invalid fitting number.")
            continue
        quantity = int(read_number("Quantity: ", minimum=1))
        add = item["k"] * quantity
        total_k += add
        print(f"Added K={add:g}; total K={total_k:g}")

def collect_equipment_drop(equipment):
    print("\nGROUP: EQUIPMENT PRESSURE LOSSES")
    print("Use actual measured/manufacturer differential pressure; no universal K is assumed.")
    for item in equipment:
        print(f"{item['id']}. {item['name']}")
    print("Enter 0 when finished.")
    total_bar = 0.0
    while True:
        try:
            selected_id = int(input("Equipment number: ").strip())
        except ValueError:
            print("Enter a listed number.")
            continue
        if selected_id == 0:
            return total_bar
        item = next((x for x in equipment if x["id"] == selected_id), None)
        if item is None:
            print("Invalid equipment number.")
            continue
        dp = read_number(f"Pressure drop across {item['name']} (bar): ")
        total_bar += dp
        print(f"Added {dp:.4f} bar; total equipment drop={total_bar:.4f} bar")

def main():
    print("=" * 68)
    print("PUMP TOTAL DYNAMIC HEAD (TDH) CALCULATOR")
    print("Single steady-state flow path | SI units")
    print("=" * 68)

    print("\nGROUP: FLUID PROPERTIES")
    print("1. Generic water / groundwater / brackish water")
    print("2. Natural seawater ionic-ratio screening profile")
    profile_choice = input("Select profile [1-2]: ").strip()
    profile = "natural_seawater" if profile_choice == "2" else "generic"
    ec = read_number("EC (mS/cm, compensated to 25 °C): ")
    temp = read_number("Water temperature (°C) [25]: ") if input("Use 25 °C? [Y/n]: ").strip().lower() == "n" else 25.0
    try:
        fluid = estimate_from_ec(ec_ms_cm=ec, temperature_c=temp,
                                 composition_profile=profile, ec_reference_temperature_c=25.0)
    except ValueError as exc:
        print(f"Fluid input error: {exc}")
        return

    delta_z = collect_static_head()
    print("\nGROUP: PIPE")
    flow = read_number("Flow rate (m³/h): ", minimum=0.000001)
    length = read_number("Total straight pipe length (m): ")
    diameter = read_number("Pipe internal diameter (mm): ", minimum=0.000001)
    roughness = read_number("Absolute roughness (mm): ")
    fittings = collect_fittings(load_json("fittings.json")["fittings"])
    equipment_dp = collect_equipment_drop(load_json("equipment_templates.json")["equipment"])

    print("\nGROUP: BOUNDARY CONDITIONS")
    print("Enter gauge pressures at start/end. For two open tanks, enter 0 for both.")
    p1 = read_number("Start pressure (kPa gauge): ", allow_negative=True)
    p2 = read_number("End pressure (kPa gauge): ", allow_negative=True)
    print("For two large tank free surfaces, use zero for both boundary velocities.")
    v1 = read_number("Start velocity (m/s) [0]: ") if input("Enter start velocity? [y/N]: ").strip().lower() == "y" else 0.0
    v2 = read_number("End velocity (m/s) [0]: ") if input("Enter end velocity? [y/N]: ").strip().lower() == "y" else 0.0

    try:
        result = calculate_tdh(
            flow_m3_h=flow, pipe_length_m=length, internal_diameter_mm=diameter,
            roughness_mm=roughness, density_kg_m3=fluid.density_kg_m3,
            kinematic_viscosity_m2_s=fluid.kinematic_viscosity_m2_s,
            total_fitting_k=fittings, equipment_pressure_drop_bar=equipment_dp,
            elevation_difference_m=delta_z, pressure_start_kpa=p1, pressure_end_kpa=p2,
            velocity_start_m_s=v1, velocity_end_m_s=v2)
    except ValueError as exc:
        print(f"Calculation input error: {exc}")
        return

    print("\n" + "=" * 68)
    print("FLUID PROPERTY ESTIMATES")
    print(f"Profile                         : {fluid.fluid_type}")
    print(f"EC / Temperature                : {fluid.ec_ms_cm:.3f} mS/cm / {fluid.temperature_c:.2f} °C")
    print(f"Estimated TDS                   : {fluid.tds_mg_l:.1f} mg/L")
    print(f"Estimated density               : {fluid.density_kg_m3:.3f} kg/m³")
    print(f"Estimated kinematic viscosity   : {fluid.kinematic_viscosity_m2_s:.6g} m²/s")
    print("\nHYDRAULIC RESULTS")
    print(f"Pipe velocity                   : {result['pipe_velocity_m_s']:.3f} m/s")
    print(f"Reynolds number                 : {result['reynolds']:.0f}")
    print(f"Flow regime                     : {result['flow_regime']}")
    print(f"Darcy friction factor           : {result['darcy_friction_factor']:.6f}")
    print("-" * 68)
    print(f"Static head Δz                  : {result['static_head_m']:+.4f} m")
    print(f"Pressure head difference        : {result['pressure_head_m']:+.4f} m")
    print(f"Velocity head difference        : {result['velocity_head_difference_m']:+.4f} m")
    print(f"Major pipe loss                 : {result['major_loss_m']:.4f} m")
    print(f"Fittings / valves loss          : {result['fitting_loss_m']:.4f} m")
    print(f"Equipment pressure loss         : {result['equipment_loss_m']:.4f} m")
    print("-" * 68)
    print(f"REQUIRED PUMP TDH               : {result['total_tdh_m']:.4f} m")
    if result["total_tdh_m"] < 0:
        print("NOTE: Negative calculated TDH indicates the boundary conditions/gravity head may drive the flow; verify system definition.")
    if result["friction_warning"]:
        print(f"WARNING: {result['friction_warning']}")
    print("\nFluid-property limitations:")
    for warning in fluid.warnings:
        print(f"- {warning}")
    print("=" * 68)

if __name__ == "__main__":
    main()
