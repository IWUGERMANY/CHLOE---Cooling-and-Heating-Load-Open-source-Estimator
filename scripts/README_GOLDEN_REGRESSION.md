# CHLOE Golden Regression

This regression script protects the current CHLOE behavior for
`Exemplary_Inputs.xlsx`.

The script uses the package-level Excel helper in `chloe.excel_io`, collects the
calculated `calculator.__dict__`, the loaded input values, and the rounded output
values, then compares them with a golden CSV generated from the trusted baseline
branch.

## Initial Golden Creation

Run this once on the trusted baseline branch:

```powershell
cd "C:\Users\wail\Desktop\Projects\CHLOE---Cooling-and-Heating-Load-Open-source-Estimator"
python scripts\regression_chloe_golden.py --update-golden
```

This creates:

```text
tests/golden/chloe_exemplary_outputs.csv
```

Commit the golden file together with this script.

## Regression Check On Another Branch

After changing CHLOE on an optimization/refactoring branch:

```powershell
cd "C:\Users\wail\Desktop\Projects\CHLOE---Cooling-and-Heating-Load-Open-source-Estimator"
python scripts\regression_chloe_golden.py
```

Expected output:

```text
differences=0
```

The script also writes a comparison report to:

```text
regression_results/chloe_exemplary_comparison.xlsx
```

If `openpyxl` is unavailable, the comparison report is written as CSV instead.

## What Is Compared

- Excel input values loaded by `chloe.excel_io.read_input_values(...)`.
- All calculated attributes stored on `calculator.__dict__`.
- Rounded output values produced by `chloe.excel_io.build_rounded_outputs(...)`.

Numeric values are compared with a default tolerance of `1e-9`.

## Notes

This script does not change CHLOE formulas. It intentionally keeps Excel isolated
as a regression/example path. Productive integrations such as Lezbau should use
`from chloe import ChloeInput, run_chloe_simulation` instead.
