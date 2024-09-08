
import os
import inspect
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
sys.path.insert(0, root_dir) 
from InsertTerminalsPandas.Geometry.GeometryTerminals import*
from TestFunck import *

in_dict = {
    "py": [
        -2593.1707615915016,
        -2593.1707615914793,
        -10893.170761591482,
        -10893.170761591495
    ],
    "pcy": -6743.1707615914893,
    "pcx": 2834.4630248830731,
    "pz": [
        8438.3999999999996,
        8438.3999999999996,
        8438.3999999999996,
        8438.3999999999996
    ],
    "px": [
        6942.3427891327119,
        75.0,
        75.0,
        4245.5093103995805
    ]
}

lines = offset_polygon(in_dict,1000)
key_curve = CheckPointLocation(lines.offset_lines,'Y','min')
curve_dict = CreateCurveDictionary(lines.offset_lines)
curve_dict._get_curves_location()
curve_dictionary = curve_dict.get_filter_curve_dict()

curve_filter = CreateCurvesFilters(curve_dictionary,'up','down','center',1,True)
points = curve_filter.split_curve_by_point_definition()
print(points)
plot_test = PlotTestLines(
    lines.polygon,
    lines=[
        *curve_dict._get_central_line_curves(),
        *curve_dict._get_up_down_curves(),
        *curve_dict._get_left_right_curves()
        ],
    points_coordinates=points
    )
plot_test.plot_lines()
plot_test._plot_scatters()
plt.show()


