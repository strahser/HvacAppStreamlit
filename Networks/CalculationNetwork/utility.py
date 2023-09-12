
from itertools import cycle, product
from shapely.geometry import LineString, Point
import io
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.patches import Polygon
from matplotlib.pyplot import axes, axis

from numpy.core.numeric import NaN
import pandas as pd
import json
import math
import random
import numpy as np
from library_hvac_app.text_custom_functions import StringBuilder
def df_unique(df, column_name):
    """
    get unique item of column for dropdown list
    """
    unique_list = pd.unique(df[column_name])
    return unique_list

def df_write_html(df_, df_path_html):
    """
    temp view df in html
    """
    pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>
    html_string = '''
        <html>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <meta http-equiv="Content-Type" content="text/html; charset=cp1251" />

        <head><title>HTML Pandas Dataframe with CSS</title></head>
        <link rel="stylesheet" type="text/css" href="df_style.css"/>
        <body>
            {table}
        </body>
        </html>.
        '''
    # OUTPUT AN HTML FILE
    with open(df_path_html, 'w') as f:
        f.write(html_string.format(table=df_.to_html(classes='table')))


def lineIntersection(x1, x2, y1, y2, x3, x4, y3, y4):
    const = ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    if const:
        px = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4)) / const
        py = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4)) / const
        return px, py
    else:
        return NaN


def segment_center(x1,x2):
    center = (x1+x2)/2
    return center


def segment_intersection(x1, x2, y1, y2, x3, x4, y3, y4):
    line = LineString([(x1, y1), (x2, y2)])
    other = LineString([(x3, y3), (x4, y4)])
    int_pt = line.intersection(other)
    if isinstance(int_pt, Point):
        point_of_intersection = int_pt.x, int_pt.y
        return point_of_intersection
    else:
        return None


def p_distance(x1, y1, x2, y2):
    if x1 != None or y1 != None or x2 != None or y2 != None:
        res = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    else:
        raise ValueError("wrong type of coordinate")
    return res


def split_df_val(df, splited_column, new_column1, new_column2):

    df.loc[df[splited_column] != None, new_column1] = df[splited_column].str[0]
    df.loc[df[splited_column] != None, new_column2] = df[splited_column].str[1]
    return df


def filter_df(df_, column_name, column_val):
    mask = df_[column_name] == column_val
    filtred_df = df_[mask]
    return filtred_df

class MultiText:
    def __init__(self, df) -> None:
        self._df = df

    def filter_df_value(self, filtred_column_name, filtred_column_value, returned_column_val):
        """
        make filter in df.returne one value
        """
        res = self._df.loc[self._df[filtred_column_name]
            == filtred_column_value, returned_column_val]

        return res

    def df_to_dict(self, df, rename_dict):
        df = df.rename(columns=rename_dict)
        res = df.set_index("S_ID").to_dict(orient="index")
        return res

    def add_space_data(self, filtred_col_value, key_column_names, k_shot_names):
        k_str = [self._df.loc[self._df["S_ID"] == filtred_col_value,
                            col_name].values[0] for col_name in key_column_names]
        k_dict = dict(zip(k_shot_names, k_str))
        sb = StringBuilder()

        def round_for_str(val):
            res = round(val) if isinstance(val, (int, float)) else val
            return res
        for k, v in k_dict.items():
            k = round_for_str(k)
            v = round_for_str(v)
            sb.Append(str(k))
            sb.Append(str(v))
            sb.Append("\n")
        return sb

    def add_mtext_to_df(self, new_m_text_col_name: str, key_column_names: str, k_shot_names: str):
        """ 
        add column with text to df. key_column_names -> column name of value. k_shot_names->Prefix
        """
        self._df[new_m_text_col_name] = self._df.apply(lambda x:
                                        self.add_space_data(
                                        x["S_ID"], key_column_names, k_shot_names),
                                        axis=1)
        return self._df

class Writer:
    def __init__(self, file_path, data) -> None:
        """
        write file to html,json by file path (endwith file extation)
        """
        self.file_path = file_path
        self.data = data

    def write_file(self):
        if self.file_path.endswith(".json"):
            self.to_json()
        elif self.file_path.endswith(".html"):
            self.to_html()
        else:
            print("wrong file format")

    def to_json(self):
        with open(self.file_path, "w", encoding='utf-8') as write_file:
            json.dump(self.data, write_file, indent=4, ensure_ascii=False)

    def to_html(self):
        with open(self.file_path, "w", encoding="utf-8") as write_file:
            write_file.writelines('<meta charset="UTF-8">\n')
            write_file.write(self.data)





