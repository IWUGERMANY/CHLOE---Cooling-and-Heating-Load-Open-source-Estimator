class HeatingCoolingLoadCalculator:
    def heating_cooling_load(
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
        share_heated: float, # Share of net floor area which is heated [-]
        share_cooled: float, # Share of net floor area which is cooled [-]
        share_mech_ventilated: float, # Share of net floor area which is mechanically ventilated [-]
        # Cooling load specific inputs:
        t_norm_ext_cooling_july: float,  # Norm exterior temperature in July for the cooling case [°C] (based on VDI 2078 p.142)
        t_norm_ext_cooling_sept: float,  # Norm exterior temperature in September for the cooling case [°C] (based on VDI 2078 p.142)
        gtot: float,  # Solar factor [-] - from DIN 18599-2 Table 8
        share_glass_frame: float, # Share of framing in the total window area, typically 0.3 [-]
        t_set_cooling: float,  # Set cooling temperature [°C] - Standardwerte in DIN 18599-10, 25°C für Wohngebäude, für NWG siehe Tabelle 5 ab S.26
        t_set_cooling_max: float,  # Maximum permissible indoor temperature during cooling period [°C] - Standardwerte in DIN 18599-10, 26°C für Wohngebäude, für NWG siehe Tabelle 5 ab S.26
        phi_i_cooling_spec: float,  # Internal loads for the cooling case [W/m^2] - SFH: 45 Wh/(m^2.d) or 1.875 W/m^2 - MFH 90 Wh/(m^2.d) or 3.75 W/m^2 according to DIN 18599-10
    ):

        # Set reference volume of the building [m^3]
        if reference_vol_name == "net":
            self.reference_vol_value: float = net_building_vol
        elif reference_vol_name == "gross":

            self.reference_vol_value = gross_building_vol
        else:  # By default the net volume will be considered
            self.reference_vol_value = net_building_vol

        # Mean indoor temperature for cooling, according to VDI 2078, p.139
        self.t_i_cooling: float = (t_set_cooling_max + t_set_cooling - 2) / 2

        ########## Heat transmission losses ##########

        # Heat transmission losses through building components to exterior, including heat bridges [W/K]
        self.h_tr_hb: float = (
            ((u_walls + thermal_bridges_supplement) * wall_area_og)
            + ((u_windows + thermal_bridges_supplement) * total_window_area)
            + ((u_roof + thermal_bridges_supplement) * roof_area * temp_adj_roof)
            + ((u_base + thermal_bridges_supplement) * base_area * temp_adj_base)
            + (
                (u_walls + thermal_bridges_supplement)
                * wall_area_ug
                * temp_adj_walls_ug
            )
        )

        # Total heat transmission losses - Heating load case [W]
        self.phi_t_heating: float = self.h_tr_hb * (t_set_heating - t_norm_ext_heating)

        # Total heat transmission losses - Cooling load case [W]
        if t_norm_ext_cooling_july >= self.t_i_cooling:
            self.phi_t_cooling_july: float = self.h_tr_hb * (
                t_norm_ext_cooling_july - self.t_i_cooling
            )

        else:
            self.phi_t_cooling_july = 0
        if t_norm_ext_cooling_sept >= self.t_i_cooling:
            self.phi_t_cooling_sept: float = self.h_tr_hb * (
                t_norm_ext_cooling_sept - self.t_i_cooling
            )
        else:
            self.phi_t_cooling_sept = 0

        ########## Heat losses through ventilation ##########

        # Define air change rate through windows
        self.ach_win: float = max(0, ach_min - ach_vent - ach_infl)

        # Define air inflow temperature from ventilation system, including heat recovery
        # Assumption: exhaust air temperature (Abluft) equals the interior setpoint temperature
        # Heating case
        self.t_rec_heating: float = t_norm_ext_heating + heat_rec_vent * (
            t_set_heating - t_norm_ext_heating
        )
        # Cooling case
        self.t_rec_cooling_july: float = t_norm_ext_cooling_july - heat_rec_vent * (
            t_norm_ext_cooling_july - self.t_i_cooling
        )
        self.t_rec_cooling_sept: float = t_norm_ext_cooling_sept - heat_rec_vent * (
            t_norm_ext_cooling_sept - self.t_i_cooling
        )

        ## If more air change occurs through infiltration than the minimum ventilation requirements, then only ventilation losses through infiltration are considered (0.34 is the air constant)
        if ach_infl >= ach_min:
            self.phi_v_tot_heating: float = (
                0.34
                * self.reference_vol_value
                * (ach_infl * (t_set_heating - t_norm_ext_heating))
            )
            if t_norm_ext_cooling_july >= self.t_i_cooling:
                self.phi_v_tot_cooling_july: float = (
                    0.34
                    * self.reference_vol_value
                    * (ach_infl * (t_norm_ext_cooling_july - self.t_i_cooling))
                )
            else:
                self.phi_v_tot_cooling_july = 0
            if t_norm_ext_cooling_sept >= self.t_i_cooling:
                self.phi_v_tot_cooling_sept: float = (
                    0.34
                    * self.reference_vol_value
                    * (ach_infl * (t_norm_ext_cooling_sept - self.t_i_cooling))
                )
            else:
                self.phi_v_tot_cooling_sept = 0

        ## If infiltration air change is lower than the minimum ventilation requirements, window openings and mechanical ventilation (if present) are considered
        else:
            ## Ventilation losses through infiltration
            self.phi_v_infl_heating: float = (
                0.34 * self.reference_vol_value
                * (ach_infl * (t_set_heating - t_norm_ext_heating))
            )

            if t_norm_ext_cooling_july >= self.t_i_cooling:
                self.phi_v_infl_cooling_july: float = (
                    0.34
                    * self.reference_vol_value
                    * (ach_infl * (t_norm_ext_cooling_july - self.t_i_cooling))
                )
            else:
                self.phi_v_infl_cooling_july = 0

            if t_norm_ext_cooling_sept >= self.t_i_cooling:
                self.phi_v_infl_cooling_sept: float = (
                    0.34
                    * self.reference_vol_value
                    * (ach_infl * (t_norm_ext_cooling_sept - self.t_i_cooling))
                )
            else:
                self.phi_v_infl_cooling_sept = 0

            ## Ventilation losses through ventilation system
            self.phi_v_vent_heating: float = (
                (0.34 * self.reference_vol_value * share_mech_ventilated * (ach_vent * (t_set_heating - self.t_rec_heating))
                + (0.34 * self.reference_vol_value * (1-share_mech_ventilated) * (ach_vent * (t_set_heating - t_norm_ext_heating))))
            )

            if self.t_rec_cooling_july >= self.t_i_cooling:
                self.phi_v_vent_cooling_july: float = (
                    (0.34 * self.reference_vol_value * share_mech_ventilated * (ach_vent * (self.t_rec_cooling_july - self.t_i_cooling))
                    + 0.34 * self.reference_vol_value * (1-share_mech_ventilated) * (ach_vent * (t_norm_ext_cooling_july - self.t_i_cooling)))
                )
            else:
                self.phi_v_vent_cooling_july = 0

            if self.t_rec_cooling_sept >= self.t_i_cooling:
                self.phi_v_vent_cooling_sept: float = (
                    (0.34 * self.reference_vol_value * share_mech_ventilated * (ach_vent * (self.t_rec_cooling_sept - self.t_i_cooling))
                        + 0.34 * self.reference_vol_value * (1 - share_mech_ventilated) * (ach_vent * (t_norm_ext_cooling_sept - self.t_i_cooling)))
                )
            else:
                self.phi_v_vent_cooling_sept = 0

            ## Ventilation losses through window openings
            self.phi_v_win_heating: float = (
                0.34
                * self.reference_vol_value
                * (self.ach_win * (t_set_heating - t_norm_ext_heating))
            )

            if t_norm_ext_cooling_july >= self.t_i_cooling:
                self.phi_v_win_cooling_july: float = (
                    0.34
                    * self.reference_vol_value
                    * (self.ach_win * (t_norm_ext_cooling_july - self.t_i_cooling))
                )
            else:
                self.phi_v_win_cooling_july = 0

            if t_norm_ext_cooling_sept >= self.t_i_cooling:
                self.phi_v_win_cooling_sept: float = (
                    0.34
                    * self.reference_vol_value
                    * (self.ach_win * (t_norm_ext_cooling_sept - self.t_i_cooling))
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

        ########## Cooling load - Heat gains from solar radiation through windows ##########

        # Average maximum irradiation on South-East and South-West oriented facades in July and September [W/m²]
        self.is_max_se_july: float = 690
        self.is_max_se_sept: float = 785
        self.is_max_sw_july: float = 690
        self.is_max_sw_sept: float = 791

        # For the cooling load calculation, it is assumed that two facades of the building are illumnated simultaneously (SE and SW facades), and that the total window area is evenly distributed on all facades.
        # Surface of windows which is illuminated by the sun [m2]
        self.window_area_illuminated_se: float = total_window_area / 4
        self.window_area_illuminated_sw: float = total_window_area / 4


        # Solar gains through windows in July and September [w]

        self.phi_solar_se_july: float = (
            self.window_area_illuminated_se * self.is_max_se_july * gtot * share_glass_frame
        )
        self.phi_solar_sw_july: float = (
            self.window_area_illuminated_sw * self.is_max_sw_july * gtot * share_glass_frame
        )
        self.phi_solar_tot_july: float = self.phi_solar_se_july + self.phi_solar_sw_july

        self.phi_solar_se_sept: float = (
            self.window_area_illuminated_se * self.is_max_se_sept * gtot * share_glass_frame
        )
        self.phi_solar_sw_sept: float = (
            self.window_area_illuminated_sw * self.is_max_sw_sept * gtot * share_glass_frame
        )
        self.phi_solar_tot_sept: float = self.phi_solar_se_sept + self.phi_solar_sw_sept

        ### Internal loads
        self.phi_i_cooling = phi_i_cooling_spec * net_floor_area

        ########## Total loads [kW] ##########
        # Heating load
        self.phi_hl: float = (self.phi_t_heating + self.phi_v_tot_heating) * share_heated

        # Cooling load July
        self.phi_cl_july: float = (
            self.phi_t_cooling_july
            + self.phi_v_tot_cooling_july
            + self.phi_solar_tot_july
            + self.phi_i_cooling
        ) * share_cooled
        # Cooling load Sept
        self.phi_cl_sept: float = (
            self.phi_t_cooling_sept
            + self.phi_v_tot_cooling_sept
            + self.phi_solar_tot_sept
            + self.phi_i_cooling
        ) * share_cooled
        # Max Cooling load
        self.phi_cl: float = max(self.phi_cl_july, self.phi_cl_sept)




############################################
#### Import inputs from Inputs.xslx
############################################

calculator = HeatingCoolingLoadCalculator()
import openpyxl
# Load the Excel workbook
workbook = openpyxl.load_workbook('Inputs.xlsx')
# Select the appropriate worksheet
worksheet = workbook.active
# Define the column name
column_name = 'B'
# Read input parameters from the Excel file
parameters = [
    'net_floor_area', 'u_windows', 'u_walls', 'u_roof', 'u_base', 'temp_adj_base', 'temp_adj_walls_ug',
    'temp_adj_roof', 'wall_area_og', 'wall_area_ug', 'total_window_area', 'roof_area', 'base_area',
    't_set_heating', 'thermal_bridges_supplement', 'gross_building_vol', 'net_building_vol', 'reference_vol_name',
    't_norm_ext_heating', 'heat_rec_vent', 'ach_min', 'ach_infl', 'ach_vent', 'share_heated', 'share_cooled',
    'share_mech_ventilated', 't_norm_ext_cooling_july', 't_norm_ext_cooling_sept', 'gtot', 'share_glass_frame', 't_set_cooling',
    't_set_cooling_max', 'phi_i_cooling_spec'
]
# Read the values from the Excel file
input_values = {}
for i, parameter in enumerate(parameters, start=2):
    cell_value = worksheet[f'{column_name}{i}'].value
    input_values[parameter] = cell_value
# Call the heating_cooling_load method with the input parameters
calculator.heating_cooling_load(**input_values)





# Access the calculated heating load
heating_cooling_load_result = round(calculator.phi_hl)
heating_cooling_load_result2 = round(calculator.phi_v_tot_heating)
heating_cooling_load_result3 = round(calculator.phi_solar_tot_july)
heating_cooling_load_result4 = round(calculator.phi_t_cooling_july)
heating_cooling_load_result5 = round(calculator.phi_v_tot_cooling_july)
heating_cooling_load_result6 = round(calculator.phi_t_heating)
heating_cooling_load_result7 = round(calculator.phi_cl)
heating_cooling_load_result8 = round(calculator.phi_solar_tot_sept)
heating_cooling_load_result9 = round(calculator.phi_t_cooling_sept)
heating_cooling_load_result10 = round(calculator.phi_v_tot_cooling_sept)
heating_cooling_load_result11 = round(calculator.phi_cl_july)
heating_cooling_load_result12 = round(calculator.phi_cl_sept)
heating_cooling_load_result13 = round(calculator.phi_i_cooling)


# Print the result
print(f"Results - Heating Load")
print(f"Total Heating Load: {heating_cooling_load_result} W")
print(f"Ventilation losses (heating): {heating_cooling_load_result2} W")
print(f"Transmission losses (heating): {heating_cooling_load_result6} W")

print(f" ")
print(f"Results - Cooling Load")
print(f"Total Cooling load: {heating_cooling_load_result7} W")
print(f"Total Cooling load July: {heating_cooling_load_result11} W")
print(f"Total Cooling load September: {heating_cooling_load_result12} W")
print(f"-------------")
print(f"Solar heat gains July (cooling): {heating_cooling_load_result3} W")
print(f"Transmission heat gains July (cooling): {heating_cooling_load_result4} W")
print(f"Ventilation heat gains July (cooling): {heating_cooling_load_result5} W")
print(f"Internal gains (cooling): {heating_cooling_load_result13} W")
print(f"-------------")
print(f"Solar heat gains Sept (cooling): {heating_cooling_load_result8} W")
print(f"Transmission heat gains Sept (cooling): {heating_cooling_load_result9} W")
print(f"Ventilation heat gains Sept (cooling): {heating_cooling_load_result10} W")
print(f"Internal gains (cooling): {heating_cooling_load_result13} W")
print(f"-------------")


