from InsertTerminalsPandas.TermilalView.ConfigStaticView import LabelListStatic, LayoutOptions, st, pd


class ConfigColumnChoosingView:
	def __init__(self, selected_df: pd.DataFrame,key):	
		self.selected_df = selected_df
		# self.column_confirm_checkbox = st.checkbox("confirm column choosing",key=f"{key} column_confirm_checkbox")
		for label_, attr_ in zip(LabelListStatic.label_list, LabelListStatic.attr_list):
			select_box = st.selectbox(label_, self.selected_df.columns,
			                          index=self._get_default_columns_values(attr_))
			setattr(self, attr_, select_box)

	def _get_default_columns_values(self, value: str):
		if value in self.selected_df.columns:
			return self.selected_df.columns.to_list().index(value)
		else:
			return 0
