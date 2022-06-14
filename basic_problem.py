import math

import graph as g


def sub_euler_circuit(E, v0):
	"""从一点出发，找到一条回路，返回顺序和使用的边"""
	circuit = tuple([v0])
	S = set({})
	while circuit[0] != circuit[-1] or len(circuit) == 1:
		y = circuit[-1]
		for (u, v) in E:
			if u == y:
				circuit = circuit + tuple([v])
				E = E - {(u, v)}
				S = S | {(u, v)}
				break
	return [circuit, S]


def set_2v(E):
	"""从边集产生点集"""
	V = set({})
	for (u, v) in E:
		V = V | {u, v}
	return V


def euler_circuit(E, v0):
	"""给出欧拉回路"""
	[circuit, S] = sub_euler_circuit(E, v0)
	E = E - S
	while E != set({}):
		V1 = set(circuit)
		V2 = set_2v(E)
		V1V2 = V1 & V2
		# 已有回路和整个图的公共点集
		for v0 in V1V2:
			# 从公共点集，生成回路点集和边
			[sub_circuit, S] = sub_euler_circuit(E, v0)
			if S == set({}):
				continue
			k = circuit.index(v0)
			circuit = circuit[0: k] + sub_circuit + circuit[k + 1: -1] + tuple([circuit[-1]])
			E = E - S
			break
	return circuit


def tour_path0(V, E, path, m):
	while len(path) < m:
		w = path[-1]
		i = V.index(w)
		E1 = E[i]
		E2 = E1[1]
		for u in E2:
			if u not in path:
				path.append(u)
				break
		if path[-1] == w:
			break
	return path


def tour_path1(V, E, path, m):
	v = path.pop()
	while len(path) != 0:
		u = path[-1]
		i = V.index(u)
		E1 = E[i]
		E2 = E1[1]
		k = E2.index(v)
		while k < len(E2) - 1:
			k += 1
			v = E2[k]
			if v not in path:
				path.append(v)
				break
		if u != path[-1]:
			break
		v = path.pop()
	return path


def tour_path(V, E, path, m):
	if len(path) == m:
		path = tour_path1(V, E, path, m)
	while len(path) != 0:
		path = tour_path0(V, E, path, m)
		if len(path) == m:
			break
		path = tour_path1(V, E, path, m)
	return path


def hamilton_path(V, E, v0):
	global Ea, paths
	V = sorted(V)
	Ea = g.adjacent_list(V, E)
	paths = set({})
	path = [v0]
	m = len(V)
	path = tour_path(V, Ea, path, m)
	paths = paths | {tuple(path)}
	k = 1
	while len(path) == m:
		if k >= 100:
			break  # end
		path = tour_path(V, Ea, path, m)
		if len(path) == m:
			paths = paths | {tuple(path)}
			k += 1
	return paths


def degree_set_w(V, E):
	V = sorted(V)
	m = len(V)
	di = [0] * m
	do = [0] * m
	d = [0] * m
	for (w, u, v) in E:
		i = V.index(u)
		j = V.index(v)
		di[j] += 1
		do[i] += 1
		d[i] += 1
		d[j] += 1
	return [d, di, do]


def short_path(V, E, di, Hx, path, zn):
	V = sorted(V)
	Pm = []
	for p in path:
		vn = p[-1]
		if vn == zn:
			Pm = Pm + [p]
			continue
		if di[V.index(vn)] != 0:
			Pm = Pm + [p]
			continue
		for (w, u, v) in E:
			if u == vn:
				kv = V.index(v)
				if di[kv] > 0:
					di[kv] = di[kv] - 1
				vw = p[0] + w
				if vw <= Hx[kv]:
					Hx[kv] = vw
					e = [vw] + p[1:] + [v]
					Pm = Pm + [e]
	return [di, Hx, Pm]


def shortest_path(V, E, v0, vn):
	V = sorted(V)
	[d, di, do] = degree_set_w(V, E)
	Pm0 = []
	Pm = [[0, v0]]
	inf = 10000
	Hx = [inf for x in range(len(V))]
	Hx[0] = 0
	while Pm0 != Pm:
		Pm0 = Pm
		[di, Hx, Pm] = short_path(V, E, di, Hx, Pm0, vn)
	Pm = sorted(Pm)
	return [Hx, Pm]


def step_u0v(di0, E):
	S = set({})
	for u0 in di0:
		for (w, u, v) in E:
			if u == u0:
				S = S | {(w, u, v)}
	return S


def step_uv0(do0, E):
	S = set({})
	for v0 in do0:
		for (w, u, v) in E:
			if v == v0:
				S = S | {(w, u, v)}
	return S


def te_path(S, Hx, di):
	di0 = set({})
	for (w, u, v) in S:
		if Hx[v] < Hx[u] + w:
			Hx[v] = Hx[u] + w
		if di[v] > 0:
			di[v] = di[v] - 1
		if di[v] == 0:
			di0 = di0 | {v}
	return [Hx, di, di0]


def tl_path(S, Hy, do):
	do0 = set({})
	for (w, u, v) in S:
		if Hy[u] > Hy[v] - w:
			Hy[u] = Hy[v] - w
		if do[u] > 0:
			do[u] = do[u] - 1
		if do[u] == 0:
			do0 = do0 | {u}
	return [Hy, do, do0]


def cratical_te(V, E, di, v0, vn):
	Hx = [0] * len(V)
	
	di0 = {v0}
	while vn not in di0:
		S = step_u0v(di0, E)
		[Hx, di, di0] = te_path(S, Hx, di)
		E = E - S
	return Hx


def cratical_tl(V, E, do, Hn, v0, vn):
	Hy = [1000] * len(V)
	Hy[len(V) - 1] = Hn
	do0 = {vn}
	while v0 not in do0:
		S = step_uv0(do0, E)
		[Hy, do, do0] = tl_path(S, Hy, do)
		E = E - S
	return Hy


def cratical_path(V, E, di, do, v0, vn):
	Hx = cratical_te(V, E, di, v0, vn)
	Hn = Hx[len(V) - 1]
	Hy = cratical_tl(V, E, do, Hn, v0, vn)
	V = list(V)
	N = len(V)
	C = set({})
	for k in range(N):
		if Hx[k] == Hy[k]:
			C = C | {V[k]}
	Pc = set({})
	for (w, u, v) in E:
		if u in C and v in C:
			Pc = Pc | {(w, u, v)}
	return Pc, Hx, Hy


def preorder_traversal(tree):
	if len(tree) == 0:
		return []
	if len(tree) == 1:
		return [tree[0]]
	else:
		return [tree[0]] + preorder_traversal(tree[1]) + preorder_traversal(tree[2])


def inorder_traversal(tree):
	if len(tree) == 0:
		return []
	if len(tree) == 1:
		return [tree[0]]
	else:
		return preorder_traversal(tree[1]) + [tree[0]] + preorder_traversal(tree[2])


def postorder_traversal(tree):
	if len(tree) == 0:
		return []
	if len(tree) == 1:
		return [tree[0]]
	else:
		return preorder_traversal(tree[1]) + preorder_traversal(tree[2]) + [tree[0]]


def __huffman_coding(subtree, code):
	if len(subtree) == 2:
		return [[subtree[1], code]]
	else:
		node0 = subtree[1]
		node1 = subtree[2]
		code = __huffman_coding(node0, code + '0') + __huffman_coding(node1, code + '1')
		return code


def huffman_coding(tree):
	code0 = __huffman_coding(tree[1], '0')
	code1 = __huffman_coding(tree[2], '1')
	return code0 + code1


def coding_entropy(W, C):
	r0 = 0
	r = 0
	W = sorted(W)
	C = sorted(C)
	for k in range(len(W)):
		r0 -= W[k][1] * math.log2(W[k][1])
		r += W[k][1] * len(C[k][1])
		r0 = math.floor((r0) * 1000) / 1000
		r = math.floor((r) * 1000) / 1000
	return [r0, r]


def prim_span_tree(V, E):
	E = sorted(E)
	[w, u, v] = E[0]
	Vt = {u, v}
	Et = {(w, u, v)}
	del E[0]
	n = len(V)
	while len(Et) < n - 1:
		i = 0
		while i < len(E):
			[w, u, v] = E[i]
			if (u in Vt and v not in Vt) or (u not in Vt and v in Vt):
				Et = Et | {(w, u, v)}
				Vt = Vt | {u, v}
				del E[i]
				break
			i = i + 1
	return [Vt, Et]


def is_cycled(V, E, u0, v0):
	tv = False
	Vc = {u0, v0}
	Ec = {(u0, v0)}
	n = 0
	while n != len(Vc):
		n = len(Vc)
		for (w, u, v) in E:
			if (u in Vc) and (v in Vc):
				tv = True
				return tv
			if (u in Vc and v not in Vc) or (u not in Vc and v in Vc):
				Ec = Ec | {(u, v)}
				Vc = Vc | {u, v}
				E = E - {(w, u, v)}
				break
	return tv


def kruskal_span_tree(V, E):
	E = sorted(E)
	Vt = set({})
	Et = set({})
	n = len(V)
	k = 0
	i = 0
	while len(Et) < n - 1:
		[w, u, v] = E[i]
		i = i + 1
		if (u in Vt) and (v in Vt):
			if is_cycled(Vt, Et, u, v):
				continue
		Et = Et | {(w, u, v)}
		Vt = Vt | {u, v}
	return [Vt, Et]


def saturated_V(path):
	Vs = set(path)
	return Vs


def unsaturated_V(V, Vs):
	Vu = V - Vs
	return Vu


def path2match(V1, V2, path):
	match = set({})
	n = len(path)
	for k in range(0, n, 2):
		u = path[k]
		v = path[k + 1]
		if u in V1:
			match = match | {(u, v)}
		else:
			match = match | {(v, u)}
	return match


def augment_path(Vu, Eu, path):
	v0 = path[0]
	un = path[-1]
	u0 = -1
	vn = -1
	for (u, v) in Eu:
		if v == v0 and u in Vu:
			u0 = u
		if u == v0 and v in Vu:
			u0 = v
	for (u, v) in Eu:
		if v == un and u in Vu:
			vn = u
		if u == un and v in Vu:
			vn = v
	if u0 != -1 and vn != -1:
		path = [u0] + path + [vn]
	return path


def augment_paths(V, E, path):
	Vs = saturated_V(path)
	Vu = unsaturated_V(V, Vs)
	Eu = E
	m = 0
	while len(path) != m:
		m = len(path)
		path = augment_path(Vu, Eu, path)
		Vs = saturated_V(path)
		Vu = unsaturated_V(V, Vs)
	return path


def match_max_set(V1, V2, E, path):
	Vu = V1 | V2
	Eu = E
	match = set({})
	match_set = set({})
	Vs = set({})
	m = 0
	while len(path) != m:
		m = len(path)
		path = augment_paths(Vu, Eu, path)
		match = path2match(V1, V2, path)
		match_set = match_set | match
		Vs = Vs | saturated_V(path)
		Eu = E
		for (u, v) in E:
			if u in Vs or v in Vs:
				Eu = Eu - {(u, v)}
		if Eu == set({}):
			break
		for (u, v) in Eu:
			break
		match = set({})
		path = [u, v]
		m = 0
	return match_set