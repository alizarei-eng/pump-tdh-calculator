# Pump TDH Calculator

Python engineering project for estimating fluid properties and calculating pump Total Dynamic Head (TDH) in water-transfer systems.

## Current implementation
- EC-based TDS estimate with user-selectable TDS/EC factor (default 0.65).
- Temperature-dependent freshwater base properties (0–100 °C) with approximate salinity corrections.
- Optional natural-seawater ionic-ratio profile for screening estimates.
- User-visible warnings where EC cannot identify ionic composition.
- Next modules: pipe geometry, Darcy-Weisbach losses, fittings/equipment losses, elevation profile and TDH.

## Run
```bash
python main.py
python -m unittest discover -s tests -v
```

## Engineering limitations
EC does not uniquely determine sodium, calcium, magnesium, iron, chloride, sulfate, bicarbonate or other individual constituents. Generic profile therefore reports no invented ion concentrations. The natural-seawater profile assumes standard seawater ratios and must not be applied to groundwater or RO concentrate without laboratory validation.

TDS is estimated as EC(µS/cm) × factor. The default factor 0.65 is not universal. EC must be temperature-compensated to 25 °C. Density and viscosity corrections are approximate screening correlations, not a validated electrolyte equation of state. At high EC/concentrated brine, use measured or validated properties. Iron is not inferred; lime is not an ion. Calcium hardness and bicarbonate alkalinity are shown as CaCO3 equivalents only under the seawater-profile assumption.

The project does not yet calculate TDH. Pump selection will also require the system curve, pump curve, efficiency, NPSH and transient checks.
