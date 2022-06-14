import copy

from big_homework.util import Graph, Heap, Distance

inf = float('inf')
magic_num = -2147483648


def dijkstra(s: int, g: Graph):
	dis, n, cnt, heap, vis = dict().fromkeys(g.head.keys(), inf), len(g.head), 0, Heap(),\
		dict().fromkeys(g.head.keys(), False)
	heap.push(Distance(s, 0))
	while heap.is_empty() is False:
		d: Distance = heap.pop(0)
		if vis[d.u] is False:
			dis[d.u], vis[d.u] = d.w, True
			e: Graph.Node = g.head[d.u]
			while e is not None:
				v, e, w = e.to, e.nxt, e.w
				if dis[v] > dis[d.u] + w:
					dis[v] = dis[d.u] + w
					heap.push(Distance(v, int(dis[v])))
	return dis


def spfa(s: int, g: Graph):
	i, dis, queue, vis, cnt = 0, dict().fromkeys(g.head.keys(), inf), [s], dict().fromkeys(g.head.keys(), False),\
		dict().fromkeys(g.head.keys(), 0)
	dis[s], vis[s], flag = 0, True, False
	while len(queue) > 0:
		if flag:
			break
		u, vis[u] = queue.pop(), False
		e: Graph.Node = g.head[u]
		while e is not None:
			v, e, w = e.to, e.nxt, e.w
			if dis[v] > dis[u] + w:
				dis[v], cnt[v] = dis[u] + w, cnt[u] + 1
				if cnt[v] >= len(g.head.keys()):
					flag = True
					break
				if vis[v] is False:
					queue.append(v)
					vis[v] = True
	if flag:
		return None
	return dis


def floyd(g: Graph):
	dis = g.get_dict()
	for k in dis.keys():
		for i in dis.keys():
			for j in dis.keys():
				dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j])
	return dis


def johnson(g: Graph):
	o, dis, tp = copy.deepcopy(g), g.get_dict(), g.head.keys()
	for key in tp:
		o.add(magic_num, key, 0)
	h = spfa(magic_num, o)
	if h is None:
		return None
	o = copy.deepcopy(g)
	for u in o.head.keys():
		e: Graph.Node = o.head[u]
		while e is not None:
			e.w, e = e.w + h[u] - h[e.to], e.nxt
	for u in o.head.keys():
		d = dijkstra(u, o)
		for v in d.keys():
			dis[u][v] = inf if d[v] == inf else d[v] - h[u] + h[v]
	return dis


if __name__ == '__main__':
	arr, gh = [[3, 4, 8], [4, 5, 20], [5, 4, 90], [100, 4, 8]], Graph()
	for tmp in arr:
		gh.add(tmp[0], tmp[1], tmp[2])
	print(dijkstra(3, gh))
	print(spfa(3, gh))
	print(floyd(gh))
	print(johnson(gh))
