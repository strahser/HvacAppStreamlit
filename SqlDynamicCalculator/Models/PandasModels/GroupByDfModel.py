from SQL.SqlModel.SqlConnector import SqlConnector
from SqlDynamicCalculator.Models.PandasModels.ConfigModel import *
from SqlDynamicCalculator.Models.PandasModels.BalanceLoadDB import *
from SqlDynamicCalculator.Models.PandasModels.InputViewModel import *
from SqlDynamicCalculator.CategoryDb import *


@dataclass()
class BalanceTypeList:
	balance_name: str = None
	balance_data: list[BalanceLoadDB] = field(default_factory=list)

	def create_balance_model(self):
		balance_model = GroupByDfModel()
		balance_model_data = balance_model.create_config_model()
		return balance_model_data

	def create_balance_list(self):
		balance_list = []
		for name in CategoryDb.__annotations__.keys():
			balance_type = BalanceTypeList()
			balance_type.balance_name = getattr(CategoryDb, name)
			balance_list.append(balance_type)
		return balance_list


class GroupByDfModel:
	def __init__(self, con=SqlConnector.conn_sql):
		"""Parsing BalanceConstants.balance_load_columns_table. add to BalanceLoadDB  group by df """
		self.conn = con

	def create_config_model(self) -> list[BalanceLoadDB]:
		df_dict = SqlDFLoad().get_balance_load_df_table().to_dict("records")
		all_excel_sheets = flatten(
			self.conn.cursor().execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
		d_class_list = []
		if df_dict:
			for val in df_dict:
				balance_db = BalanceLoadDB(**val)
				db_table_name = str(val["input_excel_sheet"])
				if db_table_name in all_excel_sheets:
					group_df = pd.read_sql(
						f"""
					select {balance_db.df_joined_column_name},sum({balance_db.df_total_sum_column_name})
					as {balance_db.df_new_sum_column_name}  from {db_table_name}
					GROUP BY {balance_db.df_joined_column_name}
										""", self.conn)
					balance_db.df_group_table_values = group_df
					d_class_list.append(balance_db)
				else:
					st.exception(f"no {balance_db.df_new_table_name} in excel book")
		return d_class_list
