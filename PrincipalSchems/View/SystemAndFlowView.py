from PrincipalSchems.View.StaticView import *


class SystemAndFlowView:

	def __init__(self,
	             df_: pd.DataFrame,
	             unique_key="") -> None:
		"""create system,flow,system direction components data

        Args:
            df_ (pd.DataFrame): _description_
            unique_key (str, optional): _description_. Defaults to "".
        """
		self.unique_key = str(unique_key)
		self.df_ = df_

	def add_system_data_to_view(self):
		self.system_columns = st.multiselect("select system columns",
		                                     self.df_.columns,
		                                     key=f"{self.unique_key} system_columns"
		                                     )
		self.flow_columns = st.multiselect("select flow columns",
		                                   self.df_.columns,
		                                   key=f"{self.unique_key} flow_columns"
		                                   )
		self.vertical_direction_list = st.selectbox(
			'select schem vertical direction',
			MainSchemeConfig.vertical_direction_list,
			key=f"{self.unique_key} vertical_direction_list"
		)
		self.horizontal_direction_list = st.selectbox(
			'select schem horizontal direction',
			MainSchemeConfig.horizontal_direction_list,
            key = f"{self.unique_key} horizontal_direction_list"
        )