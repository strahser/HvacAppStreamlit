import streamlit as st
import pandas as pd

from SQL.SqlModel.SqlConnector import SqlConnector
from InsertTerminalsPandas.Controls.DetailAggModel import get_level_filter_grid_df
from InsertTerminalsPandas.Controls.LevelPlotControl import CreateSelectedPlotsControl, CreateLevelPlots
from InsertTerminalsPandas.Static.CalculationOptions import CalculationOptions
from InsertTerminalsPandas.TermilalView.ConfigView import InputDataDF, ConfigView, LayoutOptions, ColumnChoosing
from InsertTerminalsPandas.TermilalView.DeviceCRUDView import DeviceCRUDView
from InsertTerminalsPandas.TermilalView.DownloadResulView import DownloadResulLayout
from InsertTerminalsPandas.Core.TerminalsDownloadResult import TerminalsDownloadResult
from Session.StatementConfig import StatementConstants


class CreateAllViewsControl:
    def __init__(self, input_data_df: InputDataDF, key):
        """Create tabs"""
        self.key = key
        self.tabs_detail_view, self.tabs_config, self.tabs_main_plots, self.tabs_table_results, self.tabs_downloads = \
            st.tabs(["Detail View", "Config", "Plots", "Table Result", "Downloads"])
        self.input_data_df = input_data_df
        self.config_view = ConfigView(self.input_data_df, key=self.key)
        self.selected_id = []
        self.concat_all_level = None
        self.concat_level = None
        self.level_plot = None

    def choose_level_options(self):
        with self.tabs_config:
            self.config_view.create_config_tab()
        if self.config_view.choose_plot_radio_option == LayoutOptions.one_level:
            self.create_one_level_plot(self.input_data_df.revit_export)
            self.create_download_tab(LayoutOptions.one_level)
        elif self.config_view.choose_plot_radio_option == LayoutOptions.detail_view:
            with self.tabs_detail_view:
                self.create_detail_view()
        elif self.config_view.choose_plot_radio_option == LayoutOptions.all_levels:
            self.create_all_levels_plots()
            self.create_download_tab(LayoutOptions.all_levels)

    def create_detail_view(self):
        """create view,plot,tabel df for selected spaces"""
        device_crud = DeviceCRUDView(self.config_view.input_data_df)
        with st.sidebar:
            st.subheader('Show Type Data')
            show_revit_main_data_checkbox = st.checkbox('Show Spaces Data', value=True,
                                                        key=f'{self.key} Show Spaces Data')
            show_device_checkbox = st.checkbox('Show system data', key=f'{self.key}Show system data', )
            show_device_type_data_checkbox = st.checkbox('Show device type Data', key=f'{self.key}Show device data')
        if show_revit_main_data_checkbox:
            st.subheader('Select level Spaces')
            with st.expander(''):
                self.selected_id = get_level_filter_grid_df(self.input_data_df.revit_export,
                                                            self.config_view.level_value)
        if show_device_checkbox:
            selected_device_id = device_crud.create_devices_db_view()
            st.write(selected_device_id)
            # input_df = self.input_data_df.revit_export.copy()
            # condition = input_df[ColumnChoosing.S_ID].astype(str).isin([str(val) for val in selected_device_id])
            # filter_df = input_df[condition]
            level_plot = CreateLevelPlots(self.config_view, self.input_data_df.revit_export, self.input_data_df)
            level_plot.plot_all_polygons(selected_device_id)
            level_plot.plot_terminals_from_joining_excel_input_data(self.config_view.level_value)
            level_plot.create_plot_results_layout()
        if show_device_type_data_checkbox:
            st.write(self.input_data_df.device_type)
        if self.selected_id:
            self._create_selected_id_plot(self.selected_id)

    def _create_device_type_data(self):
        st.subheader("Device Type Data")
        chandged_df = st.data_editor(self.input_data_df.device_type,
                                     column_config={
                                         "device_orientation_option1": st.column_config.SelectboxColumn(
                                             options=self.input_data_df.device_orientation[
                                                 "orientation"].dropna().unique(),
                                             required=True),
                                         "device_orientation_option2": st.column_config.SelectboxColumn(
                                             options=self.input_data_df.device_orientation[
                                                 "orientation"].dropna().unique(),
                                             required=True),
                                         "single_device_orientation": st.column_config.SelectboxColumn(
                                             options=self.input_data_df.device_orientation[
                                                 "single_orientation"].dropna().unique(),
                                             required=True),
                                         "calculation_options": st.column_config.SelectboxColumn(
                                             options=CalculationOptions.get_list_of_enum_values())
                                     }
                                     )

    def _add_to_sql_device_type_button(self: pd.DataFrame):
        add_to_db_button = st.button("replace in DB", key="replace in DB button")
        if add_to_db_button:
            chandged_df_dict = self.to_dict()
            chandged_df1 = pd.DataFrame(chandged_df_dict)
            devices_name = st.session_state[StatementConstants.terminal_names_dict]["device_type"]
            chandged_df1.to_sql(devices_name, con=SqlConnector.conn_sql, if_exists="replace", index=False)

    def _create_selected_id_plot(self, selected_id: list):
        """create plot from selected Create tab result and tab download """
        input_df = self.input_data_df.revit_export.copy()
        condition = input_df[ColumnChoosing.S_ID].isin(selected_id)
        filter_df = input_df[condition]
        selected_plot = CreateSelectedPlotsControl(self.config_view, filter_df, self.input_data_df)
        selected_plot.plot_selected_terminals_and_polygons(selected_id)
        self.create_one_level_plot(input_df)
        with self.tabs_table_results:
            st.dataframe(selected_plot.create_selected_terminals_df())
        self.create_download_tab(LayoutOptions.one_level)

    def create_one_level_plot(self, input_df) -> pd.DataFrame:
        self.level_plot = CreateLevelPlots(self.config_view, input_df, self.input_data_df)
        self.level_plot.plot_all_polygons()
        self.level_plot.plot_terminals_from_joining_excel_input_data(self.config_view.level_value)
        with self.tabs_main_plots:
            self.level_plot.create_plot_results_layout()
        with self.tabs_table_results:
            self.level_plot.create_data_frame_results_layout()
        self.concat_level = self.level_plot.concat_all
        return self.concat_level

    def create_all_levels_plots(self) -> pd.DataFrame:
        concat_all_levels = []
        for level_ in self.config_view.df_levels:
            level_plot = CreateLevelPlots(self.config_view, self.input_data_df.revit_export, self.input_data_df)
            level_plot.plot_all_polygons()
            level_plot.plot_terminals_from_joining_excel_input_data(level_)
            with self.tabs_main_plots:
                level_plot.create_plot_results_layout()
            with self.tabs_table_results:
                level_plot.create_data_frame_results_layout()
            concat_all_levels.append(level_plot.concat_all)
        if concat_all_levels:
            self.concat_all_level = pd.concat(concat_all_levels, axis=0)
            return self.concat_all_level

    def create_download_tab(self, number_of_levels: str):
        if number_of_levels == LayoutOptions.one_level:
            with self.tabs_downloads:
                download_files = TerminalsDownloadResult(self.concat_level, self.input_data_df).create_download_data()
                DownloadResulLayout(download_files.excel_file, download_files.json_file).create_download_layout()

        if number_of_levels == LayoutOptions.all_levels:
            with self.tabs_downloads:
                download_files = TerminalsDownloadResult(self.concat_all_level,
                                                         self.input_data_df).create_download_data()
                DownloadResulLayout(download_files.excel_file, download_files.json_file).create_download_layout()
