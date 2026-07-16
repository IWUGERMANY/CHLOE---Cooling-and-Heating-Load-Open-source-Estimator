"""Public CHLOE package API for application integrations.

Use `run_chloe_simulation(...)` with structured `ChloeInput` data from host
applications such as Lezbau. Excel helpers live in `chloe.excel_io` and are kept
for examples and golden regression only.
"""

from .calculator import HeatingCoolingLoadCalculator
from .inputs import ChloeInput
from .results import ChloeResult
from .service import run_chloe_simulation

__version__ = "0.2.0"

__all__ = [
    "ChloeInput",
    "ChloeResult",
    "HeatingCoolingLoadCalculator",
    "run_chloe_simulation",
]

