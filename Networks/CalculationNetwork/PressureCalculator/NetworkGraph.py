import networkx as nx


class NetworkGraph:
	def __init__(self, df) -> None:
		self.df = df
		self.G = nx.DiGraph()

	def create_network(self, from_column, to_column, value_column):
		"""
        add vertix to graph for example 'S_ID',main_idx''S_SA_fresh'
        """
		for (
				sourse,
				end_p,
				weght,
		) in zip(self.df[from_column], self.df[to_column], self.df[value_column]):
			self.G.add_edge(sourse, end_p, weight=weght)
		return self.G

	def get_longest_network(self):
		longest_path = nx.dag_longest_path(self.G, weight="weight")
		return longest_path

	def get_max_pressure_value(self):
		max_value = nx.dag_longest_path_length(self.G, weight="weight")
		return max_value