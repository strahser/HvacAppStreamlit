import random

from anytree import Node, RenderTree, NodeMixin, LevelOrderGroupIter
import pandas as pd


class WNode(NodeMixin):

	def __init__(self, parent=None, name=None, weight=None):
		super(WNode, self).__init__()
		self.parent = parent
		self.name = name
		self.weight = weight

	def _post_detach(self, parent):
		self.weight = None


def print_tree(nodes: dict, roots: set) -> None:
	for root in roots:
		print()
		for pre, _, node in RenderTree(nodes[root]):
			print(f'{pre}{node.name} ({node.val})')


def add_nodes(nodes: dict, roots: set, parent: str, child: str, val: int) -> None:
	if parent not in nodes:
		nodes[parent] = Node(parent, val=0)
		roots.add(parent)
	if child not in nodes:
		nodes[child] = Node(child, val=val)
	else:
		nodes[child].val = val
	nodes[child].parent = nodes[parent]
	if child in roots:
		roots.remove(child)


def create_tree(df: pd.DataFrame):
	nodes = {}
	roots = set()
	for row in df.itertuples(index=False, name='df_row'):
		if row.to_branch is not None:
			add_nodes(nodes, roots, row.to_branch, row.from_branch, row.flow)
	print_tree(nodes, roots)
	return nodes, roots


f = WNode(parent=None, name="f", weight=0)
b = WNode(parent=f, name="b", weight=8)
a = WNode(parent=b, name="a", weight=6)
d = WNode(parent=b, name="d", weight=4)
c = WNode(parent=d, name="c", weight=0)
e = WNode(parent=d, name="e", weight=1)
g = WNode(parent=f, name="g", weight=0)
i = WNode(parent=g, name="i", weight=3)
h = WNode(parent=i, name="h", weight=2)

for pre, _, node in RenderTree(f):
	print("%s%s (%s) [Σ = %s]" %
	      (pre, node.name, node.weight or 0,
	       sum([item for sublist in
	            [[node.weight for node in children] for children in LevelOrderGroupIter(node)]
	            for item in sublist])))
