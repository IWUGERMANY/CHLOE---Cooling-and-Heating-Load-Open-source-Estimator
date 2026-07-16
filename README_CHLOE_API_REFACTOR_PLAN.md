# CHLOE API Refactoring Plan

## Ziel

CHLOE soll sich wie ein importierbares Library-/Service-Modul verhalten und in
Lezbau sauber ueber eine Funktion wie `run_chloe_simulation(...)` nutzbar sein.

Aktuell ist der `main`-Branch historisch als Skript aufgebaut:

```text
Exemplary_Inputs.xlsx -> main.py -> Konsolenausgabe
```

Fuer Lezbau und ein spaeteres Package ist das nicht ideal. Ziel ist:

```python
from chloe import run_chloe_simulation

result = run_chloe_simulation(chloe_params)
print(result.phi_hl)
print(result.phi_cl)
```

Die Konsolenausgabe gehoert nicht in die Core-API. Sie kann spaeter als Demo,
CLI oder Beispielskript existieren, aber nicht als Standardverhalten beim Import.

## Leitplanken

- Formeln bleiben unveraendert, solange keine fachliche Aenderung explizit
  geplant ist.
- Nach jedem Refactoring muss die Golden Regression mit
  `scripts/regression_chloe_golden.py` `differences=0` liefern.
- Lezbau-Kompatibilitaet ist wichtig: `chloe_params` kann aus einem Lezbau-
  Objekt, einer Dataclass, einem Pydantic-Modell oder einem Dict kommen.
- Die User-Regel gilt: Codex fuehrt keine Tests aus. Der Nutzer fuehrt die
  Regression selbst aus.

## Aktueller Stand

Bereits umgesetzt auf dem Optimierungsbranch:

- `main.py` rechnet nicht mehr direkt beim Import.
- `run_chloe(input_path="Exemplary_Inputs.xlsx")` existiert als erster
  importierbarer Einstiegspunkt fuer den Excel-Beispielfall.
- `print_results(...)` ist separiert und wird nur noch bei direktem Aufruf von
  `python main.py` genutzt.
- `scripts/regression_chloe_golden.py` ist kompatibel mit alter Skriptstruktur
  und neuer `run_chloe(...)`-Funktion.

## P1: ChloeInput einfuehren

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `ChloeInput` als gefrorene Dataclass in `main.py` eingefuehrt.
- `read_input_values(...)` gibt jetzt `ChloeInput` zurueck.
- `run_chloe(...)` nutzt `ChloeInput` und gibt das Input-Objekt zusaetzlich im Result-Dict zurueck.
- `ChloeInput.from_mapping(...)` und `ChloeInput.from_object(...)` bereiten die spaetere Lezbau-Integration vor.

### Ziel

Die Eingaben sollen nicht mehr implizit ueber lange Positionsargumente oder
Excel-Zellen fliessen, sondern explizit als strukturierter Input.

Vorschlag:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ChloeInput:
    net_floor_area: float
    u_windows: float
    u_walls: float
    u_roof: float
    u_base: float
    temp_adj_base: float
    temp_adj_walls_ug: float
    temp_adj_roof: float
    wall_area_og: float
    wall_area_ug: float
    total_window_area: float
    roof_area: float
    base_area: float
    t_set_heating: float
    thermal_bridges_supplement: float
    gross_building_vol: float
    net_building_vol: float
    reference_vol_name: str
    t_norm_ext_heating: float
    heat_rec_vent: float
    ach_min: float
    ach_infl: float
    ach_vent: float
    share_heated: float
    share_cooled: float
    share_mech_ventilated: float
    t_norm_ext_cooling_july: float
    t_norm_ext_cooling_sept: float
    gtot: float
    share_glass_frame: float
    t_set_cooling: float
    t_set_cooling_max: float
    phi_i_cooling_spec: float
```

### Nutzen

- weniger fehleranfaellig als Positionsargumente;
- besser fuer Lezbau-Mapping;
- einfacher zu testen;
- klarer API-Vertrag fuer Package-Nutzer.

## P2: ChloeResult einfuehren

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `ChloeResult` als gefrorene Dataclass in `main.py` eingefuehrt.
- `ChloeResult.from_calculator(...)` kapselt die Uebernahme der Calculator-Attribute.
- `build_rounded_outputs(...)` arbeitet jetzt auf `ChloeResult` statt direkt auf dem Calculator.
- `run_chloe(...)` gibt das explizite Ergebnisobjekt unter `result` zurueck.

### Ziel

Die Ergebnisse sollen nicht nur auf `self` des Calculators liegen, sondern als
explizites Ergebnisobjekt zurueckgegeben werden.

Vorschlag:

```python
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
```

### Nutzen

- Lezbau kann direkt `result.phi_hl` und `result.phi_cl` nutzen;
- Regression kann Zwischenwerte weiter vergleichen;
- weniger Kopplung an interne Calculator-Attribute.

## P3: `run_chloe_simulation(chloe_params)` in CHLOE bereitstellen

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `run_chloe_simulation(chloe_params) -> ChloeResult` in `main.py` eingefuehrt.
- Die Funktion akzeptiert `ChloeInput`, Dicts, Pydantic-Modelle oder einfache Objekte ueber `ChloeInput.from_object(...)`.
- `run_chloe(...)` bleibt als Excel-Helper fuer den Beispiel-/Regressionfall bestehen.

### Ziel

CHLOE soll selbst die Service-Funktion bereitstellen, die Lezbau spaeter nutzen
kann.

Vorschlag:

```python
def run_chloe_simulation(chloe_params) -> ChloeResult:
    chloe_input = ChloeInput.from_object(chloe_params)
    calculator = HeatingCoolingLoadCalculator()
    return calculator.calculate(chloe_input)
```

`from_object(...)` sollte akzeptieren:

- `ChloeInput`;
- Dict;
- Dataclass/Objekt mit `__dict__`;
- Pydantic-Objekt mit `model_dump()` oder `dict()`.

### Nutzen

- Lezbau muss weniger eigene Wrapper-Logik halten;
- klare Package-API;
- spaeter leichter fuer PyPI-Dokumentation.

## P4: Calculator in echte Rechenklasse umbauen

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `HeatingCoolingLoadCalculator.calculate(chloe_input) -> ChloeResult` eingefuehrt.
- `run_chloe_simulation(...)` nutzt jetzt `calculator.calculate(...)`.
- `run_chloe(...)` nutzt dieselbe Calculator-Instanz fuer Ergebnis und Regression.
- `heating_cooling_load(...)` bleibt als interne/kompatible Formel-Methode bestehen.

### Ziel

`HeatingCoolingLoadCalculator` soll rechnen, aber nicht dauerhaft als alleiniger
Ergebniscontainer dienen.

Zielstruktur:

```python
class HeatingCoolingLoadCalculator:
    def calculate(self, params: ChloeInput) -> ChloeResult:
        ...
        return ChloeResult(...)
```

Optional kann eine Kompatibilitaetsschicht erhalten bleiben, falls alte Nutzer
noch `heating_cooling_load(...)` aufrufen.

### Nutzen

- bessere Lesbarkeit;
- stabilerer API-Vertrag;
- weniger Seiteneffekte;
- einfacher fuer Lezbau-Integration.

## P5: Konsolenausgabe aus Core entfernen

### Status

Umgesetzt auf `chloe-optimization`.

Geaendert:

- `main.py` wurde nach dem Package-Split entfernt.
- Die historische Beispielausgabe liegt jetzt in `examples/run_exemplary.py`.
- Die Core-API bleibt `run_chloe(...)` fuer Excel-Regression und `run_chloe_simulation(...)` fuer strukturierte Inputs.

### Ziel

Keine `print()`-Ausgaben in der Core-API.

Moegliche Struktur:

```text
src/chloe/                 # Package-Code ohne print
examples/run_exemplary.py  # Demo-Skript mit print
```

Die alte Beispielausgabe liegt in `examples/run_exemplary.py`. Eine spaetere CLI kann separat ergaenzt werden, falls sie gebraucht wird.

### Nutzen

- sauber fuer Import in Lezbau;
- keine unerwarteten Konsolenausgaben in Backend-Prozessen;
- bessere Package-Qualitaet.

## P6: Regression nach jedem Schritt

Nach jedem Schritt soll der Nutzer ausfuehren:

```powershell
cd "C:\Users\wail\Desktop\Projects\CHLOE---Cooling-and-Heating-Load-Open-source-Estimator"
python scripts\regression_chloe_golden.py
```

Erwartung:

```text
differences=0
```

Wenn Abweichungen auftreten:

```text
regression_results/chloe_exemplary_comparison.xlsx
```

pruefen und erst danach weiter refactoren.

## P7: Lezbau-Integration vorbereiten

Wenn CHLOE intern stabil ist:

- Lezbau-Wrapper `lbbd/services/chloe_service.py` vereinfachen;
- statt eigenem Wrapper idealerweise `from chloe import run_chloe_simulation`
  nutzen;
- bestehendes Lezbau-Caching beibehalten oder bewusst verschieben;
- Lezbau-Regression separat ausfuehren.

## Offene Entscheidung

Noch zu entscheiden:

- Soll `ChloeResult` nur `phi_hl` und `phi_cl` enthalten oder auch alle
  Zwischenwerte?
- Soll CHLOE langfristig eine kleine CLI bekommen?

Status: P1 bis P7 sind umgesetzt. `main.py` wurde entfernt; `examples/run_exemplary.py` uebernimmt die Beispielausgabe.

