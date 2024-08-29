import pandas as pd
from plotly import graph_objs as go

from PrincipalSchems.Controls.PolygonPointsMergeControl import PolygonPointsMergeControl
from PrincipalSchems.View.MainLayoutView import DynamicWidgetsViewContextData


class PlotlyPlotter:
    def __init__(
            self, fig: go.Figure, polygon_points_merge_control: PolygonPointsMergeControl
    ):
        self.fig = fig
        self._df = polygon_points_merge_control.df_text._df
        self.polygon_points_merge_control = polygon_points_merge_control
        self.level_property = polygon_points_merge_control.get_level_property()

    def add_level_text(self):
        for prop in self.level_property:
            if prop.vertical_direction_list == "up":
                self.fig.add_trace(
                    # add flow
                    go.Scatter(
                        x=[prop.level_coord_x, prop.level_coord_x],
                        y=[prop.level_coord_y, prop.level_coord_y],
                        legendgroup="level name",
                        name="level name",
                        textfont=dict(size=14, family="Issocuper", color="black"),
                        text=f"<em> {str(prop.level_name)} </em>",
                        showlegend=False,
                        mode="text",
                    )
                )

    def add_text_to_plot(self):
        # text to center polygon
        self.fig.add_trace(
            go.Scatter(
                x=self._df["pcx"],
                y=self._df["pcy"],
                mode="text",
                textfont=dict(size=14, family="Issocuper", color="black"),
                text="<em>" + self._df["text"] + "</em>",
                texttemplate="%{text}",
                legendgroup="Space Text",
                name="Space Text",
                showlegend=False,
            )
        )

    def plot_vertical_side_plot_lines_to_system(self):
        # between levels
        for idx_, row in self.polygon_points_merge_control.add_color_df.iterrows():
            self.fig.add_trace(
                go.Line(
                    x=(row["Max_x"], row["Min_x"]),
                    y=(row["Max_y"], row["Min_y"]),
                    line_color=row.color,
                    legendgroup=row.system_name,
                    name=row.system_name,
                )
            )

    def _plot_polygons_plot(self, show_color: bool = False, line_color_filter: str = False):

        for idx, row in self._df.iterrows():
            if show_color and line_color_filter:
                self.fig.add_trace(
                    go.Scatter(
                        x=row["px"],
                        y=row["py"],
                        fill="toself",
                        line_color=row["color"],
                        legendgroup=row[line_color_filter],
                        name=row[line_color_filter],
                        mode="lines",
                        showlegend=True,
                    )
                )
            else:
                self.fig.add_trace(
                    go.Scatter(
                        x=row["px"],
                        y=row["py"],
                        mode="lines",
                        line_color="grey",
                        showlegend=False,
                    )
                )

    def plot_start_end_system_lines(self, textposition: str = "bottom left"):
        # from polygons up or down
        all_system_points = self.polygon_points_merge_control.system_property_points
        df_1 = pd.DataFrame([prop.__dict__ for prop in all_system_points])
        df_1 = df_1.groupby(['offset_point_x', 'offset_point_y'])["system_flow"].sum().reset_index()

        for point in all_system_points:
            self.fig.add_trace(
                # add flow
                go.Scatter(
                    x=[point.x_start_points, point.x_start_points],
                    y=[point.y_start_points, point.y_start_points],
                    line_color=point.color,
                    marker=dict(
                        size=14,
                        color=point.color,
                        symbol="arrow-bar-down",
                        # line=dict(width=0.5),
                    ),
                    legendgroup=point.system_name,
                    name=point.system_name,
                    textfont=dict(size=14, family="Issocuper", color=point.color),
                    text=f"<i> L={str(point.system_flow)} </i>",
                    textposition=textposition,
                    legendgrouptitle_text="Systems" + " " + point.system_name,
                    showlegend=False,
                    mode="text+markers",
                )
            )
            # add offset sum flow
            for idx, row in df_1.iterrows():
                if row['offset_point_x'] == point.offset_point_x and row['offset_point_y'] == point.offset_point_y:
                    self.fig.add_trace(
                        # add sum flow
                        go.Scatter(
                            x=[point.offset_point_x, point.offset_point_x],
                            y=[point.offset_point_y, point.offset_point_y],
                            line_color=point.color,
                            marker=dict(
                                size=14,
                                color=point.color,
                                symbol="arrow-bar-down",
                                # line=dict(width=0.5),
                            ),
                            legendgroup=point.system_name,
                            name=point.system_name,
                            textfont=dict(size=14, family="Issocuper", color=point.color),
                            text=f"<i>{point.level_value} L{point.system_name} = {round(row['system_flow'])} </i>",
                            textposition=textposition,
                            legendgrouptitle_text="Systems" + " " + point.system_name,
                            showlegend=False,
                            mode="text",
                        )
                    )

            self.fig.add_trace(
                # from polygons up or down
                go.Line(
                    x=(point.x_start_points, point.x_end_points),
                    y=(point.y_start_points, point.y_end_points),
                    line_color=point.color,
                    legendgroup=point.system_name,
                    name=point.system_name,
                    legendgrouptitle_text="Systems" + " " + point.system_name,
                    showlegend=False,
                    mode="lines+ text",
                )
            )
            # offset points
            self.fig.add_trace(
                go.Line(
                    x=(point.x_end_points, point.offset_point_x),
                    y=(point.y_end_points, point.offset_point_y),
                    line_color=point.color,
                    marker=dict(
                        size=15,
                        color=point.color,
                        symbol="triangle-right",
                        line=dict(width=0.6),
                    ),
                    legendgroup=point.system_name,
                    textfont=dict(size=14, family="Issocuper", color=point.color),
                    name=point.system_name,
                    text="<i>" + point.system_name + "</i>",
                    textposition="bottom center",
                    mode="lines+ markers+ text",
                )
            )

    def __plot_horizontal_line_to_equipment(self, row):
        self.fig.add_trace(
            go.Line(
                x=[row["base_point_x"], row["px"]],
                y=[row["base_point_y"], row["py"]],
                line_color=row["color"],
                legendgroup=row.system_name,
                name=row.system_name,
            )
        )

    def __text_check_position(self, base_point_x: float, base_point_y: float, px: float, py: float) -> str:
        """check position for equipment text"""

        if base_point_x < px and base_point_y == py:
            return "middle left"
        elif base_point_x > px and base_point_y == py:
            return "middle right"
        elif base_point_x == px and base_point_y > py:
            return "top center"
        else:
            return "bottom center"

    def plot_add_text_to_equipment_point(self, dynamic_widgets_view_context_data: DynamicWidgetsViewContextData,
                                         location_point_list: list[pd.DataFrame],
                                         ):

        for en, df in enumerate(location_point_list):  # levels iteration
            for idx_, row in df.iterrows():  # df row iteration
                # horizontal line to equipment
                self.__plot_horizontal_line_to_equipment(row)
            # equipment text and marker
            self.fig.add_trace(
                go.Scatter(
                    x=df["base_point_x"],
                    y=df["base_point_y"],
                    legendgroup=dynamic_widgets_view_context_data.legend_group[en],
                    name=dynamic_widgets_view_context_data.legend_group[en],
                    text="<em>"
                         + df["system_name"].astype("string")
                         + " <br>"
                         + df[
                             self.polygon_points_merge_control.layout_view_context_data.level_column
                         ]
                         + " <br>"
                         + str(dynamic_widgets_view_context_data.flow_list_value[en])
                         + "</em>",
                    textposition=self.__text_check_position(
                        row["base_point_x"], row["base_point_y"], row["px"], row["py"]
                    ),
                    textfont=dict(size=14, family="Issocuper"),
                    mode="text+markers+lines",
                    marker=dict(
                        size=40,
                        color=df.color,
                        symbol=dynamic_widgets_view_context_data.equipment_symbol_list[
                            en
                        ],
                        line=dict(color="Black", width=2),
                    ),
                )
            )

    def __show_only_unique_legend(self):
        names = set()
        self.fig.for_each_trace(
            lambda trace: trace.update(showlegend=False)
            if (trace.name in names)
            else names.add(trace.name)
        )
        return self.fig

    def plot_update_fig(
            self,
            plot_height: float = 3000,
            plot_width: float = 3000,
            show_grid: bool = False,
            plote_titl: str = "Plot Title",
    ) -> None:
        self.fig.update_traces(hoverinfo="text+name")

        self.fig.update_xaxes(
            showgrid=show_grid, zeroline=show_grid, showticklabels=show_grid
        )
        self.fig.update_yaxes(
            showgrid=show_grid,
            zeroline=show_grid,
            showticklabels=show_grid,
            scaleanchor="x",
            scaleratio=1,
        )
        self.fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            autosize=False,
            width=plot_height,
            height=plot_width,
            plot_bgcolor="rgba(0,0,0,0)",
            title={
                "text": f"<em> {plote_titl} </em>",
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            title_font_size=18,
            title_font_family="Issocuper",
        )
        self.__show_only_unique_legend()