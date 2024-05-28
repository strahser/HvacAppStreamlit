# pip install streamlit-aggrid
import pandas as pd
from InsertTerminalsPandas.Static.ColumnChoosing import ColumnChoosing
from library_hvac_app.streamlit_custom_functions import AggGridOptions


def get_level_filter_grid_df(_df: pd.DataFrame, level_value: str) -> list[str]:
    """filter input df by level and create agg table"""
    level_condition = _df[ColumnChoosing.S_level] == level_value
    df_ = _df[level_condition]
    selected_df_data = AggGridOptions(df_)
    selected_df_data_df = selected_df_data.create_ag_selected_row_df("selected_rows")
    selected_df_data_df = pd.DataFrame(selected_df_data_df)
    selected_df_data_id = selected_df_data_df[ColumnChoosing.S_ID].to_list() if not selected_df_data_df.empty else []
    return selected_df_data_id
