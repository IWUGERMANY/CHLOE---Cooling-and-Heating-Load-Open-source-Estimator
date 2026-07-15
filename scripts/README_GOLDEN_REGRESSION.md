# CHLOE Golden Regression

This regression script protects the current CHLOE behavior for
`Exemplary_Inputs.xlsx`.

The current `main.py` executes calculation logic at module level and prints the
results. The script therefore runs `main.py` in a controlled context, captures the
calculated globals and the `calculator.__dict__`, and compares them with a golden
CSV generated from the `main` branch.

## Initial Golden Creation

Run this once on the current trusted `main` branch:

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

- Excel input values loaded by `main.py`.
- All calculated attributes stored on `calculator.__dict__`.
- Rounded output values that are currently printed by `main.py`.

Numeric values are compared with a default tolerance of `1e-9`.

## Notes

This script does not change CHLOE formulas. It is intentionally compatible with
the current `main.py` structure. A later cleanup can move CHLOE execution into a
function such as `run_chloe(input_path)`, but that is not required for the first
regression safety net.
