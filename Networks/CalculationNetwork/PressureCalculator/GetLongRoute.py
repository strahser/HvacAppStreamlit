from Networks.CalculationNetwork.PressureCalculator.NetworkGraph import NetworkGraph


class GetLongRoute:
	def __init__(self, df, from_column: str = "from", to_column: str = "to",
	             value_column: str = "full_pressure") -> None:
		self.df = df
		self.from_column = from_column
		self.to_column = to_column
		self.value_column = value_column

	def _get_long_route(self):
		self.graf = NetworkGraph(self.df)
		self.graf.create_network(self.from_column, self.to_column, self.value_column)
		long_route = self.graf.get_longest_network()
		return long_route

	def get_long_df(self):
		long_route = set(self._get_long_route())
		filtred_list = long_route & set(self.df[self.from_column].values)
		mask = self.df[self.from_column].isin(filtred_list)
		df_filter = self.df[mask]
		return df_filter
