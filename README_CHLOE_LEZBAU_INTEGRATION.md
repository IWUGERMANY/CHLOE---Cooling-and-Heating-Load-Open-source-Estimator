# CHLOE Lezbau Integration

## Ziel

Diese Datei beschreibt, wie CHLOE nach dem Refactoring in Lezbau integriert werden soll.
CHLOE soll nicht mehr ueber Excel produktiv genutzt werden, sondern ueber eine kleine, stabile Python-API.

## Produktive API

Lezbau soll spaeter nur diese Core-API verwenden:

```python
from chloe import ChloeInput, ChloeResult, run_chloe_simulation
```

Der produktive Einstiegspunkt ist:

```python
result = run_chloe_simulation(chloe_input)
```

Dabei kann `chloe_input` entweder ein `ChloeInput` sein oder ein Objekt, das die
benoetigten Attribute enthaelt.

## Produktiver Datenfluss

Der Ziel-Datenfluss in Lezbau ist:

```text
User / Frontend / Django DB
  -> Lezbau Mapper / build_chloe_input_object(...)
  -> ChloeInput
  -> run_chloe_simulation(...)
  -> ChloeResult
  -> Lezbau Ergebnisaggregation / API Response
```

Wichtig: Excel ist kein produktiver Datenpfad fuer Lezbau.

## Rolle von `build_chloe_input_object(...)`

In Lezbau soll `build_chloe_input_object(...)` die Aufgabe uebernehmen, die passenden
Daten aus Django/Mapper/DIBS-Ergebnissen in ein CHLOE-kompatibles Input-Objekt zu
uebersetzen.

Langfristig ist das Ziel:

```python
from chloe import ChloeInput, run_chloe_simulation

chloe_input = ChloeInput(
    # Werte aus Lezbau Mapping / DB / Simulationsergebnissen
)
chloe_result = run_chloe_simulation(chloe_input)
```

Falls Lezbau voruebergehend ein eigenes Objekt baut, bleibt das moeglich, solange alle
benoetigten Attribute vorhanden sind. `ChloeInput.from_object(...)` kann solche Objekte
in den stabilen CHLOE-Input-Vertrag normalisieren.

## Rolle von Excel

Excel bleibt nur fuer:

- Golden Regression mit `Exemplary_Inputs.xlsx`;
- Vergleich gegen bekannte CHLOE-Ergebnisse;
- manuelles Beispiel ueber `examples/run_exemplary.py`.

Die Excel-Helfer liegen bewusst separat in:

```text
src/chloe/excel_io.py
```

Sie werden nicht mehr ueber die Public Core API in `src/chloe/__init__.py` exportiert.
Wenn sie gebraucht werden, sollen sie explizit importiert werden:

```python
from chloe.excel_io import run_chloe, read_input_values
```

## Wichtige Dateien

```text
src/chloe/inputs.py       # ChloeInput und Input-Normalisierung
src/chloe/results.py      # ChloeResult
src/chloe/calculator.py   # HeatingCoolingLoadCalculator und Formeln
src/chloe/service.py      # run_chloe_simulation(...)
src/chloe/excel_io.py     # Excel-only Regression/Example Helper
```

## Regression nach Aenderungen

Nach jeder fachlichen oder strukturellen Aenderung soll der Nutzer ausfuehren:

```powershell
cd "C:\Users\wail\Desktop\Projects\CHLOE---Cooling-and-Heating-Load-Open-source-Estimator"
python scripts\regression_chloe_golden.py
```

Erwartung:

```text
differences=0
```

Optional fuer die alte Beispielausgabe:

```powershell
python examples\run_exemplary.py
```

## Naechste Lezbau-Schritte

1. In Lezbau pruefen, welche Werte `build_chloe_input_object(...)` aktuell liefert.
2. Diese Werte gegen `ChloeInput` mappen.
3. Lezbau so umbauen, dass `run_chloe_simulation(chloe_input)` aufgerufen wird.
4. Ergebnisfelder aus `ChloeResult` in die bestehende Lezbau Ergebnisstruktur uebernehmen.
5. Regression in CHLOE und danach Integrationstest in Lezbau ausfuehren.

