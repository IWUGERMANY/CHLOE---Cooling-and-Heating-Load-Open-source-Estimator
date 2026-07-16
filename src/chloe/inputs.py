"""Input contract for CHLOE simulations."""

from __future__ import annotations

from dataclasses import dataclass, fields


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

    @classmethod
    def from_mapping(cls, values: dict) -> "ChloeInput":
        """Build CHLOE input from a mapping with CHLOE parameter names."""
        return cls(**{parameter: values[parameter] for parameter in PARAMETERS})

    @classmethod
    def from_object(cls, value) -> "ChloeInput":
        """Build CHLOE input from dict, dataclass, Pydantic or plain object."""
        if isinstance(value, cls):
            return value
        if hasattr(value, "model_dump"):
            raw = value.model_dump()
        elif hasattr(value, "dict"):
            raw = value.dict()
        elif isinstance(value, dict):
            raw = value
        elif hasattr(value, "__dict__"):
            raw = vars(value)
        else:
            raise TypeError(f"Unsupported CHLOE input type: {type(value)!r}")
        return cls.from_mapping(raw)


PARAMETERS = [field.name for field in fields(ChloeInput)]
