from InsertTerminalsPandas.TermilalView.PlotResultView import PlotResultLayout
from InsertTerminalsPandas.Controls.SelectedDFCalculateControl import *
from InsertTerminalsPandas.Controls.SelectedTerminalsControl import *
from InsertTerminalsPandas.PlotePolygons.PolygonMerge import SetColor
from InsertTerminalsPandas.Static.DevicePropertiesName import DevicePropertiesName
from InsertTerminalsPandas.Static.ColumnChoosing import ColumnChoosing
from InsertTerminalsPandas.Core.AddDataToDF import AddPolygonsToDF
from StaticData.Exception import ExceptionWriter


class CreatePlotsControlBase:
    def __init__(self,
                 config_view: ConfigView,
                 df_input_table: pd.DataFrame,
                 input_data_df: InputDataDF,
                 level_value: str = None):
        self.devices_list = None
        self.input_data_df = input_data_df
        self.config_view = config_view
        self.level_value = level_value if level_value else self.config_view.level_value
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()
        self.df_polygons = AddPolygonsToDF(df_input_table, self.level_value, input_data_df).add_all_polygons_to_df()
        self.df_polygons = self.df_polygons.fillna(0)

    def _create_system_color(self) -> dict:
        color_dict = {}
        for system_ in self.config_view.system_select:
            system_name_column = self.input_data_df.system_dictionary[system_].system_name
            color = SetColor(self.input_data_df.revit_export, system_name_column, ColumnChoosing.S_ID)
            df = color.set_color_by_category().dropna()
            filtered_df = df[["color", system_name_column]]
            unique_system = filtered_df[system_name_column].unique()
            unique_color = filtered_df["color"].unique()
            system_color = dict(zip(unique_system, unique_color))
            color_dict.update(system_color)
        return color_dict


class CreateSelectedPlotsControl(CreatePlotsControlBase):
    def __init__(self, config_view: ConfigView, df_input_table: pd.DataFrame, input_data_df: InputDataDF):
        super().__init__(config_view, df_input_table, input_data_df)

    def _create_device_list(self, selected_id: list[str]):
        self.selected_id = selected_id
        parsing_terminals = ParsingDBtoTerminalDataControl(self.df_polygons, self.config_view, self.input_data_df)
        system_color_dictionary = self._create_system_color()
        devices_list = parsing_terminals.add_parsing_data_to_device_model(system_color_dictionary, selected_id)
        self.device_layout_list = parsing_terminals.device_layout_list
        return devices_list

    def plot_selected_terminals_and_polygons(self, selected_id: list[str], polygon_expander_name: str = "Plot "):
        self.devices_list = self._create_device_list(selected_id)
        PlotSelectedSpacesAndTerminals.plot_selected_polygons(self.df_polygons, self.ax, selected_id)
        for device in self.devices_list:
            PlotSelectedSpacesAndTerminals.plot_selected_terminals(self.ax, device)
        plt.axis('off')
        st.subheader(polygon_expander_name)
        with st.expander(""):
            col1, col2, col3 = st.columns(3)
            height = col1.number_input("Plot height", min_value=2, max_value=30, step=2, value=5,
                                       key="terminal plot height")
            width = col2.number_input("Plot width", min_value=2, max_value=30, step=2, value=5,
                                      key="terminal plot width")
            self.fig.set_size_inches(width, height)
            fig = PlotTerminalsAndSpaces.save_plot(self.fig)
            st.write(fig, unsafe_allow_html=True)

    def create_selected_terminals_df(self):
        df = pd.DataFrame(self.devices_list)[DevicePropertiesName.selected_df_columns_name]
        df_out = df.style.applymap(style_less_then, subset='k_ef')
        return df_out


class CreateLevelPlots(CreatePlotsControlBase):
    def __init__(self, config_view: ConfigView, df_input_table: pd.DataFrame, input_data_df: InputDataDF):
        super().__init__(config_view, df_input_table, input_data_df)
        self.level_value_label = None

    def plot_all_polygons(self, selected_spaces_id=None):
        PlotTerminalsAndSpaces.plot_spaces(ax=self.ax, all_level_spaces=self.df_polygons,
                                           selected_spaces_id=selected_spaces_id)

    def plot_terminals_from_joining_excel_input_data(self, level_value: str = None):
        self.df_result_list = []
        self.df_concat = []
        for system_ in self.config_view.system_select:
            try:
                main_df = MainDFCalculate(self.config_view,
                                          system_,
                                          level_value,
                                          self.input_data_df
                                          )
                df_result = main_df.get_df_result()
                df_concat = main_df.get_df_for_concat()
                self.df_result_list.append(df_result)
                self.df_concat.append(df_concat)
                self.fig.set_size_inches(self.config_view.plot_width, self.config_view.plot_height)
                PlotTerminalsAndSpaces.plot_terminals(
                    self.ax,
                    main_df.df_calculated.level_df_data,
                    system_,
                    self.input_data_df
                )
                level_value_label = main_df.df_calculated.level_df_data[ColumnChoosing.S_level].unique()
                self.level_value_label = level_value_label[0] if len(level_value_label) > 0 else level_value_label
                self.save_fig = PlotTerminalsAndSpaces.save_plot(self.fig)
            except:
                ExceptionWriter.exception_name_and_flow(system_)
                self.save_fig = None

        if self.save_fig:
            self.concat_all = pd.concat(self.df_concat, axis=0)
        else:
            self.concat_all = None
        return self.concat_all

    def create_plot_results_layout(self):
        self.plot_result_layout = PlotResultLayout(self.save_fig, self.df_result_list,
                                                   self.config_view.system_select,
                                                   self.level_value_label)
        self.plot_result_layout.create_plot_results_layout()

    def create_data_frame_results_layout(self):
        self.plot_result_layout.create_data_frame_results_layout()
