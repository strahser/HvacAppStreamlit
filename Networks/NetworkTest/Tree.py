import networkx as nx
import matplotlib.pyplot as plt


def plot_graph():
	G = nx.Graph()

	G.add_edge("a", "b", weight=0.6)
	G.add_edge("a", "c", weight=0.2)
	G.add_edge("c", "d", weight=0.1)
	G.add_edge("c", "e", weight=0.7)
	G.add_edge("c", "f", weight=0.9)
	G.add_edge("a", "d", weight=0.3)

	elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
	esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]

	pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

	# nodes
	nx.draw_networkx_nodes(G, pos, node_size=700)

	# edges
	nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
	nx.draw_networkx_edges(G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed")

	# node labels
	nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
	# edge weight labels
	edge_labels = nx.get_edge_attributes(G, "weight")
	nx.draw_networkx_edge_labels(G, pos, edge_labels)

	ax = plt.gca()
	ax.margins(0.08)
	plt.axis("off")
	plt.tight_layout()
	plt.show()


def add_sums(tree):
	if 'children' not in tree:
		return tree['price']
	s = sum(map(add_sums, tree['children']))
	if 'price' in tree:
		s += tree['price']
	tree['sum'] = s
	return s


test_data = [
	{
		"id": 1,
		"type": "group",
		"name": "test-group 1",
		"price": 0,
		"sum": 0,
		"children": [
			{
				"id": 2,
				"type": "position",
				"name": "test-inner 1",
				"price": 5
			},
			{
				"id": 3,
				"type": "position",
				"name": "test-inner 2",
				"price": 10
			}
		]
	},
	{
		"id": 4,
		"type": "group",
		"name": "test-group 2",
		"sum": 0,
		"children": [
			{
				"id": 5,
				"type": "position",
				"name": "test-inner 3",
				"price": 5
			},
			{
				"id": 6,
				"type": "group",
				"name": "test-group 3",
				"sum": 0,
				"children": [
					{
						"id": 7,
						"type": "position",
						"name": "test-inner 4",
						"price": 5
					},
					{
						"id": 8,
						"type": "position",
						"name": "test-inner 5",
						"price": 10
					}
				]
			}
		]
	}
]


class Node:
	def __init__(self, name, weight, children=None):
		self.name = name
		self.children = children
		self.weight = weight
		self.weight_plus_children = weight
		self.get_all_weight()

	def get_all_weight(self):
		if self.children is None:
			return self.weight_plus_children
		else:
			for child in self.children:
				self.weight_plus_children += child.get_weigth_with_children()
		return self.weight_plus_children

	def get_weigth_with_children(self):
		return self.weight_plus_children

	def __str__(self):
		return f"{self.name}-{self.weight_plus_children}"


s1_level1 = Node('s1_level1', 5000)
s1_level2 = Node('s1_level1', 320)
s1_level3 = Node('s1_level1', 1000)
level1 = Node('level1', 0, [s1_level1])
level2 = Node('level2', 0, [level1, s1_level2])
level3 = Node('level3', 0, [level2, s1_level3])
print(level3)


# Networkx
def max_att_sum(G, node, attr):
	if nx.descendants(G, node):
		return nx.dag_longest_path_length(G.subgraph(nx.descendants(G, node) | {node}))
	else:
		return G.nodes[node][attr]


def get_sum_of_children(graph, node):
	sum_children = 0
	children = graph.successors(node)
	for child in children:
		sum_children += child
	return sum_children
