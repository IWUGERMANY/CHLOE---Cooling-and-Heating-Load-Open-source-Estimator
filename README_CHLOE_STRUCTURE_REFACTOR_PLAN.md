# CHLOE Structure Refactoring Plan

## Ziel

`main.py` soll nicht dauerhaft die komplette CHLOE-Logik enthalten. Fuer Lezbau,
PyPI und langfristige Wartbarkeit soll CHLOE als sauberes Python-Package mit
klarer Public API strukturiert werden.

Aktueller Zwischenstand auf `chloe-optimization`:

- `ChloeInput` existiert.
- `ChloeResult` existiert.
- `run_chloe_simulation(chloe_params)` existiert.
- `run_chloe(input_path)` bleibt fuer Excel-/Golden-Regression erhalten.
- Konsolenausgabe wurde aus `main.py` entfernt und nach `examples/run_exemplary.py`
  verschoben.

Das ist fachlich gut, aber strukturell noch nicht final, weil alles noch in
`main.py` liegt.

## Zielstruktur

```text
CHLOE---Cooling-and-Heating-Load-Open-source-Estimator/
  src/
    chloe/
      __init__.py                 # Public API
      inputs.py                   # ChloeInput
      results.py                  # ChloeResult
      calculator.py               # HeatingCoolingLoadCalculator
      service.py                  # run_chloe_simulation(...)
      excel_io.py                 # read_input_values(...), run_chloe(...)
  examples/
    run_exemplary.py              # Demo mit Excel + print
  scripts/
    regression_chloe_golden.py    # Golden Regression
  tests/
    golden/
      chloe_exemplary_outputs.csv
```

## Leitplanken

- Keine Formel-Aenderungen waehrend des Splits.
- Keine fachliche Ergebnis-Aenderung.
- Golden Regression muss nach jedem Schritt `differences=0` liefern.
- Excel bleibt nur fuer Regression und Beispiel relevant.
- Produktive Lezbau-Integration soll spaeter ueber `ChloeInput` und
  `run_chloe_simulation(...)` laufen.
- Codex fuehrt keine Tests aus; der Nutzer fuehrt Regression/Tests selbst aus.

## S1: Package-Ordner anlegen

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `src/chloe/` angelegt.
- `src/chloe/__init__.py` angelegt.
- Noch keine Logik verschoben.

### Ziel

Die Package-Struktur vorbereiten:

```text
src/chloe/
  __init__.py
```

### Ergebnis

Noch keine Logik verschieben, nur Zielstruktur anlegen.

### Pruefung durch Nutzer

```powershell
python scripts\regression_chloe_golden.py
```

Erwartung:

```text
differences=0
```

## S2: `ChloeInput` nach `src/chloe/inputs.py` verschieben

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `ChloeInput` nach `src/chloe/inputs.py` verschoben.
- `PARAMETERS` nach `src/chloe/inputs.py` verschoben.
- `main.py` importiert `ChloeInput` und `PARAMETERS` aus `chloe.inputs`.
- `src/chloe/__init__.py` exportiert `ChloeInput`.

### Ziel

Input-Vertrag aus `main.py` herausloesen.

Neue Datei:

```text
src/chloe/inputs.py
```

Enthaelt:

```python
ChloeInput
PARAMETERS
```

`main.py` importiert danach:

```python
from chloe.inputs import ChloeInput, PARAMETERS
```

### Nutzen

- Lezbau kann spaeter direkt `ChloeInput` importieren.
- Input-Mapping wird sichtbarer und testbarer.

### Pruefung durch Nutzer

```powershell
python scripts\regression_chloe_golden.py
```

## S3: `ChloeResult` nach `src/chloe/results.py` verschieben

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `ChloeResult` nach `src/chloe/results.py` verschoben.
- `main.py` importiert `ChloeResult` aus `chloe.results`.
- `src/chloe/__init__.py` exportiert `ChloeResult`.

### Ziel

Ergebnis-Vertrag aus `main.py` herausloesen.

Neue Datei:

```text
src/chloe/results.py
```

Enthaelt:

```python
ChloeResult
```

### Nutzen

- Lezbau kann spaeter typisiert auf `result.phi_hl` und `result.phi_cl`
  zugreifen.
- Regression kann Zwischenwerte weiter pruefen.

### Pruefung durch Nutzer

```powershell
python scripts\regression_chloe_golden.py
```

## S4: `HeatingCoolingLoadCalculator` nach `src/chloe/calculator.py` verschieben

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `HeatingCoolingLoadCalculator` nach `src/chloe/calculator.py` verschoben.
- `main.py` importiert `HeatingCoolingLoadCalculator` aus `chloe.calculator`.
- `src/chloe/__init__.py` exportiert `HeatingCoolingLoadCalculator`.
- `ChloeResult` nutzt fuer Typing den package-lokalen Calculator-Pfad.

### Ziel

Die eigentliche Rechenklasse aus `main.py` herausloesen.

Neue Datei:

```text
src/chloe/calculator.py
```

Enthaelt:

```python
HeatingCoolingLoadCalculator
```

`calculate(chloe_input) -> ChloeResult` bleibt die neue Rechen-API.
`heating_cooling_load(...)` bleibt vorerst als interne/kompatible Formel-Methode
bestehen.

### Nutzen

- `main.py` wird klein.
- Rechenlogik ist klar auffindbar.
- Spaetere Formel-Refactorings koennen gezielt in `calculator.py` passieren.

### Pruefung durch Nutzer

```powershell
python scripts\regression_chloe_golden.py
```

## S5: `run_chloe_simulation(...)` nach `src/chloe/service.py` verschieben

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `run_chloe_simulation(...)` nach `src/chloe/service.py` verschoben.
- `main.py` importiert `run_chloe_simulation` aus `chloe.service`.
- `src/chloe/__init__.py` exportiert `run_chloe_simulation`.

### Ziel

Den produktiven Einstiegspunkt fuer Lezbau ins Package verschieben.

Neue Datei:

```text
src/chloe/service.py
```

Enthaelt:

```python
def run_chloe_simulation(chloe_params) -> ChloeResult:
    ...
```

### Nutzen

Lezbau soll spaeter idealerweise nutzen:

```python
from chloe import run_chloe_simulation

result = run_chloe_simulation(chloe_input)
```

statt eigene Wrapper-Logik um den Calculator zu bauen.

### Pruefung durch Nutzer

```powershell
python scripts\regression_chloe_golden.py
```

## S6: Excel-Helfer nach `src/chloe/excel_io.py` verschieben

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `read_input_values(...)`, `build_rounded_outputs(...)` und `run_chloe(...)` nach `src/chloe/excel_io.py` verschoben.
- `run_chloe(...)` gibt weiterhin die Calculator-Instanz fuer die Golden-Regression zurueck.
- `main.py` wurde entfernt.
- `examples/run_exemplary.py` importiert `run_chloe` aus `chloe.excel_io`.
- `src/chloe/__init__.py` exportiert optional `read_input_values` und `run_chloe`.

### Ziel

Excel ist nicht produktiver Core, sondern nur Beispiel-/Regressionseingabe.

Neue Datei:

```text
src/chloe/excel_io.py
```

Enthaelt:

```python
read_input_values(...)
run_chloe(...)
```

### Nutzen

- Excel-Abhaengigkeit bleibt klar abgegrenzt.
- Produktiver Service kann ohne Excel genutzt werden.
- Golden Regression kann weiterhin `Exemplary_Inputs.xlsx` verwenden.

### Pruefung durch Nutzer

```powershell
python scripts\regression_chloe_golden.py
```

## S7: Public API in `src/chloe/__init__.py` definieren

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `src/chloe/__init__.py` definiert jetzt die oeffentliche Package-API.
- Produktiver Einstiegspunkt: `run_chloe_simulation(...)`.
- Strukturierte Datenobjekte: `ChloeInput`, `ChloeResult`.
- Excel-Helfer fuer Regression/Beispiel: `run_chloe(...)`, `read_input_values(...)`, `build_rounded_outputs(...)`.

### Ziel

Stabile Imports fuer Package-Nutzer und Lezbau bereitstellen.

Vorschlag:

```python
from .inputs import ChloeInput
from .results import ChloeResult
from .calculator import HeatingCoolingLoadCalculator
from .service import run_chloe_simulation
```

Optional, falls Excel-Helfer oeffentlich bleiben sollen:

```python
from .excel_io import run_chloe, read_input_values
```

### Nutzen

Saubere spaetere Nutzung:

```python
from chloe import ChloeInput, run_chloe_simulation
```

### Pruefung durch Nutzer

```powershell
python scripts\regression_chloe_golden.py
```

## S8: `main.py` entfernen

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `main.py` wurde entfernt, weil keine produktive Abhaengigkeit mehr darauf bestehen soll.
- Die echte API liegt jetzt ausschliesslich unter `src/chloe/`.
- Beispiele laufen ueber `examples/run_exemplary.py`.
- Regression laeuft ueber `scripts/regression_chloe_golden.py` und `chloe.excel_io`.

### Ziel

`main.py` soll nicht mehr Teil des aktiven Codes sein.

Neue und bestehende Nutzung soll direkt ueber `src/chloe` oder `examples/run_exemplary.py` laufen.

### Nutzen

- Keine doppelte Einstiegsschicht mehr.
- Package-Struktur ist eindeutig.

### Pruefung durch Nutzer

```powershell
python scripts\regression_chloe_golden.py
```

## S9: Regression-Skript auf Package-Imports ausrichten

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `scripts/regression_chloe_golden.py` nutzt jetzt `from chloe.excel_io import run_chloe`.
- Das Skript haengt nicht mehr von `main.py` und `runpy.run_path(...)` ab.
- Alte `--main`/`main.py`-Kompatibilitaet wurde entfernt.

### Ziel

`scripts/regression_chloe_golden.py` nutzt direkt die Package-Funktionen und haengt nicht mehr von `main.py` ab.

Ziel:

```python
from chloe.excel_io import run_chloe
```

oder:

```python
from chloe import run_chloe
```

falls `run_chloe` als Public API erhalten bleiben soll.

### Nutzen

- Regression prueft denselben Importpfad wie Package-Nutzer.
- Besser fuer PyPI und Lezbau-Vorbereitung.

### Pruefung durch Nutzer

```powershell
python scripts\regression_chloe_golden.py
```

## S10: Lezbau-Integration vorbereiten

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `src/chloe/__init__.py` exportiert nur noch die Lezbau/Core-API.
- Public Core API: `ChloeInput`, `ChloeResult`, `HeatingCoolingLoadCalculator`, `run_chloe_simulation`.
- Excel-Helfer bleiben in `chloe.excel_io`, werden aber nicht mehr ueber `from chloe import ...` exportiert.
- `main.py` wurde entfernt; Excel-Helfer bleiben explizit in `chloe.excel_io`.

### Ziel

Nach stabilem Package-Split kann Lezbau spaeter angepasst werden.

Aktueller Zielimport fuer Lezbau:

```python
from chloe import ChloeInput, run_chloe_simulation
```

In Lezbau kann `build_chloe_input_object(...)` spaeter `ChloeInput` bauen statt
direkt `HeatingCoolingLoadCalculator`.

### Wichtige Klarstellung

Produktiver Datenfluss ist nicht:

```text
Excel -> CHLOE -> Lezbau
```

sondern:

```text
User / Frontend / Django DB
  -> Lezbau Mapper
  -> ChloeInput
  -> run_chloe_simulation(...)
  -> ChloeResult
```

Excel bleibt nur fuer Golden Regression und Beispiel.

## Abschlusskriterium

Status: abgeschlossen. Der Nutzer hat nach S10 differences=0 bestaetigt.

Der Struktur-Split gilt als abgeschlossen, wenn:

- `main.py` entfernt ist;
- `src/chloe/` die echte Package-API enthaelt;
- `examples/run_exemplary.py` die alte Demo-Ausgabe uebernimmt;
- `scripts/regression_chloe_golden.py` erfolgreich laeuft;
- Nutzer bestaetigt:

```text
differences=0
```




