
from Networks.ControlNetwork.CreateMainNetworkLayout import *
from Networks.PloteNetwork.NetworkPressurePlotter import *
from library_hvac_app.DbFunction.pandas_custom_function import df_to_excel_in_memory


class NetworkPressureLayout:
    def __init__(
        self,
        df_to_revit:pd.DataFrame,
        json_path:json,
        input_settings_df:pd.DataFrame
        ) -> st:
        """From layout data create tables of pressure loss and long route.
            Create plote of network and pressure network.

        Args:
            df_to_revit (pd.DataFrame): for choosing data.
            json_path (json): for polygons
            input_settings_df (pd.DataFrame): for calculation

        Returns:
            st: _description_
        """
        self.df_to_revit = df_to_revit
        self.json_path = json_path
        self.input_settings_df = input_settings_df
        self.network_layout = self.create_network_layout()
        self.filtred_coulmns = [
            "S_Name",
            "from",
            "to",
            "distance",
            "power",
            "flow",
            "diameter",
            "velocity",
            "line_pressure",
            "dinamic_pressure",
            "full_pressure",
        ]
        self.create_pressure_df()
        self.create_pressure_long_route_df()

    def create_network_layout(self):
        network_layout = CreateMainNetworkLayout(
            df_to_revit=self.df_to_revit,
            json_path=self.json_path,
            input_settings_df=self.input_settings_df,
        )
        network_layout()
        return network_layout

    def get_concate_pressure_df(self, df_list):
        if len(df_list) > 1:
            return pd.concat(df_list)
        else:
            return df_list[0]

    @staticmethod
    def drop_center_rows_dupblicates(df, prefix_from):
        prefix_from = to_list(prefix_from)
        for prefix_from in prefix_from:
            if prefix_from:
                df = df.drop(df[df["to"] == prefix_from + "cent"].index)
        return df

    # table
    def create_pressure_df(self):
        self.df_pressure_concate = self.get_concate_pressure_df(
            [val.concat_df() for val in self.network_layout.pressuer_df_list]
        )
        self.df_pressure_concate_filter = self.df_pressure_concate.filter(
            self.filtred_coulmns
        )
        return self.df_pressure_concate_filter

    def create_pressure_long_route_df(self):
        long_route = GetLongRoute(self.df_pressure_concate)
        self.longe_route_df = long_route.get_long_df()
        self.longe_route_df_filter = self.longe_route_df.filter(self.filtred_coulmns)
        return self.longe_route_df_filter

    # plots
    def create_network_plotter(self):
        network_plotter = NetworkPlotter(
            polygon_merge=self.network_layout.networks_update[0].polygon_merge,
            network_list=self.network_layout.networks_update,
            df_network=[
                network.df_branch for network in self.network_layout.networks_update
            ],
            space_name=self.network_layout.system_layouts.space_name,
            is_filled=True,
        )
        return network_plotter

    def create_pressure_plotter(self):
        pressure_plotter = NetworkPressurePlotter(
            polygon_merge=self.network_layout.networks_update[0].polygon_merge,
            network_list=self.network_layout.networks_update,
            df_network=[
                val.drop_center_rows_dupblicates()
                for val in self.network_layout.add_layout_data_to_pressure_calculation()
            ],
            title_prefix="Pressure Drop",
            show_grid=False,
        )
        return pressure_plotter

    def create_pressure_long_route_plotter(self):
        longe_route_df = self.drop_center_rows_dupblicates(
            self.longe_route_df, self.network_layout.list_of_from
        )
        pressure_plotter_long_route = NetworkPressurePlotter(
            polygon_merge=self.network_layout.networks_update[0].polygon_merge,
            network_list=self.network_layout.networks_update,
            df_network=[longe_route_df],
            title_prefix="Pressure Drop",
            show_grid=False,
        )
        return pressure_plotter_long_route

    def get_figures_for_layout(self):
        fig1 = self.create_network_plotter().calculate()
        fig2 = self.create_pressure_plotter().calculate()
        fig3 = self.create_pressure_long_route_plotter().calculate()
        return fig1, fig2, fig3

    def get_saved_figures(self,fig):
        saved_figure1 = self.create_network_plotter().save_plot(fig)
        return saved_figure1

    def create_df_and_plote_layout(self):
        fig1, fig2, fig3 = self.get_figures_for_layout()
        with st.expander("Network Table"):
            st.subheader("Pressure drop calculation")
            st.write(self.df_pressure_concate_filter)
            st.subheader("Main route Pressure drop calculation")
            st.write(self.longe_route_df_filter)
        with st.expander("Draft polte"):
            st.pyplot(fig1)
        with st.expander("Pressure polte"):
            st.pyplot(fig2)
            st.pyplot(fig3)
        with st.expander('downloads'):
            st.download_button(label='📥 StreamlitDownloadFunctions draft plote',
                                    data=self.get_saved_figures(fig1) ,
                                    file_name= 'draft_plote.svg')
            st.download_button(label='📥 StreamlitDownloadFunctions pressure plote',
                        data=self.get_saved_figures(fig2) ,
                        file_name= 'pressure_plote.svg')
            df1 = self.df_pressure_concate_filter
            df2 = self.longe_route_df_filter

            bufer_list = df_to_excel_in_memory([df1,df2],['sheet1','sheet2'])
            st.download_button(label='📥 StreamlitDownloadFunctions pressure tables',
                        data=bufer_list,
                        file_name="pandas_multiple.xlsx",)
