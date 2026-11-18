"""Darcy friction-factor calculations, adapted from pipe-pressure-loss-calculator."""
from __future__ import annotations
import math

def darcy_friction_factor(reynolds: float, relative_roughness: float) -> tuple[float, str | None]:
    if reynolds <= 0 or relative_roughness < 0:
        raise ValueError("Invalid Reynolds number or relative roughness.")
    if reynolds < 2300:
        return 64.0 / reynolds, None
    warning = ("Flow is in the transition region (Re 2300–4000); friction-factor prediction is uncertain."
               if reynolds < 4000 else None)
    factor = 0.25 / (math.log10(relative_roughness / 3.7 + 5.74 / reynolds**0.9) ** 2)
    for _ in range(100):
        term = relative_roughness / 3.7 + 2.51 / (reynolds * math.sqrt(factor))
        updated = 1.0 / (-2.0 * math.log10(term)) ** 2
        if abs(updated - factor) < 1e-12:
            factor = updated
            break
        factor = updated
    return factor, warning
