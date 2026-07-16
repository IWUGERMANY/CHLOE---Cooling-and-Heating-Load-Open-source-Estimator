# CHLOE Packaging Notes

## Ziel

CHLOE ist jetzt als installierbares Python-Package vorbereitet. Der produktive
Import bleibt stabil:

```python
from chloe import ChloeInput, run_chloe_simulation
```

Der PyPI-/Package-Name ist aktuell:

```text
chloe-load-estimator
```

Der Import-Name bleibt:

```python
import chloe
```

## Warum Core ohne harte Excel-Abhaengigkeit

Lezbau braucht fuer die produktive Integration keine Excel-Dateien. Deshalb hat
das Core-Package keine Runtime-Dependency. Die Excel-Unterstuetzung fuer
Regression und Beispiel liegt als optionales Extra vor:

```powershell
pip install -e ".[excel]"
```

Damit bleibt die spaetere Lezbau-Installation schlanker.

## Lokale Installation fuer Entwicklung

Im CHLOE-Repo:

```powershell
cd "C:\Users\wail\Desktop\Projects\CHLOE---Cooling-and-Heating-Load-Open-source-Estimator"
python -m pip install -e ".[excel]"
```

Danach sollte dieser Import funktionieren:

```powershell
python -c "from chloe import ChloeInput, run_chloe_simulation; print(ChloeInput, run_chloe_simulation)"
```

## Regression nach Packaging-Aenderungen

Der Nutzer fuehrt aus:

```powershell
python scripts\regression_chloe_golden.py
```

Erwartung:

```text
differences=0
```

Optional fuer die Beispielausgabe:

```powershell
python examples\run_exemplary.py
```

## Build fuer PyPI spaeter

Wenn das Package veroeffentlicht werden soll:

```powershell
python -m pip install -e ".[dev]"
python -m build
```

Das erzeugt:

```text
dist/*.whl
dist/*.tar.gz
```

Upload auf PyPI erfolgt spaeter bewusst manuell.

## Lezbau requirements.txt spaeter

Solange CHLOE noch nicht auf PyPI aktualisiert ist, kann Lezbau temporaer auf den
Git-Branch zeigen:

```text
git+https://github.com/IWUGERMANY/CHLOE---Cooling-and-Heating-Load-Open-source-Estimator.git@chloe-optimization#egg=chloe-load-estimator
```

Nach PyPI-Release besser:

```text
chloe-load-estimator==0.2.0
```

Falls der finale PyPI-Name anders sein soll, muss `project.name` in
`pyproject.toml` vor dem Release angepasst werden.
