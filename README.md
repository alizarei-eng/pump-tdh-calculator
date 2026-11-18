# Pump TDH Calculator

Python CLI for estimating fluid properties and calculating the required pump Total Dynamic Head (TDH) for a single steady-state flow path.

## Implemented
- EC-based fluid-property screening (TDS, density, viscosity).
- Static head using either direct Δz or start/end elevations.
- Darcy–Weisbach major pipe loss.
- K-based fitting and valve losses using the transferred reference fitting database.
- Equipment differential-pressure losses (filters, heat exchangers, RO, etc.) entered from measured/manufacturer ΔP and converted to metres of fluid.
- Boundary pressure-head and velocity-head differences.
- Component-by-component TDH report.

## Run
```bash
python main.py
python -m unittest discover -s tests -v
```

## Engineering limitations
This version models one steady-state flow path with one reference pipe diameter. Fitting K values are approximate and must be checked against actual geometry/manufacturer data. Equipment losses use measured or manufacturer differential pressure; no universal K is invented for filters or RO equipment. EC-derived density and viscosity are screening estimates only, especially unsuitable as final properties for concentrated brine without validation.

Not yet included: branched/multi-diameter networks, pump/system curves, pump selection, efficiency/power, NPSH, transient surge/water hammer.
