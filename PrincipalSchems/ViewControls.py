# region Import
import io
import zipfile

from InputView.InputViewControl import InputViewControl, UploadLayout

from plotly import graph_objs as go
import plotly

from PrincipalSchems.Controls.DataForPlotting import DataForPlotting
from PrincipalSchems.Controls.PlotterCreateLayout import PlotterCreateLayout
from PrincipalSchems.Dxf.DxfExport import DxfExport
from PrincipalSchems.View.MainLayoutView import *
from PrincipalSchems.View.StaticView import StaticTabsView
from datetime import datetime


# endregion

class SchemeMain:
    def __init__(self, upload_layout: UploadLayout, key):
        self.fig = go.Figure()
        self.upload_layout = upload_layout
        self.key = key

    def download_plt_html(self):
        today = datetime.now()
        with io.BytesIO() as buffer:
            # Write the zip file to the buffer
            width = st.session_state["Scheme plot_width"]
            height = st.session_state["Scheme plot_height"]
            with zipfile.ZipFile(buffer, "w") as zip:
                res1 = plotly.io.to_image(self.fig, "pdf", width=width, height=height, scale=1.5)
                res2 = plotly.io.to_image(self.fig, "jpg", width=width, height=height, scale=1.5)
                res3 = plotly.io.to_html(self.fig, include_plotlyjs="cdn", default_width=width, default_height=height)
                zip.writestr(f"Scheme_{today}.pdf", res1)
                zip.writestr(f"Scheme_{today}.jpg", res2)
                zip.writestr(f"Scheme_{today}.html", res3)
                buffer.seek(0)
            btn = st.download_button(
                label="Download ZIP",
                data=buffer,  # StreamlitDownloadFunctions buffer
                file_name=f"Scheme_{today}.zip"
            )

    @staticmethod
    def get_flow_text_direction(tabs_view: TabsView):
        if tabs_view.layout_view_context_data.vertical_direction_list == "up":
            return "top left"
        else:
            return "bottom left"

    @staticmethod
    def expander_equipment(tabs: TabsView):
        tabs.create_dynamic_equipment_layout()

    def tab_0(self, tabs: st.tabs):
        with tabs[0]:
            with st.expander("Hide/Show Input Data", True):
                input_view_control = InputViewControl(self.upload_layout, key=self.key)
                self.input_df = input_view_control.create_input_view()
                static_layout_view = StaticLayoutView(self.input_df, key=self.key)
                self.input_df.rename(columns={static_layout_view.ID_COLUMN: "S_ID"}, inplace=True)
                tabs_view1 = TabsView(static_layout_view, key=self.key)
                tabs_view2 = TabsView(static_layout_view, key=self.key, color_reverse=True)
                tabs_view1.create_choose_column_level()
                tabs_view1.create_choose_system_property(1, "first", uniq_key=f"{self.key} 1")
                tabs_view2.create_choose_system_property(2, "second", uniq_key=f"{self.key} 2")
        return tabs_view1, tabs_view2

    def tab_1(self, tabs: st.tabs, tabs_view1: TabsView, tabs_view2: TabsView):
        with tabs[1]:
            tabs_view1.create_space_dimensions()
        with tabs[4]:
            tabs_view1.add_plot_config()
        tab_view_list = [tabs_view1, tabs_view2]
        return tab_view_list

    def main(self):
        tabs = st.tabs(StaticTabsView.tabs)
        tabs_view1, tabs_view2 = self.tab_0(tabs)
        tab_view_list = self.tab_1(tabs, tabs_view1, tabs_view2)

        if tabs_view1.is_input_data_load() and tabs_view2.is_input_data_load():
            for tab in tab_view_list:
                with tabs[2]:
                    tab.create_dynamic_equipment_layout()
                with tabs[3]:
                    tab.create_dynamic_system_layout()
                data_for_plotting = DataForPlotting(self.input_df, tab)
                text_position = self.get_flow_text_direction(tab)
                plotter_create_layout1 = PlotterCreateLayout(self.fig, data_for_plotting)
                plotter_create_layout1.create_plot_layout(text_position)
                dxf_export = DxfExport(plotter_create_layout1)
                dxf_export.export_to_dxf_data()

        elif tabs_view1.is_input_data_load():
            with tabs[2]:
                self.expander_equipment(tabs_view1)
            with tabs[3]:
                tabs_view1.create_dynamic_system_layout()
                data_for_plotting1 = DataForPlotting(self.input_df, tabs_view1)
                plotter_create_layout1 = PlotterCreateLayout(self.fig, data_for_plotting1)
                text_position = self.get_flow_text_direction(tabs_view1)
                plotter_create_layout1.create_plot_layout(text_position)
        else:
            tabs_view1.waring_if_main_data_not_load()
        create_plot = st.button("Create Plot")
        if create_plot:
            self.download_plt_html()
            # plt_plotter_polygon = PltPolygonPlotter(fig_mpl, ax, data_for_plotting)
            # plt_plotter_polygon()
            # legend_without_duplicate_labels_fig(fig_mpl)
            # plt.legend()
            # st.pyplot(fig_mpl)
            # , use_container_width=True

            st.plotly_chart(self.fig)
