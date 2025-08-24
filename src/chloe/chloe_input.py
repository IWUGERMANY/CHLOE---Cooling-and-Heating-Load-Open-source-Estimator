class ChloeParams:
    def __init__(
        self,
        net_floor_area: float,  # Net floor area [m^2]
        u_windows: float,  # U-value of windows [W/(m^2*K)]
        u_walls: float,  # U-value of walls [W/(m^2*K)]
        u_roof: float,  # U-value of roof or ceiling against unheated [W/(m^2*K)]
        u_base: float,  # U-value of base or floor against unheated [W/(m^2*K)]
        temp_adj_base: float,
        # Temperature adjustment factor for the base - 0.3 for floor against ground, 0.5 for floor against unheated
        temp_adj_walls_ug: float,  # Temperature adjustment factor for walls below ground - 0.3
        temp_adj_roof: float,
        # Temperature adjustment factor for the roof - 1 for roof against air, 0.5 for ceiling against unheated
        wall_area_og: float,  # Wall area [m^2]
        wall_area_ug: float,  # Wall area underground [m^2]
        total_window_area: float,  # Total window area [m^2]
        roof_area: float,  # Roof area [m^2]
        base_area: float,  # Base area [m^2]
        t_set_heating: float,  # Set heating temperature [°C]
        thermal_bridges_supplement: float,  # Thermal bridges supplement [W/(m^2*K)]
        gross_building_vol: float,  # Gross building volume [m^3]
        net_building_vol: float,  # Net building volume [m^3]
        reference_vol_name: str,  # Choice of reference volume between gross and net volume [-]
        t_norm_ext_heating: float,  # Norm exterior temperature for the heating case [°C]
        heat_rec_vent: float,  # Heat recovery rate of the ventilation system [-]
        ach_min: float,
        # Minimum air change rate - 0.5 ("nicht bedarfsgeführt") or 0.45 ("bedarfsgeführt") for residential buildings standard value (given by DIN 18599-10, p.26-28) [h-1]
        ach_infl: float,
        # Air change rate through infiltration [h-1] - Passivhausanforderung erfüllt: 0.04 ; Neubau mit Dichtheitstest und raumlufttechnische Anlage: 0.07 ; Neubau mit Dichtheitstest ohne raumlufttechnische Anlage: 0.14 ; Neubau ohne Dichtheitstest: 0.28 ; Bestehendes Gebäude ohne Dichtheitstest: 0.42 ; Bestehndes Gebäude mit offensichtlichen Undichtheiten: 0.70
        ach_vent: float,
        # Air change rate through ventilation (Standard value 0.4 ("nicht bedarfsgeführt") or 0.35 ("bedarfsgeführt") according to DIN 18599-6) [h-1]
        share_heated: float,  # Share of net floor area which is heated [-]
        share_cooled: float,  # Share of net floor area which is cooled [-]
        share_mech_ventilated: float,  # Share of net floor area which is mechanically ventilated [-]
        # Cooling load specific inputs:
        t_norm_ext_cooling_july: float,
        # Norm exterior temperature in July for the cooling case [°C] (based on VDI 2078 p.142)
        t_norm_ext_cooling_sept: float,
        # Norm exterior temperature in September for the cooling case [°C] (based on VDI 2078 p.142)
        gtot: float,  # Solar factor [-] - from DIN 18599-2 Table 8
        share_glass_frame: float,  # Share of framing in the total window area, typically 0.3 [-]
        t_set_cooling: float,
        # Set cooling temperature [°C] - Standardwerte in DIN 18599-10, 25°C für Wohngebäude, für NWG siehe Tabelle 5 ab S.26
        t_set_cooling_max: float,
        # Maximum permissible indoor temperature during cooling period [°C] - Standardwerte in DIN 18599-10, 26°C für Wohngebäude, für NWG siehe Tabelle 5 ab S.26
        phi_i_cooling_spec: float,
    ):
        self.net_floor_area = net_floor_area
        self.u_windows = u_windows
        self.u_walls = u_walls
        self.u_roof = u_roof
        self.u_base = u_base
        self.temp_adj_base = temp_adj_base
        self.temp_adj_walls_ug = temp_adj_walls_ug
        self.temp_adj_roof = temp_adj_roof
        self.wall_area_og = wall_area_og
        self.wall_area_ug = wall_area_ug
        self.total_window_area = total_window_area
        self.roof_area = roof_area
        self.base_area = base_area
        self.t_set_heating = t_set_heating
        self.thermal_bridges_supplement = thermal_bridges_supplement
        self.gross_building_vol = gross_building_vol
        self.net_building_vol = net_building_vol
        self.reference_vol_name = reference_vol_name
        self.t_norm_ext_heating = t_norm_ext_heating
        self.heat_rec_vent = heat_rec_vent
        self.ach_min = ach_min
        self.ach_infl = ach_infl
        self.ach_vent = ach_vent
        self.share_heated = share_heated
        self.share_cooled = share_cooled
        self.share_mech_ventilated = share_mech_ventilated
        self.t_norm_ext_cooling_july = t_norm_ext_cooling_july
        self.t_norm_ext_cooling_sept = t_norm_ext_cooling_sept
        self.gtot = gtot
        self.share_glass_frame = share_glass_frame
        self.t_set_cooling = t_set_cooling
        self.t_set_cooling_max = t_set_cooling_max
        self.phi_i_cooling_spec = phi_i_cooling_spec