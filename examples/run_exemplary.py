"""Run the exemplary CHLOE Excel input and print a human-readable summary."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from chloe.excel_io import run_chloe


OUTPUT_LABELS = {
    "total_heating_load": "Total Heating Load",
    "ventilation_losses_heating": "Ventilation losses (heating)",
    "transmission_losses_heating": "Transmission losses (heating)",
    "total_cooling_load": "Total Cooling load",
    "total_cooling_load_july": "Total Cooling load July",
    "total_cooling_load_september": "Total Cooling load September",
    "solar_heat_gains_july_cooling": "Solar heat gains July (cooling)",
    "transmission_heat_gains_july_cooling": "Transmission heat gains July (cooling)",
    "ventilation_heat_gains_july_cooling": "Ventilation heat gains July (cooling)",
    "internal_gains_cooling": "Internal gains (cooling)",
    "solar_heat_gains_september_cooling": "Solar heat gains Sept (cooling)",
    "transmission_heat_gains_september_cooling": "Transmission heat gains Sept (cooling)",
    "ventilation_heat_gains_september_cooling": "Ventilation heat gains Sept (cooling)",
}


def print_results(rounded_outputs: dict) -> None:
    """Print the exemplary CHLOE result in the historical console layout."""
    print("Results - Heating Load")
    print(f"{OUTPUT_LABELS['total_heating_load']}: {rounded_outputs['total_heating_load']} W")
    print(
        f"{OUTPUT_LABELS['ventilation_losses_heating']}: "
        f"{rounded_outputs['ventilation_losses_heating']} W"
    )
    print(
        f"{OUTPUT_LABELS['transmission_losses_heating']}: "
        f"{rounded_outputs['transmission_losses_heating']} W"
    )

    print(" ")
    print("Results - Cooling Load")
    print(f"{OUTPUT_LABELS['total_cooling_load']}: {rounded_outputs['total_cooling_load']} W")
    print(
        f"{OUTPUT_LABELS['total_cooling_load_july']}: "
        f"{rounded_outputs['total_cooling_load_july']} W"
    )
    print(
        f"{OUTPUT_LABELS['total_cooling_load_september']}: "
        f"{rounded_outputs['total_cooling_load_september']} W"
    )
    print("-------------")
    print(
        f"{OUTPUT_LABELS['solar_heat_gains_july_cooling']}: "
        f"{rounded_outputs['solar_heat_gains_july_cooling']} W"
    )
    print(
        f"{OUTPUT_LABELS['transmission_heat_gains_july_cooling']}: "
        f"{rounded_outputs['transmission_heat_gains_july_cooling']} W"
    )
    print(
        f"{OUTPUT_LABELS['ventilation_heat_gains_july_cooling']}: "
        f"{rounded_outputs['ventilation_heat_gains_july_cooling']} W"
    )
    print(f"{OUTPUT_LABELS['internal_gains_cooling']}: {rounded_outputs['internal_gains_cooling']} W")
    print("-------------")
    print(
        f"{OUTPUT_LABELS['solar_heat_gains_september_cooling']}: "
        f"{rounded_outputs['solar_heat_gains_september_cooling']} W"
    )
    print(
        f"{OUTPUT_LABELS['transmission_heat_gains_september_cooling']}: "
        f"{rounded_outputs['transmission_heat_gains_september_cooling']} W"
    )
    print(
        f"{OUTPUT_LABELS['ventilation_heat_gains_september_cooling']}: "
        f"{rounded_outputs['ventilation_heat_gains_september_cooling']} W"
    )
    print(f"{OUTPUT_LABELS['internal_gains_cooling']}: {rounded_outputs['internal_gains_cooling']} W")
    print("-------------")


def main() -> None:
    result = run_chloe(str(REPO_ROOT / "Exemplary_Inputs.xlsx"))
    print_results(result["rounded_outputs"])


if __name__ == "__main__":
    main()

