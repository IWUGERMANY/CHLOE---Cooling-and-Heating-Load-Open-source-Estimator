"""Service entry points for CHLOE simulations."""

from __future__ import annotations

from .calculator import HeatingCoolingLoadCalculator
from .inputs import ChloeInput
from .results import ChloeResult


def run_chloe_simulation(chloe_params) -> ChloeResult:
    """Run CHLOE from structured parameters and return a result object."""
    chloe_input = ChloeInput.from_object(chloe_params)
    calculator = HeatingCoolingLoadCalculator()
    return calculator.calculate(chloe_input)
