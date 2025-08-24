#TODO: Chloe als pypi module anlegen.

class HeatingCoolingLoadCalculator:
    def __init__(
        self,
        net_floor_area: float,  # Net floor area [m^2]
        u_windows: float,  # U-value of windows [W/(m^2*K)]
        u_walls: float,  # U-value of walls [W/(m^2*K)]
        u_roof: float,  # U-value of roof or ceiling against unheated [W/(m^2*K)]
        u_base: float,  # U-value of base or floor against unheated [W/(m^2*K)]
        temp_adj_base: float,  # Temperature adjustment factor for the base - 0.3 for floor against ground, 0.5 for floor against unheated
        temp_adj_walls_ug: float,  # Temperature adjustment factor for walls below ground - 0.3
        temp_adj_roof: float,  # Temperature adjustment factor for the roof - 1 for roof against air, 0.5 for ceiling against unheated
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
        ach_min: float,  # Minimum air change rate - 0.5 ("nicht bedarfsgeführt") or 0.45 ("bedarfsgeführt") for residential buildings standard value (given by DIN 18599-10, p.26-28) [h-1]
        ach_infl: float,  # Air change rate through infiltration [h-1] - Passivhausanforderung erfüllt: 0.04 ; Neubau mit Dichtheitstest und raumlufttechnische Anlage: 0.07 ; Neubau mit Dichtheitstest ohne raumlufttechnische Anlage: 0.14 ; Neubau ohne Dichtheitstest: 0.28 ; Bestehendes Gebäude ohne Dichtheitstest: 0.42 ; Bestehndes Gebäude mit offensichtlichen Undichtheiten: 0.70
        ach_vent: float,  # Air change rate through ventilation (Standard value 0.4 ("nicht bedarfsgeführt") or 0.35 ("bedarfsgeführt") according to DIN 18599-6) [h-1]
        share_heated: float,  # Share of net floor area which is heated [-]
        share_cooled: float,  # Share of net floor area which is cooled [-]
        share_mech_ventilated: float,  # Share of net floor area which is mechanically ventilated [-]
        # Cooling load specific inputs:
        t_norm_ext_cooling_july: float,  # Norm exterior temperature in July for the cooling case [°C] (based on VDI 2078 p.142)
        t_norm_ext_cooling_sept: float,  # Norm exterior temperature in September for the cooling case [°C] (based on VDI 2078 p.142)
        gtot: float,  # Solar factor [-] - from DIN 18599-2 Table 8
        share_glass_frame: float,  # Share of framing in the total window area, typically 0.3 [-]
        t_set_cooling: float,  # Set cooling temperature [°C] - Standardwerte in DIN 18599-10, 25°C für Wohngebäude, für NWG siehe Tabelle 5 ab S.26
        t_set_cooling_max: float,  # Maximum permissible indoor temperature during cooling period [°C] - Standardwerte in DIN 18599-10, 26°C für Wohngebäude, für NWG siehe Tabelle 5 ab S.26
        phi_i_cooling_spec: float,  # Internal loads for the cooling case [W/m^2] - SFH: 45 Wh/(m^2.d) or 1.875 W/m^2 - MFH 90 Wh/(m^2.d) or 3.75 W/m^2 according to DIN 18599-10
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
        # Cooling load specific inputs:
        self.t_norm_ext_cooling_july = t_norm_ext_cooling_july
        self.t_norm_ext_cooling_sept = t_norm_ext_cooling_sept
        self.gtot = gtot
        self.share_glass_frame = share_glass_frame
        self.t_set_cooling = t_set_cooling
        self.t_set_cooling_max = t_set_cooling_max
        self.phi_i_cooling_spec = phi_i_cooling_spec

    def calculate_reference_volume_building(self):
        volume_map = {"net": self.net_building_vol, "gross": self.gross_building_vol}
        self.reference_vol_value = volume_map.get(
            self.reference_vol_name, self.net_building_vol
        )

    def calculate_heat_transmission_losses(self):
        def _u_with_thermal_bridges_supplement(u_value: float) -> float:
            return u_value + self.thermal_bridges_supplement

        self.h_tr_hb: float = sum(
            [
                _u_with_thermal_bridges_supplement(self.u_walls) * self.wall_area_og,
                _u_with_thermal_bridges_supplement(self.u_windows)
                * self.total_window_area,
                _u_with_thermal_bridges_supplement(self.u_roof)
                * self.roof_area
                * self.temp_adj_roof,
                _u_with_thermal_bridges_supplement(self.u_base)
                * self.base_area
                * self.temp_adj_base,
                _u_with_thermal_bridges_supplement(self.u_walls)
                * self.wall_area_ug
                * self.temp_adj_walls_ug,
            ]
        )

    def calculate_total_heat_transmission_losses_cooling(self):
        def calculate_and_set_phi_t_cooling(month: str) -> None:
            if month == "july":
                ext_temp = self.t_norm_ext_cooling_july
                attr_name = "phi_t_cooling_july"
            elif month == "september":
                ext_temp = self.t_norm_ext_cooling_sept
                attr_name = "phi_t_cooling_sept"
            else:
                raise ValueError(
                    "Ungültiger Monat: nur 'july' oder 'september' erlaubt."
                )

            value = (
                self.h_tr_hb * (ext_temp - self.t_i_cooling)
                if ext_temp >= self.t_i_cooling
                else 0.0
            )
            setattr(self, attr_name, value)

        calculate_and_set_phi_t_cooling("july")
        calculate_and_set_phi_t_cooling("september")

    def calculate_heat_transmission_losses_heating(self):
        self.phi_t_heating: float = self.h_tr_hb * (
            self.t_set_heating - self.t_norm_ext_heating
        )

    def calculate_internal_loads(self):
        self.phi_i_cooling = self.phi_i_cooling_spec * self.net_floor_area

    def calculate_solar_gains_through_windows(self):
        self.phi_solar_se_july: float = (
            self.window_area_illuminated_se
            * self.is_max_se_july
            * self.gtot
            * self.share_glass_frame
        )
        self.phi_solar_sw_july: float = (
            self.window_area_illuminated_sw
            * self.is_max_sw_july
            * self.gtot
            * self.share_glass_frame
        )
        self.phi_solar_tot_july: float = self.phi_solar_se_july + self.phi_solar_sw_july

        self.phi_solar_se_sept: float = (
            self.window_area_illuminated_se
            * self.is_max_se_sept
            * self.gtot
            * self.share_glass_frame
        )
        self.phi_solar_sw_sept: float = (
            self.window_area_illuminated_sw
            * self.is_max_sw_sept
            * self.gtot
            * self.share_glass_frame
        )
        self.phi_solar_tot_sept: float = self.phi_solar_se_sept + self.phi_solar_sw_sept

    def set_average_max_irradiation_facades(self):
        self.is_max_se_july: float = 690
        self.is_max_se_sept: float = 785
        self.is_max_sw_july: float = 690
        self.is_max_sw_sept: float = 791

    def calculate_ventilation_losses_with_infiltration(self):
        if self.ach_infl >= self.ach_min:
            self.phi_v_tot_heating: float = (
                0.34
                * self.reference_vol_value
                * (self.ach_infl * (self.t_set_heating - self.t_norm_ext_heating))
            )
            if self.t_norm_ext_cooling_july >= self.t_i_cooling:
                self.phi_v_tot_cooling_july: float = (
                    0.34
                    * self.reference_vol_value
                    * (
                        self.ach_infl
                        * (self.t_norm_ext_cooling_july - self.t_i_cooling)
                    )
                )
            else:
                self.phi_v_tot_cooling_july = 0
            if self.t_norm_ext_cooling_sept >= self.t_i_cooling:
                self.phi_v_tot_cooling_sept: float = (
                    0.34
                    * self.reference_vol_value
                    * (
                        self.ach_infl
                        * (self.t_norm_ext_cooling_sept - self.t_i_cooling)
                    )
                )
            else:
                self.phi_v_tot_cooling_sept = 0

        ## If infiltration air change is lower than the minimum ventilation requirements, window openings and mechanical ventilation (if present) are considered
        else:
            ## Ventilation losses through infiltration
            self.phi_v_infl_heating: float = (
                0.34
                * self.reference_vol_value
                * (self.ach_infl * (self.t_set_heating - self.t_norm_ext_heating))
            )

            if self.t_norm_ext_cooling_july >= self.t_i_cooling:
                self.phi_v_infl_cooling_july: float = (
                    0.34
                    * self.reference_vol_value
                    * (
                        self.ach_infl
                        * (self.t_norm_ext_cooling_july - self.t_i_cooling)
                    )
                )
            else:
                self.phi_v_infl_cooling_july = 0

            if self.t_norm_ext_cooling_sept >= self.t_i_cooling:
                self.phi_v_infl_cooling_sept: float = (
                    0.34
                    * self.reference_vol_value
                    * (
                        self.ach_infl
                        * (self.t_norm_ext_cooling_sept - self.t_i_cooling)
                    )
                )
            else:
                self.phi_v_infl_cooling_sept = 0

            ## Ventilation losses through ventilation system
            self.phi_v_vent_heating: float = (
                0.34
                * self.reference_vol_value
                * self.share_mech_ventilated
                * (self.ach_vent * (self.t_set_heating - self.t_rec_heating))
                + (
                    0.34
                    * self.reference_vol_value
                    * (1 - self.share_mech_ventilated)
                    * (self.ach_vent * (self.t_set_heating - self.t_norm_ext_heating))
                )
            )

            if self.t_rec_cooling_july >= self.t_i_cooling:
                self.phi_v_vent_cooling_july: float = (
                    0.34
                    * self.reference_vol_value
                    * self.share_mech_ventilated
                    * (self.ach_vent * (self.t_rec_cooling_july - self.t_i_cooling))
                    + 0.34
                    * self.reference_vol_value
                    * (1 - self.share_mech_ventilated)
                    * (
                        self.ach_vent
                        * (self.t_norm_ext_cooling_july - self.t_i_cooling)
                    )
                )
            else:
                self.phi_v_vent_cooling_july = 0

            if self.t_rec_cooling_sept >= self.t_i_cooling:
                self.phi_v_vent_cooling_sept: float = (
                    0.34
                    * self.reference_vol_value
                    * self.share_mech_ventilated
                    * (self.ach_vent * (self.t_rec_cooling_sept - self.t_i_cooling))
                    + 0.34
                    * self.reference_vol_value
                    * (1 - self.share_mech_ventilated)
                    * (
                        self.ach_vent
                        * (self.t_norm_ext_cooling_sept - self.t_i_cooling)
                    )
                )
            else:
                self.phi_v_vent_cooling_sept = 0

            ## Ventilation losses through window openings
            self.phi_v_win_heating: float = (
                0.34
                * self.reference_vol_value
                * (self.ach_win * (self.t_set_heating - self.t_norm_ext_heating))
            )

            if self.t_norm_ext_cooling_july >= self.t_i_cooling:
                self.phi_v_win_cooling_july: float = (
                    0.34
                    * self.reference_vol_value
                    * (self.ach_win * (self.t_norm_ext_cooling_july - self.t_i_cooling))
                )
            else:
                self.phi_v_win_cooling_july = 0

            if self.t_norm_ext_cooling_sept >= self.t_i_cooling:
                self.phi_v_win_cooling_sept: float = (
                    0.34
                    * self.reference_vol_value
                    * (self.ach_win * (self.t_norm_ext_cooling_sept - self.t_i_cooling))
                )
            else:
                self.phi_v_win_cooling_sept = 0

            ## Total ventilation losses in [W]
            self.phi_v_tot_heating = (
                self.phi_v_infl_heating
                + self.phi_v_vent_heating
                + self.phi_v_win_heating
            )

            self.phi_v_tot_cooling_july = (
                self.phi_v_infl_cooling_july
                + self.phi_v_vent_cooling_july
                + self.phi_v_win_cooling_july
            )
            self.phi_v_tot_cooling_sept = (
                self.phi_v_infl_cooling_sept
                + self.phi_v_vent_cooling_sept
                + self.phi_v_win_cooling_sept
            )

    def calculate_cooling_case(self):
        self.t_rec_cooling_july: float = (
            self.t_norm_ext_cooling_july
            - self.heat_rec_vent * (self.t_norm_ext_cooling_july - self.t_i_cooling)
        )
        self.t_rec_cooling_sept: float = (
            self.t_norm_ext_cooling_sept
            - self.heat_rec_vent * (self.t_norm_ext_cooling_sept - self.t_i_cooling)
        )

    def calculate_air_change_rate_through_windows(self):
        self.ach_win: float = max(0, self.ach_min - self.ach_vent - self.ach_infl)

    def calculate_cooling_load_sept(self):
        self.phi_cl_sept: float = (
            self.phi_t_cooling_sept
            + self.phi_v_tot_cooling_sept
            + self.phi_solar_tot_sept
            + self.phi_i_cooling
        ) * self.share_cooled

    def calculate_cooling_load_july(self):
        self.phi_cl_july: float = (
            self.phi_t_cooling_july
            + self.phi_v_tot_cooling_july
            + self.phi_solar_tot_july
            + self.phi_i_cooling
        ) * self.share_cooled

    def calculate_phi_cl(self):
        self.phi_cl: float = max(self.phi_cl_july, self.phi_cl_sept)

    def calculate_phi_hl(self):
        self.phi_hl: float = (
            self.phi_t_heating + self.phi_v_tot_heating
        ) * self.share_heated

    def heating_cooling_load(self):
        # Set reference volume of the building [m^3]
        self.calculate_reference_volume_building()

        # Mean indoor temperature for cooling, according to VDI 2078, p.139
        self.t_i_cooling: float = (self.t_set_cooling_max + self.t_set_cooling - 2) / 2

        ########## Heat transmission losses ##########

        # Heat transmission losses through building components to exterior, including heat bridges [W/K]
        self.calculate_heat_transmission_losses()

        # Total heat transmission losses - Heating load case [W]
        self.calculate_heat_transmission_losses_heating()

        # Total heat transmission losses - Cooling load case [W]
        self.calculate_total_heat_transmission_losses_cooling()

        ########## Heat losses through ventilation ##########

        # Define air change rate through windows
        self.calculate_air_change_rate_through_windows()

        # Define air inflow temperature from ventilation system, including heat recovery
        # Assumption: exhaust air temperature (Abluft) equals the interior setpoint temperature
        # Heating case
        self.t_rec_heating: float = self.t_norm_ext_heating + self.heat_rec_vent * (
            self.t_set_heating - self.t_norm_ext_heating
        )
        # Cooling case
        self.calculate_cooling_case()

        ## If more air change occurs through infiltration than the minimum ventilation requirements, then only ventilation losses through infiltration are considered (0.34 is the air constant)
        self.calculate_ventilation_losses_with_infiltration()

        ########## Cooling load - Heat gains from solar radiation through windows ##########

        # Average maximum irradiation on South-East and South-West oriented facades in July and September [W/m²]
        self.set_average_max_irradiation_facades()

        # For the cooling load calculation, it is assumed that two facades of the building are illumnated simultaneously (SE and SW facades), and that the total window area is evenly distributed on all facades.
        # Surface of windows which is illuminated by the sun [m2]
        self.window_area_illuminated_se: float = self.total_window_area / 4
        self.window_area_illuminated_sw: float = self.total_window_area / 4

        # Solar gains through windows in July and September [w]

        self.calculate_solar_gains_through_windows()

        ### Internal loads
        self.calculate_internal_loads()

        ########## Total loads [kW] ##########
        # Heating load
        self.calculate_phi_hl()
        # Cooling load July
        self.calculate_cooling_load_july()
        # Cooling load Sept
        self.calculate_cooling_load_sept()
        # Max Cooling load
        self.calculate_phi_cl()
        return round(self.phi_hl), round(self.phi_cl)
