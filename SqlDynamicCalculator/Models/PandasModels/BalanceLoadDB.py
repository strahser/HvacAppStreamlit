from dataclasses import dataclass, field
import pandas as pd


@dataclass()
class BalanceLoadDB:
	input_excel_sheet: str = None  # existing excel sheet Unique
	df_new_table_name: str = None  # for db table. Unique
	balance_type_selected: str = None
	df_joined_column_name: str = None  # join
	df_total_sum_column_name: str = None  # for parsing from excel
	df_new_sum_column_name: str = None  # sum column
	df_group_table_values: pd.DataFrame = None  # data frame add
	df_space_joined_table_values: pd.DataFrame = None  # data frame join space data and add load data
	df_table_label: str = None  # to Excel sheet
	default_columns: list[str] = None