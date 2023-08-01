import pandas as pd


# region Utility

class SystemGroupCreator:

	@staticmethod
	def create_dictionary_from_df(df_: pd.DataFrame, main_columns: list) -> dict:
		"""
        create dictionary from df filtred by self.main_columns and remove none system
        """
		clear_df = df_[main_columns]
		clear_dict = clear_df.to_dict("split")
		new_dict = {}
		for val in clear_dict["data"]:
			temp = []
			for val1 in val:
				if not isinstance(val1, float):
					temp.append(val1)
			new_dict[temp[0]] = temp[1:]

		return new_dict


def get_system_flow_groups(
		df: pd.DataFrame,
		system_columns: list,
		flow_columns: list,
) -> pd.DataFrame:
	empty_df = []

	for sys, flow in zip(system_columns, flow_columns):
		temp = (
			df.groupby(sys)[flow]
			.sum()
			.reset_index()
			.rename(columns={sys: "system", flow: "flow"})
		)
		empty_df.append(temp)
	concate_df = pd.concat(empty_df, axis=0)
	return concate_df


# endregion

