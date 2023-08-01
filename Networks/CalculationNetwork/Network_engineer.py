
import pandas as pd


class ExcelLoader:
    def __init__(self, system_type:str, input_settings_df:pd) -> None:
        """
        load df from excel and covert to dict
        """
        self.system_type = system_type
        self.input_settings_df = input_settings_df

    def get_medium_dict(self):
        df_medium = self.input_settings_df["medium_property"]
        df_medium = df_medium.set_index("system_type").to_dict("index")
        self.df_medium = df_medium[self.system_type]
        return self.df_medium

    def get_diameter_list(self):
        """
        diameter_type - name of excel sheet (ducts_round,pipes)
        """
        df_medium = self.get_medium_dict()
        diameter_sheet = df_medium["diameter_type"]
        df_diameter = self.input_settings_df[diameter_sheet]
        diameter_list = df_diameter["diameter"].values
        return diameter_list

    def get_default_velocity(self, network_branch_type):
        """
        type branch, main_root
        """
        self.get_medium_dict()
        if network_branch_type == "branch":
            velocity = self.df_medium["velocity_branch_normal"]
        else:
            velocity = self.df_medium["velocity_root_normal"]
        return velocity

    def __repr__(self) -> str:
        return self.__class__.__name__


class DiameterSelecter:
    def __init__(self, flow:float, default_velocity:float) -> int:
        """calculate diameter by flow and velocity.
            select standart diameter from diameter list

        Args:
            flow (float): _description_
            default_velocity (float): _description_

        Returns:
            int: standart diameter
        """
        self.flow = flow
        self.default_velocity = default_velocity

    def get_area(self):
        area = self.flow/(3600*self.default_velocity)
        return area

    def calculate_default_diameter(self):
        area = self.get_area()
        diameter = 2*(area/3.14)**0.5
        diameter = diameter*1000
        return diameter

    def choose_standart_diameter(self, diameter_list:list)->int:
        """select diameter from diametr list

        Args:
            diameter_list (list): from excel

        Returns:
            int: standart diameter
        """

        default_diameter = self.calculate_default_diameter()
        min_diam = [diam for diam in diameter_list if default_diameter < diam]
        if min_diam:
            return min(min_diam)
        else:
            return int(default_diameter)

    def __repr__(self) -> str:
        return self.__class__.__name__


class FlowCalculation:
    def __init__(self, medium_loader: dict) ->float:
        """
        calculate flow from power
        flow -m3/h
        power -kW
        """
        self.medium_loader = medium_loader

        for k, v in self.medium_loader.items():
            setattr(self, k, v)

    def __is_need_convert_power_to_flow(self):
        if self.t_max and self.t_min and self.power_or_flow == "power":
            return True
        else:
            return False

    def calculate_flow(self, power):
        if self.__is_need_convert_power_to_flow():
            dt = self.t_max-self.t_min
            power_kW = power/1000
            flow = power_kW/dt*self.density*self.heat_capacity*3.6
            return flow
        else:
            return power

    def __repr__(self) -> str:
        return self.__class__.__name__


class DropPressure:
    def __init__(self, medium_property: dict, diameter:float, flow:float) -> None:
        """
        get presure drop 
        air default settings dictionary(medium_property)
        k_roughness = 0.2,
        density = 1.205,
        viscosity = 15*10**-6
        diameter -mm
        flow - m3/h
        """
        self.ke = medium_property["k_roughness"],
        self.density = medium_property["density"]
        # kinematic viscosity m2/s
        self.viscosity = medium_property["viscosity"]
        self.diameter = diameter/1000  # m
        self.flow = flow

    def get_area(self,):
        area = 3.14*self.diameter**2/4
        return area

    def get_velocity(self):
        area = self.get_area()
        velocity = self.flow/(3600*area)
        return velocity

    def get_renolds_number(self):
        velocity = self.get_velocity()
        self.Re = velocity*self.diameter/self.viscosity
        return self.Re

    def __get_lamda_altshul(self,):
        """
        lamda - friction value universal formula
        """
        self.get_renolds_number()
        lamda = 0.11*(self.ke/self.diameter+68/self.Re)**0.25 if self.diameter else 0
        return lamda

    def get_lamda_turbulence(self):
        """
        air formula 
        """
        self.get_renolds_number()
        if self.Re < 4000:
            lamda = self.__get_lamda_altshul()
            return lamda
        elif self.Re < 60000:
            lamda = 0.3164/self.Re**(0.25)
            return lamda
        else:
            lamda = 0.1266/self.Re**(0.1667)
            return lamda

    def get_presure_line_drop(self):
        lamda = self.get_lamda_turbulence()
        dynamic_presure = self.get_presure_dynamic_drop()
        pressure_drop = (lamda/self.diameter)*dynamic_presure if self.diameter else 0
        return pressure_drop

    def get_presure_dynamic_drop(self,):
        velocity = self.get_velocity()
        dynamic_presure = self.density*(velocity**2)/2
        return dynamic_presure

    def get_full_dynamic_drop_pressure(self, k_local_pressure=0):
        full_dynamic_pressure = self.get_presure_dynamic_drop()*k_local_pressure
        return full_dynamic_pressure

    def __repr__(self) -> str:
        return self.__class__.__name__


class SettingBuilder:
    """choose data from excel setting file
    """
    def __init__(self, excel_loader: ExcelLoader, power: float, network_branch_type: str) -> None:
        """load data from excel to DF

        Args:
            excel_loader (ExcelLoader): constant
            power (float): value from data frame
            network_branch_type (str): "branch", "root"
        """
        self.excel_loader = excel_loader
        self.power = power
        self.network_branch_type = network_branch_type
        self.medium_dict = self.excel_loader.get_medium_dict()
        self.drop_presuer = DropPressure(
            self.medium_dict, self.choose_standart_diameter(), self.get_flow())

    def get_flow(self):
        flow = FlowCalculation(self.medium_dict).calculate_flow(self.power)
        return flow

    def get_default_diameter(self):
        flow = self.get_flow()
        default_velocity = self.excel_loader.get_default_velocity(
            self.network_branch_type)
        self.diameter = DiameterSelecter(flow, default_velocity)
        diameter = self.diameter.calculate_default_diameter()
        return diameter

    def get_diameter_list(self):
        diameter_list = self.excel_loader.get_diameter_list()
        return diameter_list

    def choose_standart_diameter(self):
        self.get_default_diameter()
        standart_diameter = self.diameter.choose_standart_diameter(
            self.get_diameter_list())
        return standart_diameter

    def get_k_local_pressure(self):
        k_local_pressure = self.medium_dict["k_local_pressure"]
        return k_local_pressure
