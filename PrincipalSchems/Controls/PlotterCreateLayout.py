from PrincipalSchems.Controls.DataForPlotting import DataForPlotting
from PrincipalSchems.Ploters.PlotlyPlotter import PlotlyPlotter


class PlotterCreateLayout:
    def __init__(self, fig, data_for_plotting: DataForPlotting) -> None:
        self.fig = fig
        self.data_for_plotting = data_for_plotting
        self.polygon_plotter_merge_control = data_for_plotting.polygon_points_merge_control

    def create_plot_layout(self, text_position: str = "bottom left"):
        plot_plotter = PlotlyPlotter(self.fig, self.polygon_plotter_merge_control)
        plot_plotter.plot_vertical_side_plot_lines_to_system()
        plot_plotter.plot_start_end_system_lines(text_position)
        plot_plotter._plot_polygons_plot(
            self.polygon_plotter_merge_control.layout_view_context_data.color_view_checkbox,
            self.polygon_plotter_merge_control.layout_view_context_data.space_data_view.color_filter_name,
        )
        plot_plotter.add_text_to_plot()
        plot_plotter.plot_add_text_to_equipment_point(
            self.data_for_plotting.dynamic_widgets_view_context_data,
            self.data_for_plotting.location_point_list,
        )
        plot_plotter.plot_update_fig(
            self.polygon_plotter_merge_control.layout_view_context_data.plot_height,
            self.polygon_plotter_merge_control.layout_view_context_data.plot_width,
            show_grid=False,
            plote_titl=self.data_for_plotting.plot_title,
        )
        plot_plotter.add_level_text()
