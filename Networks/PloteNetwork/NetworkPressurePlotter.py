from Networks.PloteNetwork.NetworkPlotter import *
from Polygons.PolygonPlot.MPLSetting import *
import locale


class NetworkPressurePlotter(NetworkPlotter):
    """plot df lines and add text"""

    def __init__(self, polygon_merge: PolygonMerge,  network_list: list,df_network, space_name: str = 'from', show_grid=True, is_filled=False,title_prefix:str =''):
        super().__init__(polygon_merge,  network_list,df_network, space_name, show_grid, is_filled,title_prefix)

    def plot_lines(self, df):
        x = (df["from_x"], df["to_x"])
        y = (df["from_y"], df["to_y"])
        self.ax.plot(
            x,
            y,
            color="b",
            linestyle="-",
            linewidth=3,
        )
        return self.fig

    def add_from_text(self, df):
        for i, row in df.iterrows():
            if row["distance"] == 0:
                self.corner_line_position_text(
                    row, "from_x", "from_y", self.space_name, -400, -400
                )
            else:
                self.corner_line_position_text(row, "from_x", "from_y", self.space_name)

    def add_to_text(self, df):
        for i, row in df.iterrows():
            if row["distance"] == 0:
                self.corner_line_position_text(row, "to_x", "to_y", "to", -400, -400)
            else:
                self.corner_line_position_text(row, "to_x", "to_y", "to")

    def add_diameter_text(self, df):
        """make iteration on df rows.
        shifts the text block
        """
        for i, row in df.iterrows():
            if row["from_x"] == row["to_x"]:
                self.center_line_position_text(row, 600, 0)
            elif row["distance"] == 0:
                self.center_line_position_text(row, 400, 400)
            else:
                self.center_line_position_text(row)

    def center_line_position_text(self, row, const_x=0, const_y=0):
        """get diameter and flow

        Args:
            row (pd.df): _description_
            const_x (int, optional): _description_. Defaults to 0.
            const_y (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: matplotlib text
        """
        center_line_position_text = self.ax.text(
            row["center_x"] + const_x,
            row["center_y"] + const_y,
            AddTextToPlote.add_flow_value(row),
            **text_style,
        )
        return center_line_position_text

    def corner_line_position_text(
        self, row, x_coord: str, y_coord: str, txt_column: str, const_x=0, const_y=0
    ):
        corner_line_position_text = self.ax.text(
            row[x_coord] + const_x,
            row[y_coord] + const_y,
            row[txt_column],
            bbox=box_1,
            **text_style,
        )
        return corner_line_position_text

    def add_grid(self):
        self.ax.grid(True, which="both")
        self.ax.minorticks_on()

    def add_text_to_branchse(self, df_network):
        self.add_text_from_df(
            df_network,
            "pcx",
            "pcy",
            [
                "L",
                "",
            ],
            [self.sys_flow_column, self.space_name],
            bbox=box_2,
            **text_style,
        )

    def calculate(self):
        for df_ in self.df_network:
            self.plot_lines(df_)
            self.add_from_text(df_)
            self.add_to_text(df_)
            self.add_diameter_text(df_)
        self.add_title()
        self.make_level_filter()
        self.add_coordinate_axis()
        self.create_polygon_data()
        
        self.plot_polygons("", [], is_filled=self.is_filled)

        return self.fig


class AddTextToPlote:
    @classmethod
    def add_flow_value(self, row):

        if row["flow"] < 100:
            return f"d={row['diameter']}\nL={round(row['flow'],2)}"
        elif row["flow"] > 10 and row["flow"] < 100:
            return f"d={row['diameter']}\nL = {round(row['flow'],1)}"
        else:
            flow = locale.format("%d", int(row["flow"]), grouping=True)
            return f"d={row['diameter']}\nL = {flow}"
