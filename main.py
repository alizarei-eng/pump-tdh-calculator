"""Interactive CLI for fluid properties and complete steady-state pump TDH."""
import json
import math
from pathlib import Path
from core.fluid_properties import estimate_from_ec
from core.elevation import calculate_static_head, calculate_static_head_from_difference
from core.tdh import calculate_tdh
from core.pump_power import calculate_power, interpolate_curve, validate_pump_curve
from core.pipe_database import (available_grades, available_sdrs, available_ods,
    get_pe_pipe, get_materials, get_material_roughness, calculate_non_pe_geometry)

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

def read_choice(prompt, valid, default=None):
    while True:
        value = input(prompt).strip()
        if not value and default is not None:
            return default
        if value in valid:
            return value
        print("Invalid selection. Choose one of: " + ", ".join(valid))

def choose_from_list(title, values, formatter=str):
    print("\n" + title)
    for i, value in enumerate(values, 1):
        print(f"{i}. {formatter(value)}")
    selected = int(read_number("Enter list number: ", minimum=1))
    while selected > len(values):
        print("Number is outside the list.")
        selected = int(read_number("Enter list number: ", minimum=1))
    return values[selected - 1]

def collect_static_head():
    print("\nGROUP: ELEVATION / STATIC HEAD")
    print("1. Enter elevation difference Δz directly")
    print("2. Enter start and destination elevations")
    choice = read_choice("Select method [1-2]: ", ["1", "2"])
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
        total_k += item["k"] * quantity
        print(f"Added K={item['k']*quantity:g}; total K={total_k:g}")

def collect_equipment_drop(equipment):
    print("\nGROUP: EQUIPMENT PRESSURE LOSSES")
    print("Enter actual measured/manufacturer differential pressure.")
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

def collect_pipe():
    print("\nGROUP: PIPE DATA")
    materials = [item for item in get_materials() if item['roughness_mm'] is not None]
    material = choose_from_list("Available pipe materials (roughness is loaded automatically):",
                                materials, lambda x: x["name"])
    if material["name"] == "HDPE":
        grades = available_grades()
        grade = choose_from_list("Available PE material grades:", grades)
        sdrs = available_sdrs(grade)
        sdr = choose_from_list(f"Available SDR values for {grade}:", sdrs)
        ods = available_ods(grade, sdr)
        od = choose_from_list(f"Available outside diameters for {grade}, SDR {sdr:g} (mm):", ods)
        geometry = get_pe_pipe(grade, sdr, od)
        internal_diameter = geometry["internal_diameter_mm"]
        print(f"Catalogue wall thickness : {geometry['wall_thickness_mm']:.2f} mm")
        print(f"Calculated nominal ID    : {internal_diameter:.2f} mm")
        print(f"Reference pressure       : {geometry['nominal_pressure_bar']} bar")
        if "ratio_derived" in geometry["dimension_status"]:
            print("DIMENSION NOTE: wall value is ratio-derived; verify against controlled standard/manufacturer data.")
    else:
        od = read_number("Pipe outside diameter OD (mm): ", minimum=0.000001)
        wall = read_number("Nominal wall thickness (mm): ", minimum=0.000001)
        internal_diameter = calculate_non_pe_geometry(od, wall)
        print(f"Calculated nominal ID: {internal_diameter:.2f} mm")
    roughness, _, roughness_label = get_material_roughness(material["id"])
    print(f"Auto-loaded roughness : {roughness:g} mm ({roughness_label})")
    flow = read_number("Flow rate (m³/h): ", minimum=0.000001)
    length = read_number("Total straight pipe length (m): ")
    return flow, length, internal_diameter, roughness, geometry if material["name"] == "HDPE" else None


def read_optional_efficiency(prompt):
    while True:
        raw = input(prompt).strip().replace(",", ".")
        if not raw:
            print("No value entered: using 100% (idealized default, not measured efficiency).")
            return 1.0
        try:
            percent = float(raw)
            if not math.isfinite(percent) or not 0 < percent <= 100:
                raise ValueError
            return percent / 100.0
        except ValueError:
            print("Enter a percentage greater than 0 and at most 100, or leave blank.")


def read_optional_positive(prompt):
    while True:
        raw = input(prompt).strip().replace(",", ".")
        if not raw:
            return None
        try:
            value = float(raw)
            if not math.isfinite(value) or value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Enter a positive finite number, or leave blank.")


def collect_power_results(flow_m3_h, required_tdh_m, density_kg_m3):
    print("\nGROUP: PUMP AND MOTOR POWER")
    print("1. Enter pump and motor efficiencies manually")
    print("2. Enter pump-curve points one by one (flow and head; efficiency and shaft power optional)")
    print("3. Use default efficiencies of 100% (theoretical minimum power)")
    mode = read_choice(
        "Select power method [1-3, Enter=3 (idealized 100%)]: ",
        ["1", "2", "3"], default="3")
    pump_efficiency = 1.0
    motor_efficiency = 1.0
    shaft_power_kw = None
    curve_head = None
    curve_warning = None
    points = []

    if mode == "1":
        pump_efficiency = read_optional_efficiency("Pump efficiency (%) [Enter = 100%]: ")
        motor_efficiency = read_optional_efficiency("Motor efficiency (%) [Enter = 100%]: ")
    elif mode == "2":
        count = int(read_number("Number of pump-curve points (2-30): ", minimum=2))
        while count > 30:
            print("Maximum supported points: 30.")
            count = int(read_number("Number of pump-curve points (2-30): ", minimum=2))
        points = []
        for index in range(1, count + 1):
            print(f"\nPump curve point {index}/{count}")
            q = read_number("Flow rate (m³/h): ", minimum=0.000001)
            h = read_number("Pump head (m): ", minimum=0)
            eta_percent = read_optional_positive("Pump efficiency (%) [Enter if unavailable]: ")
            if eta_percent is not None and eta_percent > 100:
                print("Efficiency must not exceed 100%; please enter the curve again.")
                return collect_power_results(flow_m3_h, required_tdh_m, density_kg_m3)
            shaft = read_optional_positive("Pump shaft power (kW) [Enter if unavailable]: ")
            points.append({
                "flow_m3_h": q, "head_m": h,
                "pump_efficiency": eta_percent / 100.0 if eta_percent is not None else None,
                "shaft_power_kw": shaft,
            })
        try:
            validate_pump_curve(points)
        except ValueError as exc:
            print(f"Pump-curve data error: {exc}")
            return collect_power_results(flow_m3_h, required_tdh_m, density_kg_m3)

        curve_head = interpolate_curve(points, flow_m3_h, "head_m")
        curve_eta = interpolate_curve(points, flow_m3_h, "pump_efficiency")
        shaft_power_kw = interpolate_curve(points, flow_m3_h, "shaft_power_kw")
        if curve_head is None:
            curve_warning = "Required flow is outside the entered pump-curve range. No extrapolation was made."
        if curve_eta is not None:
            pump_efficiency = curve_eta
        elif shaft_power_kw is not None:
            hydraulic_kw = density_kg_m3 * 9.80665 * (flow_m3_h / 3600.0) * required_tdh_m / 1000.0
            derived_eta = hydraulic_kw / shaft_power_kw
            if 0 < derived_eta <= 1:
                pump_efficiency = derived_eta
            else:
                curve_warning = (curve_warning + " " if curve_warning else "") + "Derived efficiency is outside 0-100%; 100% default retained."
        else:
            print("No efficiency or shaft-power values were interpolated: using 100% pump efficiency.")
        motor_efficiency = read_optional_efficiency("Motor efficiency (%) [Enter = 100%]: ")

    try:
        power = calculate_power(
            flow_m3_h=flow_m3_h, required_tdh_m=required_tdh_m,
            density_kg_m3=density_kg_m3, pump_efficiency=pump_efficiency,
            motor_efficiency=motor_efficiency, shaft_power_kw=shaft_power_kw)
    except ValueError as exc:
        print(f"Power calculation error: {exc}")
        return None
    power["curve_head_m"] = curve_head
    power["curve_head_margin_m"] = curve_head - required_tdh_m if curve_head is not None else None
    power["curve_warning"] = curve_warning
    power["efficiency_source"] = {
        "1": "manual input (blank values default to 100%)",
        "2": "entered pump curve (missing values default to 100%)",
        "3": "100% idealized default",
    }[mode]
    power["_input_mode"] = mode
    power["_curve_points"] = points
    power["_shaft_power_input_kw"] = shaft_power_kw
    return power


def print_power_results(power):
    if power is None:
        return
    # Mechanical horsepower: 1 kW = 1.34102209 hp.
    kw_to_hp = 1.34102209
    hydraulic_hp = power["hydraulic_power_kw"] * kw_to_hp
    shaft_hp = power["shaft_power_kw"] * kw_to_hp
    electric_hp = power["electric_power_kw"] * kw_to_hp

    print("\nPUMP POWER RESULTS")
    print(f"Hydraulic power (system TDH)           : {power['hydraulic_power_kw']:.3f} kW ({hydraulic_hp:.3f} hp)")
    print(f"Pump efficiency                        : {power['pump_efficiency'] * 100:.2f}%")
    print(f"Motor efficiency                       : {power['motor_efficiency'] * 100:.2f}%")
    print(f"Pump shaft power                       : {power['shaft_power_kw']:.3f} kW ({shaft_hp:.3f} hp)")
    print(f"Electrical input power                 : {power['electric_power_kw']:.3f} kW ({electric_hp:.3f} hp)")
    print("-" * 68)
    print(f"FINAL REQUIRED ELECTRICAL POWER        : {power['electric_power_kw']:.3f} kW ({electric_hp:.3f} hp)")
    print("This is the estimated total electrical input power for the pump motor.")
    print(f"Efficiency / power data source         : {power['efficiency_source']}")
    if power["curve_head_m"] is not None:
        print(f"Pump-curve head at required flow       : {power['curve_head_m']:.3f} m")
        print(f"Pump head minus required system TDH    : {power['curve_head_margin_m']:+.3f} m")
        print("NOTE: Head comparison only; the actual pump/system operating point has not been solved.")
    if power["curve_warning"]:
        print(f"WARNING: {power['curve_warning']}")
    if power["consistency_warning"]:
        print(f"WARNING: {power['consistency_warning']}")
    if power["pump_efficiency"] == 1.0 or power["motor_efficiency"] == 1.0:
        print("NOTE: A 100% default is idealized; actual electrical consumption will normally be higher.")


def print_input_review(inputs):
    """Show the complete editable input set used for the current calculation."""
    print("\n" + "=" * 68)
    print("INPUT REVIEW — CURRENT CALCULATION")
    print("=" * 68)
    rows = [
        ("1", "EC at 25 °C", f"{inputs['ec']:.4f} mS/cm"),
        ("2", "Water composition profile", inputs["profile"]),
        ("3", "Operating temperature", f"{inputs['operating_temp']:.2f} °C"),
        ("4", "Elevation difference Δz", f"{inputs['delta_z']:+.4f} m"),
        ("5", "Flow rate", f"{inputs['flow']:.4f} m³/h"),
        ("6", "Straight pipe length", f"{inputs['length']:.4f} m"),
        ("7", "Internal pipe diameter", f"{inputs['diameter']:.4f} mm"),
        ("8", "Absolute roughness", f"{inputs['roughness']:.6g} mm"),
        ("9", "Total fitting K", f"{inputs['fittings_k']:.6g}"),
        ("10", "Total equipment pressure drop", f"{inputs['equipment_dp']:.6g} bar"),
        ("11", "Start boundary pressure", f"{inputs['p1']:.4f} kPa(g)"),
        ("12", "End boundary pressure", f"{inputs['p2']:.4f} kPa(g)"),
        ("13", "Start boundary velocity", f"{inputs['v1']:.4f} m/s"),
        ("14", "End boundary velocity", f"{inputs['v2']:.4f} m/s"),
        ("15", "Pump/motor power method", inputs.get("power_method_label", "Not set")),
    ]
    if inputs.get("pump_efficiency") is not None:
        rows.append(("16", "Pump efficiency", f"{inputs['pump_efficiency'] * 100:.3f} %"))
    if inputs.get("motor_efficiency") is not None:
        rows.append(("17", "Motor efficiency", f"{inputs['motor_efficiency'] * 100:.3f} %"))
    if inputs.get("shaft_power_kw") is not None:
        rows.append(("18", "Interpolated pump shaft power", f"{inputs['shaft_power_kw']:.4f} kW"))
    if inputs.get("curve_head_m") is not None:
        rows.append(("19", "Interpolated pump-curve head", f"{inputs['curve_head_m']:.4f} m"))
    if inputs.get("curve_points"):
        for i, point in enumerate(inputs["curve_points"], 1):
            rows.append((f"C{i}", "Pump-curve point", str(point)))
    if inputs.get("pipe_description"):
        rows.append(("-", "Selected pipe/catalogue", inputs["pipe_description"]))
    for number, label, value in rows:
        print(f"{number:>2}. {label:<38}: {value}")
    print("\nNote: fittings and equipment are shown as their total equivalent K and total pressure drop.")
    print("Individual fitting/equipment entries can be re-entered through their edit options.")


def calculate_and_print(inputs):
    """Recalculate all dependent results using the current input values."""
    try:
        fluid = estimate_from_ec(
            ec_ms_cm=inputs["ec"], temperature_c=inputs["operating_temp"],
            composition_profile=inputs["profile"], ec_reference_temperature_c=25.0)
        result = calculate_tdh(
            flow_m3_h=inputs["flow"], pipe_length_m=inputs["length"],
            internal_diameter_mm=inputs["diameter"], roughness_mm=inputs["roughness"],
            density_kg_m3=fluid.density_kg_m3,
            kinematic_viscosity_m2_s=fluid.kinematic_viscosity_m2_s,
            total_fitting_k=inputs["fittings_k"],
            equipment_pressure_drop_bar=inputs["equipment_dp"],
            elevation_difference_m=inputs["delta_z"],
            pressure_start_kpa=inputs["p1"], pressure_end_kpa=inputs["p2"],
            velocity_start_m_s=inputs["v1"], velocity_end_m_s=inputs["v2"])
    except ValueError as exc:
        print(f"Calculation error: {exc}")
        return None

    power_result = None
    if result["total_tdh_m"] >= 0:
        mode = inputs.get("power_mode")
        if mode in ("1", "2", "3"):
            try:
                pump_efficiency = inputs["pump_efficiency"]
                shaft_power = None
                curve_head = None
                curve_warning = None
                if mode == "2":
                    curve_points = inputs.get("curve_points", [])
                    curve_head = interpolate_curve(curve_points, inputs["flow"], "head_m")
                    curve_eta = interpolate_curve(curve_points, inputs["flow"], "pump_efficiency")
                    shaft_power = interpolate_curve(curve_points, inputs["flow"], "shaft_power_kw")
                    if curve_head is None:
                        curve_warning = "Required flow is outside the entered pump-curve range. No extrapolation was made."
                    if curve_eta is not None:
                        pump_efficiency = curve_eta
                    elif shaft_power is not None:
                        hydraulic_kw = fluid.density_kg_m3 * 9.80665 * (inputs["flow"] / 3600.0) * result["total_tdh_m"] / 1000.0
                        derived_eta = hydraulic_kw / shaft_power
                        if 0 < derived_eta <= 1:
                            pump_efficiency = derived_eta
                        else:
                            curve_warning = (curve_warning + " " if curve_warning else "") + "Derived efficiency is outside 0-100%; stored efficiency retained."
                power_result = calculate_power(
                    flow_m3_h=inputs["flow"], required_tdh_m=result["total_tdh_m"],
                    density_kg_m3=fluid.density_kg_m3,
                    pump_efficiency=pump_efficiency,
                    motor_efficiency=inputs["motor_efficiency"],
                    shaft_power_kw=shaft_power)
                power_result["curve_head_m"] = curve_head
                power_result["curve_head_margin_m"] = (
                    curve_head - result["total_tdh_m"] if curve_head is not None else None)
                power_result["curve_warning"] = curve_warning
                power_result["efficiency_source"] = inputs.get("power_method_label", "configured power inputs")
            except ValueError as exc:
                print(f"Power calculation error: {exc}")
        else:
            power_result = collect_power_results(
                inputs["flow"], result["total_tdh_m"], fluid.density_kg_m3)
            if power_result is not None:
                inputs["power_mode"] = power_result["_input_mode"]
                inputs["power_method_label"] = power_result["efficiency_source"]
                inputs["pump_efficiency"] = power_result["pump_efficiency"]
                inputs["motor_efficiency"] = power_result["motor_efficiency"]
                inputs["shaft_power_kw"] = power_result["_shaft_power_input_kw"]
                inputs["curve_head_m"] = power_result["curve_head_m"]
                inputs["curve_warning"] = power_result["curve_warning"]
                inputs["curve_points"] = power_result["_curve_points"]

    print("\n" + "=" * 68)
    print("FLUID PROPERTY ESTIMATES")
    print(f"EC (temperature-compensated to 25 °C) : {fluid.ec_ms_cm:.3f} mS/cm")
    print(f"Operating water temperature           : {fluid.temperature_c:.2f} °C")
    print(f"Composition profile                   : {fluid.fluid_type}")
    print(f"Estimated TDS                         : {fluid.tds_mg_l:.1f} mg/L")
    print(f"Estimated density                     : {fluid.density_kg_m3:.3f} kg/m³")
    print(f"Estimated kinematic viscosity         : {fluid.kinematic_viscosity_m2_s:.6g} m²/s")
    print("\nPIPE DATA")
    print(f"Nominal internal diameter             : {inputs['diameter']:.2f} mm")
    print(f"Absolute roughness                    : {inputs['roughness']:g} mm")
    print("\nHYDRAULIC RESULTS")
    print(f"Pipe velocity                         : {result['pipe_velocity_m_s']:.3f} m/s")
    print(f"Reynolds number                       : {result['reynolds']:.0f}")
    print(f"Flow regime                           : {result['flow_regime']}")
    print(f"Darcy friction factor                 : {result['darcy_friction_factor']:.6f}")
    print("-" * 68)
    print(f"Static head Δz                        : {result['static_head_m']:+.4f} m")
    print(f"Pressure head difference              : {result['pressure_head_m']:+.4f} m")
    print(f"Velocity head difference               : {result['velocity_head_difference_m']:+.4f} m")
    print(f"Major pipe loss                       : {result['major_loss_m']:.4f} m")
    print(f"Fittings / valves loss                : {result['fitting_loss_m']:.4f} m")
    print(f"Equipment pressure loss               : {result['equipment_loss_m']:.4f} m")
    print("-" * 68)
    print(f"REQUIRED PUMP TDH                     : {result['total_tdh_m']:.4f} m")
    print_power_results(power_result)
    if result["total_tdh_m"] < 0:
        print("\nPower calculation skipped because required TDH is negative.")
        print("NOTE: Negative TDH may indicate gravity-driven flow or boundary conditions to review.")
    if result["friction_warning"]:
        print(f"WARNING: {result['friction_warning']}")
    for warning in fluid.warnings:
        print(f"FLUID NOTE: {warning}")
    print("=" * 68)
    return fluid, result, power_result


def edit_inputs(inputs):
    """One-parameter-at-a-time input editor."""
    while True:
        print_input_review(inputs)
        print("\nEDIT ONE PARAMETER")
        print("1 EC | 2 composition profile | 3 temperature | 4 elevation difference")
        print("5 flow | 6 pipe length | 7 internal diameter | 8 roughness")
        print("9 total fitting K | 10 equipment pressure drop")
        print("11 start pressure | 12 end pressure | 13 start velocity | 14 end velocity")
        print("15 re-enter pump/motor power data")
        print("0 return/finish")
        choice = read_choice("Select one item to edit [0-15]: ",
                             [str(i) for i in range(16)], default="0")
        if choice == "0":
            return
        key_map = {
            "1": ("ec", "EC at 25 °C (mS/cm): ", False, 0.0),
            "3": ("operating_temp", "Operating temperature (°C): ", False, 0.0),
            "4": ("delta_z", "Elevation difference Δz (m): ", True, None),
            "5": ("flow", "Flow rate (m³/h): ", False, 0.000001),
            "6": ("length", "Straight pipe length (m): ", False, 0.0),
            "7": ("diameter", "Internal diameter (mm): ", False, 0.000001),
            "8": ("roughness", "Absolute roughness (mm): ", False, 0.0),
            "9": ("fittings_k", "Total fitting K: ", False, 0.0),
            "10": ("equipment_dp", "Total equipment pressure drop (bar): ", False, 0.0),
            "11": ("p1", "Start pressure (kPa gauge): ", True, None),
            "12": ("p2", "End pressure (kPa gauge): ", True, None),
            "13": ("v1", "Start velocity (m/s): ", False, 0.0),
            "14": ("v2", "End velocity (m/s): ", False, 0.0),
        }
        if choice == "2":
            profile_choice = read_choice(
                "Composition profile [1=generic, 2=natural seawater]: ", ["1", "2"])
            inputs["profile"] = "natural_seawater" if profile_choice == "2" else "generic"
        elif choice == "15":
            inputs["power_mode"] = None
            inputs["power_method_label"] = "Re-entered after input edit"
            return
        else:
            key, prompt, allow_negative, minimum = key_map[choice]
            inputs[key] = read_number(prompt, allow_negative=allow_negative, minimum=minimum)
        print("\nInput updated. All dependent results will be recalculated.")


def main():
    print("=" * 68)
    print("PUMP TOTAL DYNAMIC HEAD (TDH) CALCULATOR")
    print("Single steady-state flow path | SI units")
    print("=" * 68)

    print("\nGROUP: FLUID PROPERTIES")
    print("EC input is conductivity already temperature-compensated to 25 °C.")
    print("It is NOT the operating water temperature.")
    ec = read_number("EC at 25 °C (mS/cm): ")
    print("\nSelect the water composition assumption:")
    print("1. Generic water / groundwater / brackish water")
    print("2. Natural seawater ionic-ratio screening profile")
    profile = "natural_seawater" if read_choice("Select profile [1-2]: ", ["1", "2"]) == "2" else "generic"
    operating_temp = read_number("Actual operating water temperature (°C): ")

    try:
        fluid = estimate_from_ec(ec_ms_cm=ec, temperature_c=operating_temp,
                                 composition_profile=profile, ec_reference_temperature_c=25.0)
    except ValueError as exc:
        print(f"Fluid input error: {exc}")
        return

    delta_z = collect_static_head()
    flow, length, diameter, roughness, pipe_info = collect_pipe()
    fittings_k = collect_fittings(load_json("fittings.json")["fittings"])
    equipment_dp = collect_equipment_drop(load_json("equipment_templates.json")["equipment"])

    print("\nGROUP: BOUNDARY CONDITIONS")
    print("Enter gauge pressures at start/end. For two open tanks, enter 0 for both.")
    p1 = read_number("Start pressure (kPa gauge): ", allow_negative=True)
    p2 = read_number("End pressure (kPa gauge): ", allow_negative=True)
    print("For two large tank free surfaces, use zero for both boundary velocities.")
    v1 = read_number("Start velocity (m/s): ") if read_choice("Enter start velocity? [y/N]: ", ["y", "Y", "n", "N"]) in ("y", "Y") else 0.0
    v2 = read_number("End velocity (m/s): ") if read_choice("Enter end velocity? [y/N]: ", ["y", "Y", "n", "N"]) in ("y", "Y") else 0.0

    inputs = {
        "ec": ec, "profile": profile, "operating_temp": operating_temp,
        "delta_z": delta_z, "flow": flow, "length": length,
        "diameter": diameter, "roughness": roughness,
        "fittings_k": fittings_k, "equipment_dp": equipment_dp,
        "p1": p1, "p2": p2, "v1": v1, "v2": v2,
        "pipe_description": (
            f"HDPE grade={pipe_info['grade']}, SDR={pipe_info['sdr']}, OD={pipe_info['outside_diameter_mm']} mm"
            if pipe_info else "Non-HDPE pipe; geometry entered manually"
        ),
        "power_mode": None, "power_method_label": "Not yet configured",
        "pump_efficiency": None, "motor_efficiency": None,
        "shaft_power_kw": None, "curve_head_m": None, "curve_warning": None,
        "curve_points": [],
    }

    while True:
        calculated = calculate_and_print(inputs)
        if calculated is None:
            print("Correct the inputs before continuing.")
        print_input_review(inputs)
        action = read_choice(
            "\nChoose: [1] Edit one input and recalculate  [0] Exit: ",
            ["0", "1"], default="0")
        if action == "0":
            break
        edit_inputs(inputs)


if __name__ == "__main__":
    main()
