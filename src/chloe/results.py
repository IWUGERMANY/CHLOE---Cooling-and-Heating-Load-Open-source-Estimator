"""Result contract for CHLOE simulations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .calculator import HeatingCoolingLoadCalculator


@dataclass(frozen=True)
class ChloeResult:
    phi_hl: float
    phi_cl: float
    phi_cl_july: float
    phi_cl_sept: float
    phi_t_heating: float
    phi_v_tot_heating: float
    phi_t_cooling_july: float
    phi_v_tot_cooling_july: float
    phi_t_cooling_sept: float
    phi_v_tot_cooling_sept: float
    phi_solar_tot_july: float
    phi_solar_tot_sept: float
    phi_i_cooling: float

    @classmethod
    def from_calculator(cls, calculator: "HeatingCoolingLoadCalculator") -> "ChloeResult":
        """Create an explicit CHLOE result from calculator attributes."""
        return cls(
            phi_hl=calculator.phi_hl,
            phi_cl=calculator.phi_cl,
            phi_cl_july=calculator.phi_cl_july,
            phi_cl_sept=calculator.phi_cl_sept,
            phi_t_heating=calculator.phi_t_heating,
            phi_v_tot_heating=calculator.phi_v_tot_heating,
            phi_t_cooling_july=calculator.phi_t_cooling_july,
            phi_v_tot_cooling_july=calculator.phi_v_tot_cooling_july,
            phi_t_cooling_sept=calculator.phi_t_cooling_sept,
            phi_v_tot_cooling_sept=calculator.phi_v_tot_cooling_sept,
            phi_solar_tot_july=calculator.phi_solar_tot_july,
            phi_solar_tot_sept=calculator.phi_solar_tot_sept,
            phi_i_cooling=calculator.phi_i_cooling,
        )
