"""Local pipe catalogue and material roughness lookups.

Catalogue dimensions are copied from hdpe-pipe-diameter-selector.
Indicative material roughness values are copied from pipe-pressure-loss-calculator.
"""
from __future__ import annotations
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPE_DB = ROOT / "databases" / "pipe_standards.json"
MATERIAL_DB = ROOT / "databases" / "pipe_materials.json"

def _load(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)

def available_grades():
    return sorted({p["material_grade"] for p in _load(PIPE_DB)["pipes"]})

def available_sdrs(grade):
    return sorted({float(p["sdr"]) for p in _load(PIPE_DB)["pipes"] if p["material_grade"] == grade})

def available_ods(grade, sdr):
    return sorted({float(p["dn_od_mm"]) for p in _load(PIPE_DB)["pipes"]
                   if p["material_grade"] == grade and float(p["sdr"]) == float(sdr)})

def get_pe_pipe(grade, sdr, od_mm):
    matches = [p for p in _load(PIPE_DB)["pipes"]
               if p["material_grade"] == grade and float(p["sdr"]) == float(sdr)
               and float(p["dn_od_mm"]) == float(od_mm)]
    if not matches:
        raise ValueError(f"No catalogue row for {grade}, SDR {sdr}, OD {od_mm:g} mm.")
    row = matches[0]
    wall = float(row["nominal_wall_thickness_mm"])
    inside = float(row["dn_od_mm"]) - 2.0 * wall
    if inside <= 0:
        raise ValueError("Catalogue dimensions produce a non-positive internal diameter.")
    return {"material": "HDPE", "grade": grade, "sdr": float(sdr),
            "outside_diameter_mm": float(od_mm), "wall_thickness_mm": wall,
            "internal_diameter_mm": inside, "nominal_pressure_bar": row.get("nominal_pressure_bar"),
            "dimension_status": row.get("status", "catalogue record")}

def get_materials():
    return _load(MATERIAL_DB)["materials"]

def get_material_roughness(material_id):
    rows = get_materials()
    row = next((x for x in rows if int(x["id"]) == int(material_id)), None)
    if row is None:
        raise ValueError("Unknown pipe material.")
    if row["roughness_mm"] is None:
        raise ValueError("Manual roughness selected; a value is required.")
    return float(row["roughness_mm"]), row["name"], row["roughness_label"]

def calculate_non_pe_geometry(outside_diameter_mm, wall_thickness_mm):
    od, wall = float(outside_diameter_mm), float(wall_thickness_mm)
    if not math.isfinite(od) or not math.isfinite(wall) or od <= 0 or wall <= 0 or 2*wall >= od:
        raise ValueError("OD and wall thickness must be positive; twice wall thickness must be smaller than OD.")
    return od - 2*wall
