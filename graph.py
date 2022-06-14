import math
import random
import networkx as nx
import matplotlib.pyplot as plt


def is_graph(V, E):
	tv = True
	for (u, v) in E:
		tv = tv and (u in V) and (v in V)
	return tv


def cartesian_product(X, Y):
	"""生成两个集合的笛卡尔积"""
	XY = set({})
	for x in X:
		for y in Y:
			XY.add((x, y))
	return XY
	

def create_graph(m, n):
	"""m 个顶点无向图"""
	global V, XY
	V = range(m)
	XY = cartesian_product(V, V)
	E = random.sample(XY, n);
	E = set(E)
	for (u, v) in E:
		if (v, u) not in E:
			E = E | {(v, u)}
	V = set(V)
	return [V, E]


def create_digraph(m, n):
	"""m 个顶点的有向图"""
	global V, XY
	V = range(m)
	XY = cartesian_product(V, V)
	E = random.sample(XY, n)
	V = set(V)
	E = set(E)
	return [V, E]


def knight_tour_graph(n):
	"""骑士周游图"""
	p_8 = [[-1, -2], [-2, -1], [-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2]]
	N = n * n
	V = list(range(N))
	E = set({})
	for k in range(N):
		j = k % n
		i = k // n
		for [u, v] in p_8:
			if 0 <= i + u < n and 0 <= j + v < n:
				E = E | {(k, (i + u) * n + (j + v))}
	return [V, E]
	

def draw_graph(E):
	G = nx.Graph()
	G.add_edges_from(E)
	nx.draw(G, node_size=200, node_color='r', with_labels=True, font_color='w')
	plt.show()
	return


def draw_digraph(E):
	G = nx.DiGraph()
	G.add_edges_from(E)
	nx.draw(G, node_size=200, node_color='r', with_labels=True, font_color='w')
	plt.show()
	return


def adjacent_list(V, E):
	"""邻接表"""
	Ea = []
	for w in V:
		e0 = [w]
		e1 = []
		for (u, v) in E:
			if u == w and v not in e1:
				e1 = e1 + [v]
			if v == w and u not in e1:
				e1 = e1 + [u]
		e0 = e0 + [sorted(e1)]
		Ea = Ea + [e0]
	return sorted(Ea)


def mn_graph(m, n):
	V = set({})
	E = set({})
	for i in range(m):
		for j in  range(n - 1):
			u = i * n + j
			v = u + 1
			V = V | {u, v}
			E = E | {(u, v)}
	for i in range(m - 1):
		for j in range(n):
			u = i * n + j
			v = u + n
			E = E | {(u, v)}
	return [V, E]


def weighted_graph(V0, E0, W0):
	V = V0
	E = set({})
	for (u, v) in E0:
		w = random.randint(1, W0)
		E = E | {(w, u, v)}
	return [V, E]


def binary_tree(nodes):
	nodes = list(nodes)
	if len(nodes) == 0:
		return []
	if len(nodes) == 1:
		return nodes
	k = int(len(nodes) / 2)
	a = nodes.pop(k)
	l_nodes = nodes[0:k]
	r_nodes = nodes[k:]
	l_tree = binary_tree(l_nodes)
	r_tree = binary_tree(r_nodes)
	return [a, l_tree, r_tree]


def frequency_list(V: list):
	W0 = []
	tmp = []
	s = 0
	for u in V:
		if u in tmp:
			continue
		tmp.append(u)
		w = V.count(u)
		W0 = W0 + [[u, w]]
		s = s + w
	W = []
	for [u, w] in W0:
		w = math.floor((w / s) * 10000) / 10000
		W = W + [[u, w]]
	return W


def huffman_tree(W):
	W0 = []
	for [a, w] in W:
		W0 = W0 + [[w, a]]
	tree = sorted(W0)
	while len(tree) != 1:
		w = tree[0][0] + tree[1][0]
		w = math.floor(w * 10000) / 10000
		tree = [[w, tree[0], tree[1]]] + tree[2:]
		tree.sort(key=lambda x: (x[0]))
	return tree[0]


def complete_bigraph_set(m, n):
	Vx = set(range(m))
	Vy = set(range(n))
	V0 = set({})
	V1 = set({})
	E = set({})
	for u in Vx:
		for v in Vy:
			x = 'x' + str(u)
			y = 'y' + str(v)
			V0 = V0 | {x}
			V1 = V1 | {y}
			E = E | {(x, y)}
	return [V0, V1, E]


def complete_graph_set(n):
	V, E = set({}), set({})
	for i in range(n):
		V = V | {i}
		for j in range(n):
			E = E | {(i, j)}
	return V, E
