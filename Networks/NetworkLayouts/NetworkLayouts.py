import streamlit as st
import pandas as pd


class CreateSystemLayout:
    """create side layout for systems property"""

    def __init__(self, df: pd.DataFrame, input_settings_df: pd.DataFrame) -> None:
        """select data from df

        Args:
            df (pd.DataFrame): df to revit
        """
        self.df = df
        
        system_type = input_settings_df["medium_property"]["system_type"].unique()
        self.system_type_choice = st.selectbox("choose system type", system_type)
        self.system_choice = st.selectbox(
            "choose system column", df.columns, index=len(df.columns) - 2
        )
        self.sys_flow_choice = st.selectbox("choose flow column", df.columns)
        self.level_val = st.selectbox("choose level", df["S_level"].unique())
        self.df_level_filter = df[df["S_level"] == self.level_val]
        self.system_name_choice = st.selectbox(
            "choose system name", self.df_level_filter[self.system_choice].unique()
        )
        self.space_name = st.selectbox(
            "Select  name text", ["S_ID", "S_Name", "S_Number"], index=2
        )
        self.system_number = st.number_input(
            "choose number of system", min_value=1, max_value=2, value=1
        )


class CreateNetworkLayout:
    def __init__(
        self,
        df: pd.DataFrame,
        system_number: int,
    ) -> None:
        """create multy system input layout

        Args:
            system_number (int): _description_
            df (pd.DataFrame): _description_
        """
        self.system_number_value = system_number
        self.system_number = str(system_number)
        self.df = df

        st.header(f"Network # {self.system_number}")
        self._create_location_point()
        self._create_start_and_end_network_points()
        self._create_prefix_name()
        print("self_sys_number",self.system_number)
    def _create_prefix_name(self):
        st.subheader("choose system prefix")
        prefix_dict = dict(
            route_name=st.text_input("choose system prefix", key=self.system_number),
        )
        for key, val in prefix_dict.items():
            setattr(self, key + "_" + self.system_number, val)

    def _create_location_point(self):
        st.subheader("choose location point")
        location_point_dict = dict(
            local_point_x=st.number_input(
                "input location point x", value=20000, key=self.system_number+'1'
            ),
            local_point_y=st.number_input(
                "input location point y", value=0, key=self.system_number+'2'
            ),
        )
        for key, val in location_point_dict.items():
            setattr(self, key + "_" + self.system_number, val)

    def _create_start_and_end_network_points(self):
        st.subheader("choose start and end network")
        network_point_dict = dict(
            network_start_point_x=st.number_input(
                "network start point x", value=-25000, key=self.system_number+'3'
            ),
            network_end_point_x=st.number_input(
                "network end point x", value=20000, key=self.system_number+'4'
            ),
            network_start_point_y=st.number_input(
                "network start point y", value=0, key=self.system_number+'5'
            ),
            network_end_point_y=st.number_input(
                "network end point y", value=0, key=self.system_number+'6'
            ),
        )
        for key, val in network_point_dict.items():
            setattr(self, key + "_" + self.system_number, val)


class AddLayoutsToList:
    """make joined layout of CreateSystemLayout and CreateNetworkLayout

    Returns:
        _type_: _description_
    """

    def __init__(
        self,
        df: pd.DataFrame,
        input_settings_df: pd.DataFrame,
    ) -> None:

        """create selectbox
        df: df to revit
        """
        self.df = df
        self.input_settings_df = input_settings_df
        self.tabs = st.tabs(["System Options","Network config"])

    def create_system_layout(
        self,
    ):
        with self.tabs[0]:
            st.subheader("choose system options")
            with st.expander('choose system options'):
                self.system_layouts = CreateSystemLayout(self.df, self.input_settings_df)
        return self.system_layouts

    def create_network_layout(self):
        with self.tabs[1]:
            with st.expander("Network config"):
                self.columns_number = self.system_layouts.system_number
                self.columns = st.columns(self.columns_number)
                self.networks_layouts_list = []
                for i in range(len(self.columns)):
                    with self.columns[i]:
                        temp = CreateNetworkLayout(self.df, i + 1)
                        self.networks_layouts_list.append(temp)
        return self.networks_layouts_list

    def create_from_to_layout(self):
        options = [
            getattr(temp, "route_name" + "_" + str(en + 1))
            for en, temp in enumerate(self.networks_layouts_list)
        ]
        with st.expander("from to connection"):
            for i in range(len(self.columns) - 1):
                if self.system_layouts.system_number >= 2:
                    st.subheader(f"select from to connection # {i+1}")
                    network_from_to_dict = dict(
                        network_from=st.selectbox(f"select from{i}", options),
                        network_to=st.selectbox(f"select to{i}", options),
                    )
                    for key, val in network_from_to_dict.items():
                        setattr(self, key + "_" + str(i + 1), val)
