# Pump TDH Calculator

A Python engineering tool for calculating pump Total Dynamic Head (TDH) in water-transfer systems.

## Project scope

The project will grow in independent calculation modules:

- Fluid properties
- Pipe geometry and pipe database
- Darcy-Weisbach friction loss
- Fitting and valve minor losses
- Equipment pressure losses
- Elevation and pipeline profile
- Total Dynamic Head (TDH)
- Pump power and operating-point checks

## Initial implementation

The first implemented module is `core/fluid_properties.py`.

It supports:
1. Freshwater properties using a tabulated temperature range (0–100 °C) with linear interpolation.
2. A natural-seawater reference condition at 25 °C and 35 g/kg.
3. User-supplied density and dynamic viscosity for custom fluids.

The module calculates kinematic viscosity from:

```
nu = dynamic_viscosity / density
```

## Important engineering limitations

- Freshwater table values are approximate engineering values at approximately atmospheric pressure.
- Seawater is currently supported only at its stated reference condition. Other seawater temperatures/salinities require validated property data or measured values.
- Conductivity (EC) is not yet converted to salinity. This conversion depends on temperature and water composition; it should not be assumed valid for concentrated RO brine.
- This project does not yet calculate TDH. The next modules will add pipe losses, elevation, equipment losses, and the pump energy equation.
- Final pump selection must use the actual system curve, pump curve, efficiency, NPSH requirements, and transient/surge checks where applicable.

## Run

Python 3.10 or newer is recommended.

```bash
python main.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```
