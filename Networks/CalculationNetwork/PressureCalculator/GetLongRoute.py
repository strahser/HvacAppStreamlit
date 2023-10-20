from Networks.CalculationNetwork.PressureCalculator.NetworkGraph import NetworkGraph


class GetLongRoute:
	def __init__(self, df) -> None:
		self.df = df

	def _get_long_route(
			self,
	):
		self.graf = NetworkGraph(self.df)
		self.graf.create_network("from", "to", "full_pressure")
		long_route = self.graf.get_longest_network()
		return long_route

	def get_long_df(self):
		long_route = set(self._get_long_route())
		filtred_list = long_route & set(self.df["from"].values)
		mask = self.df["from"].isin(filtred_list)
		df_filter = self.df[mask]
		return df_filter