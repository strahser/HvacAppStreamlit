from Models.SchemeModel import *


class SpacesPerimeterLinesDF:

    def __init__(
        self,
        space_id: list,
        polygon_coordinates: PolygonCoordinates,
        df_column_system_name: list,
    ) -> pd.DataFrame:
        self.space_id = space_id
        self.polygon_coordinates = polygon_coordinates
        self.df_column_system_name = df_column_system_name

    def create_perimeter_polygon(self):
        return PolygonsCreator(self.space_id,
                               self.polygon_coordinates).create_polygons()

    def add_perimeter_polygon_to_df(self):
        spaces = self.create_perimeter_polygon()
        df_ = (pd.DataFrame(spaces,
                            index=["Polygons"
                                   ]).T.reset_index().rename({"index": "S_ID"},
                                                             axis=1))
        return df_

    def get_perimeter_lines(self):
        df_ = self.add_perimeter_polygon_to_df()
        df_["polygon_lines"] = df_.apply(
            lambda df: gl.GeometryUtility.get_lines_in_polygon(df[
                "Polygons"].exterior.coords),
            axis=1,
        )
        return df_

    def __calculate_system_points_from_dict(self, S_ID):

        return len(self.spaces_system_dictionary[S_ID].keys())

    def __change_coordinate_value_in_system_property(
            self, system_property: SystemProperty, changed_values: dict):
        if isinstance(system_property, tuple):
            system_property = system_property._replace(**changed_values)
        return system_property

    def add_number_of_system_to_df(self):
        df = self.get_perimeter_lines()
        df["system_number"] = df.apply(
            lambda df: self.__calculate_system_points_from_dict(df["S_ID"]),
            axis=1)
        return df

    def create_system_property_df(self):
        return (pd.DataFrame(
            self.spaces_system_dictionary).T.reset_index().rename(
                {"index": "S_ID"}, axis=1))

    def merge_lines_and_system_property(self):
        return pd.merge(
            self.add_number_of_system_to_df(),
            self.create_system_property_df(),
            on="S_ID",
            how="left",
        )

    def get_curve_split_points_coordinates(self, perimeter_lines,
                                           points_number, curve_orientation):
        curve_dict = CreateCurvesFromStartPoint(perimeter_lines)
        curve_dict._get_curves_location()
        curve_dictionary = curve_dict.get_filter_curve_dict()
        points = curve_dictionary[curve_orientation]._get_standard_points(
            points_number)
        return points

    def add_points_start_coordinates_to_df(self):
        df = self.merge_lines_and_system_property()
        df["coordinates"] = df.apply(
            lambda df: self.get_curve_split_points_coordinates(
                df["polygon_lines"], df["system_number"], "up"),
            axis=1,
        )
        return df

    def add_coordinate_value_in_system_property(self):
        df = self.add_points_start_coordinates_to_df()
        unique_sys_list = []
        for i, row in df.iterrows():
            id_column = self.spaces_system_dictionary[row["S_ID"]]
            key_ = id_column.keys()
            unique_sys_list.append(list(key_))
        df["unique_sys"] = unique_sys_list
        for id_, row in df.iterrows():
            for en, sys in enumerate(row["unique_sys"]):
                df[sys] = df.apply(
                    lambda df_: self.
                    __change_coordinate_value_in_system_property(
                        df_[sys],
                        {"x_start_points": df_["coordinates"][en][0]}),
                    axis=1,
                )

        return df
