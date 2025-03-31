from lezbaucalc.building.model import BuildingModel
from lezbaucalc.building.calc import BuildingCalc

class TestBuildingCalculations:
    def test_reference_area_calc(self):
        model = BuildingModel(referenceArea=23)
        calc = BuildingCalc(model)
        assert calc.calculateArea() == 34.5, "calculated area should equal 34.5"
