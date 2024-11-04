# region Import
import io
from io import BytesIO, StringIO

import ezdxf

from InputView.InputViewControl import InputViewControl, UploadLayout

from PrincipalSchems.Controls.DataForPlotting import DataForPlotting
from PrincipalSchems.Dxf.DxfExport import DxfExport
from PrincipalSchems.View.MainLayoutView import *
from PrincipalSchems.View.StaticView import StaticTabsView


# endregion

def download_dxf_from_drawing(drawing, filename="downloaded_dxf.dxf"):
    # Export file as string data so it can be transfered to the browser html A element href:
    # Create a string io object: An in-memory stream for text I/O
    stream_obj = io.StringIO()
    # write the doc (ie the dxf file) to the doc stream object
    drawing.write(stream_obj)
    # get the stream object values which returns a string
    dxf_text_string = stream_obj.getvalue()
    # close stream object as required by good practice
    stream_obj.close()
    st.download_button(
        label="Скачать DXF",
        data=dxf_text_string,
        file_name=filename,
        mime="application/dxf"
    )
    return dxf_text_string


class SchemeMain:
    def __init__(self, upload_layout: UploadLayout, key):
        self.upload_layout = upload_layout
        self.key = key

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
        plotter_data_list = []
        if tabs_view1.is_input_data_load() and tabs_view2.is_input_data_load():
            for tab in tab_view_list:
                with tabs[2]:
                    tab.create_dynamic_equipment_layout()
                with tabs[3]:
                    tab.create_dynamic_system_layout()
                data_for_plotting = DataForPlotting(self.input_df, tab)
                plotter_data_list.append(data_for_plotting)
        elif tabs_view1.is_input_data_load():
            with tabs[2]:
                self.expander_equipment(tabs_view1)
            with tabs[3]:
                tabs_view1.create_dynamic_system_layout()
                data_for_plotting1 = DataForPlotting(self.input_df, tabs_view1)
                plotter_data_list.append(data_for_plotting1)
        else:
            tabs_view1.waring_if_main_data_not_load()
        create_plot = st.button("Создать график")
        show_sketch = st.checkbox("показать эскиз")
        # Создать DXF
        if create_plot and len(plotter_data_list) > 0:
            dxf_export = DxfExport(plotter_data_list)
            _fig = dxf_export.export_to_dxf_data()
            dxf_export.save()
            download_dxf_from_drawing(DxfExport.doc)
            if show_sketch:
                st.pyplot(_fig)
