from PrincipalSchems.View.StaticView import *


class DynamicBaseView:
	
	def __init__(self, df_: pd.DataFrame, key, columns_number):
		"""add dynamic text input System Name, flow input, level input. Disable

        Args:
            df_ (pd.DataFrame): _description_
            columns_number (int, optional): _description_. Defaults to 10.
        """
		self.equipment_config_scheme_list = ["Equipment level", "Equipment Flow", "Equipment symbol", "Equipment label"]  # equipment config
		self.columns_number = columns_number
		self.columns = st.columns(columns_number)
		self.df_ = df_
		self.key = key

	def add_system_widget_to_df(self, column_number=0, _id=0):
		self.columns[column_number].write("System Name")
		for ind, row in self.df_.iterrows():
			setattr(
				self, f"system_label_{row['system']}_{_id}",
				self.columns[column_number].text_input(
					"#",
					row["system"],
					key=f"{self.key} system_label_{row['system']}_{_id}",
					label_visibility="collapsed",
					disabled=True))
	
	# optional conflict with DynamicLevelView.add_level_widget_to_df
	def add_flow_widget_to_df(self, column_number=1, _id=0):
		self.columns[column_number].write("System Flow")
		for ind, row in self.df_.iterrows():
			setattr(self, f"flow_label{row['system']}_{_id}",
			        self.columns[column_number].text_input(
				        "#",
				        round(row["flow"], 1),
				        key=f"{self.key} flow_label{row['system']}_{_id}",
				        label_visibility="collapsed",
			        )
			        )
