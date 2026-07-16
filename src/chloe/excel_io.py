"""Excel input helpers for CHLOE examples and golden regression."""

from __future__ import annotations

from .calculator import HeatingCoolingLoadCalculator
from .inputs import ChloeInput, PARAMETERS
from .results import ChloeResult
from .service import run_chloe_simulation


def read_input_values(input_path: str = "Exemplary_Inputs.xlsx", column_name: str = "B") -> ChloeInput:
    """Read CHLOE input parameters from the exemplary Excel input file."""
    import openpyxl

    workbook = openpyxl.load_workbook(input_path, data_only=True)
    worksheet = workbook.active
    values = {
        parameter: worksheet[f"{column_name}{row}"].value
        for row, parameter in enumerate(PARAMETERS, start=2)
    }
    return ChloeInput.from_mapping(values)


def build_rounded_outputs(result: ChloeResult) -> dict:
    """Return the rounded output values that the original script printed."""
    return {
        "total_heating_load": round(result.phi_hl),
        "ventilation_losses_heating": round(result.phi_v_tot_heating),
        "transmission_losses_heating": round(result.phi_t_heating),
        "total_cooling_load": round(result.phi_cl),
        "total_cooling_load_july": round(result.phi_cl_july),
        "total_cooling_load_september": round(result.phi_cl_sept),
        "solar_heat_gains_july_cooling": round(result.phi_solar_tot_july),
        "transmission_heat_gains_july_cooling": round(result.phi_t_cooling_july),
        "ventilation_heat_gains_july_cooling": round(result.phi_v_tot_cooling_july),
        "internal_gains_cooling": round(result.phi_i_cooling),
        "solar_heat_gains_september_cooling": round(result.phi_solar_tot_sept),
        "transmission_heat_gains_september_cooling": round(result.phi_t_cooling_sept),
        "ventilation_heat_gains_september_cooling": round(result.phi_v_tot_cooling_sept),
    }


def run_chloe(input_path: str = "Exemplary_Inputs.xlsx") -> dict:
    """Run CHLOE for an Excel input file and return inputs, calculator and outputs."""
    chloe_input = read_input_values(input_path)
    calculator = HeatingCoolingLoadCalculator()
    result = calculator.calculate(chloe_input)
    return {
        "input_values": chloe_input.__dict__,
        "chloe_input": chloe_input,
        "calculator": calculator,
        "result": result,
        "rounded_outputs": build_rounded_outputs(result),
    }
