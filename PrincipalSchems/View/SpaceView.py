from Polygons.PolygonView.PlotView import *
from StaticData.AppConfig import MenuChapters


class SpaceDimensionView:
    def __init__(self, key):
        self.key = key

    def add_polygon_config_widget(self):
        columns = st.columns(4)
        with columns[0]:
            self.polygon_width = st.number_input("insert space width", value=50,key=f"{self.key} polygon_width")
            self.polygon_height = st.number_input("insert space height", value=50,key=f"{self.key} polygon_height")
        with columns[1]:
            self.level_distance = st.number_input("distance between levels", value=300,key=f"{self.key} level_distance")
            self.distance_between_systems = st.number_input("distance between systems", value=20,key=f"{self.key} distance_between_systems ")
        with columns[2]:
            self.equipment_distance_horizontal = st.number_input("Equipment Distance Horizontal", value=300,key=f"{self.key} equipment_distance_horizontal")
            self.equipment_distance_vertical = st.number_input("Equipment Distance Vertical", value=300,key=f"{self.key} equipment_distance_vertical")