import pandas as pd


def get_group_table(init_df: pd.DataFrame, group_fild: pd, agg_fild: str, agg_funk: list) -> pd.DataFrame:
	agg_dict = {
		"sum": "sum",
		"mean": "mean",
		"max": "max",
		'count': 'count',
		"all": ['sum', 'mean', 'median', 'min', 'max', 'count', 'std', 'var', 'mad', ],
		'describe': ['sum', 'describe']
	}
	if group_fild and agg_fild and group_fild != agg_fild:
		if agg_funk == "to list":
			df_group = init_df.groupby(group_fild)[agg_fild].apply(list).reset_index()
			return df_group
		else:
			try:
				df_group = init_df.groupby(group_fild)[agg_fild].agg(agg_dict[agg_funk]).reset_index()
				return df_group
			except Exception as e:
				print(e)
	else:
		return pd.DataFrame()


def get_pivot_table(
		init_df: pd.DataFrame,
		pivot_index_multiselect: list,
		pivot_values_multiselect: list,
		pivot_columns_multiselect: list,
		pivot_agg_func_multiselect: list
	):
	if pivot_values_multiselect:
		df_pivot = pd.pivot_table(
			data=init_df,
			index=pivot_index_multiselect,
			values=pivot_values_multiselect,
			columns=pivot_columns_multiselect,
			aggfunc=pivot_agg_func_multiselect,
			fill_value=0,
			margins=True
		).reset_index()
		return df_pivot
