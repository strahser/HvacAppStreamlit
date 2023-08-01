from SqlDynamicCalculator.Models.PandasModels.ConfigModel import *
from SqlDynamicCalculator.CategoryDb import CategoryDb
from SqlDynamicCalculator.Models.PandasModels.ConfigModel import ConfigModel
from InputView.InputView import *
from SqlDynamicCalculator.Models.PandasModels.InputViewModel import *


class DbConfigView:
	def __init__(self, input_view: InputView):
		self.input_view = input_view
		self.balance_type_selected = None
		self.add_table_model = None
		self.excel_lists = None
		self.input_df = InputViewModel(self.input_view.selected_excel_sheet).get_loaded_loaded_sheet()
		self.input_excel_sheet = self.input_view.selected_excel_sheet

	def get_all_view_data(self):
		self.get_excel_lists()
		self.create_group_table_view()
		self.add_data_to_db()

	def get_excel_lists(self):
		with st.expander("Config Table"):
			st.subheader("Select Excel sheet for join")
			st.write("Selected Excel Sheet")
			st.dataframe(self.input_df)

	def _create_columns_names_select_box(self):
		if not self.input_df.empty:
			self.df_joined_column_name = st.selectbox("Select Joined Column", self.input_df.columns)
			self.df_total_sum_column_name = st.selectbox("Select Total Sum Column", self.input_df.columns)
			self.df_new_sum_column_name = st.text_input("New Sum Column Name", value=self.df_total_sum_column_name)
			self.df_new_table_name = st.text_input("New Table Name",
			                                       value=f"{self.input_view.selected_excel_sheet} sum_load",
			                                       disabled=True)
			self.balance_type_selected_list = [getattr(CategoryDb, val) for val in CategoryDb.__annotations__.keys()]

	def create_input_data_dict(self) -> dict:
		input_attr = ['input_excel_sheet', 'df_new_table_name', 'balance_type_selected', 'df_joined_column_name',
		              'df_total_sum_column_name', 'df_new_sum_column_name']
		attr_dict = {}
		for name in input_attr:
			attr_dict[name] = getattr(self, name)
		print(attr_dict)
		return attr_dict

	def create_group_table_view(self):
		with st.expander("Create Grouped Table"):
			col1, col2 = st.columns([2, 9])
			with col1:
				self._create_columns_names_select_box()
			with col2:
				try:
					df = create_group_sum(self.input_df,
					                      self.df_joined_column_name,
					                      self.df_total_sum_column_name,
					                      self.df_new_sum_column_name
					                      )
					st.write("Joined Tabel")
					st.dataframe(df)
				except Exception as e:
					st.warning(e)

	def add_data_to_db(self):
		with st.expander("Add data to DB"):
			self.balance_type_selected = st.selectbox("Select Balance Type", self.balance_type_selected_list)
			ConfigModel.create_balance_load_columns_table()
			create_table = st.button("Create Table")
			if create_table:
				self.create_input_data_dict()
				self.add_balance_data_table_to_db(self.create_input_data_dict())
			st.write("Balance Data Base Table")
			st.write(SqlDFLoad().get_balance_load_df_table())

	@staticmethod
	def add_balance_data_table_to_db(input_data_dict: dict):
		try:
			ConfigModel.add_balance_data_to_table(**input_data_dict)
			st.success("Add Data to DB")
		except Exception as e:
			st.warning(e)




