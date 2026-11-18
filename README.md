# Pump TDH Calculator

Python CLI for estimating fluid properties and calculating the required pump Total Dynamic Head (TDH) for a single steady-state flow path.

## Implemented
- EC-based screening estimates for TDS, density and viscosity. EC is entered as a value temperature-compensated to 25 °C; operating water temperature is a separate input.
- PE pipe selection by material grade (PE80/PE100), SDR and outside diameter (OD), with nominal wall thickness and internal diameter loaded from the copied ISO 4427 reference catalogue.
- Automatic absolute roughness lookup by pipe material. Values are indicative engineering defaults; the user does not enter roughness for listed materials.
- Static head using either direct Δz or start/end elevations.
- Darcy–Weisbach major pipe loss, K-based fitting/valve losses, equipment differential-pressure losses and boundary pressure/velocity head differences.
- Component-by-component TDH report.

## Run
```bash
python main.py
python -m unittest discover -s tests -v
```

## Data provenance and engineering limitations
- `databases/pipe_standards.json` is copied from `hdpe-pipe-diameter-selector`; catalogue entries include both directly transcribed and ratio-derived wall-thickness records. Verify ratio-derived dimensions against a controlled standard/manufacturer catalogue before design release.
- `databases/pipe_materials.json` is copied from `pipe-pressure-loss-calculator`. Roughness values are indicative, not guaranteed manufacturer values.
- For non-HDPE materials the CLI asks OD and nominal wall thickness because SDR is not a universal designation for those materials. Their roughness is loaded automatically.
- This version models one steady-state flow path with one reference pipe diameter. Fitting K values are approximate; equipment losses require measured/manufacturer ΔP. EC-derived density and viscosity are screening estimates, particularly unsuitable as final properties for concentrated brine without validation.
- Not yet included: branched/multi-diameter networks, pump/system curves, pump selection, efficiency/power, NPSH and transient surge/water hammer.
