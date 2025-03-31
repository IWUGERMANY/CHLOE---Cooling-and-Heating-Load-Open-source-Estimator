from dataclasses import dataclass

@dataclass
class BuildingModel():
    """BuildingModel just for kicks"""
   
    referenceArea: float

    def __str__(self) -> str:
        return "Reference-Area: {}".format(self.referenceArea)