from lezbaucalc.building.model import BuildingModel

class BuildingCalc():
    buildingModel: BuildingModel

    def __init__(self, buildingModel: BuildingModel) -> None:
        self.buildingModel = buildingModel

    def calculateArea(self) -> float:
        return self.buildingModel.referenceArea * 1.5