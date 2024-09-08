
from SqlDynamicCalculator.View.PandasView.JoinAdditionalLoadView import *


class BalanceAddDataView:
	def __init__(self, input_view: InputView):
		"""ADD Data with JOIN Balance View"""
		self.balance_model_data = None
		self.input_view = input_view
		self.select_space_data = InputViewModel(input_view.selected_excel_sheet).get_loaded_loaded_sheet()

	def create_excel_df_list_show(self):
		st.markdown("#### Input Space Data")
		with st.expander("+"):
			st.dataframe(self.select_space_data)

	def create_balance_config_view(self):
		self.create_excel_df_list_show()

		for balance_type in self.balance_list:
			st.markdown(f"#### {balance_type.balance_name}")
			with st.expander("+"):
				for balance_data in self.balance_model_data:
					join_balance = JoinBalanceType(balance_type, balance_data)
					join_balance.add_balance_name_to_model_data()
					if join_balance.condition:
						st.markdown(f"""#### Table  of Additional Load:  {balance_data.df_new_table_name}""")
						with st.expander("+"):
							col1, col2 = st.columns([2, 8])
							with col2:
								st.write(pd.DataFrame(balance_data.df_group_table_values))
							with col1:
								join_table_name = join_balance.add_table_name()
							df_join = join_balance.create_join_table(self.select_space_data)
							st.subheader(join_table_name)
							st.write(df_join)
