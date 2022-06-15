inf = float('inf')


class Graph:
	def __init__(self):
		self.head = dict()
	
	class Node:
		def __init__(self, to: int, nxt, w: int):
			self.nxt = nxt
			self.to = to
			self.w = w
	
	def add(self, u: int, v: int, w: int):
		e = self.Node(v, self.head.get(u), w)
		self.head[u] = e
		self.head.setdefault(v, None)
		
	def get_dict(self):
		g = dict().fromkeys(self.head.keys(), None)
		for k in g.keys():
			g[k] = dict().fromkeys(self.head.keys(), inf)
		for u in self.head.keys():
			e: Graph.Node = self.head[u]
			while e is not None:
				g[u][e.to], e = min(g[u][e.to], e.w), e.nxt
		for u in g.keys():
			g[u][u] = min(g[u][u], 0)
		return g


class Heap:
	def __init__(self):
		self.heap = []
	
	def push(self, elem):
		self.heap.append(elem)
		s = len(self.heap) - 1
		while s > 0:
			p = s >> 1
			if self.heap[p] > self.heap[s]:
				self.heap[p], self.heap[s] = self.heap[s], self.heap[p]
			else:
				break
			p, s = s >> 1, p
	
	def pop(self, idx: int):
		rt = None
		try:
			rt, self.heap[idx] = self.heap[idx], self.heap[-1]
			self.heap.pop(-1)
		except IndexError:
			print("The heap is Empty now, can't do pop.")
			return rt
		p, s, size = idx, idx << 1, len(self.heap)
		while s < size:
			if s + 1 < size and self.heap[s + 1] < self.heap[s]:
				s += 1
			if self.heap[p] > self.heap[s]:
				self.heap[p], self.heap[s] = self.heap[s], self.heap[p]
			else:
				break
			p, s = s, s << 1
		return rt
	
	def is_empty(self):
		return len(self.heap) == 0
	
	
class Distance:
	def __init__(self, u: int, ww: int):
		self.u = u
		self.w = ww
	
	def __eq__(self, other):
		return self.w == other.w
	
	def __lt__(self, other):
		return self.w < other.w
	
	def __le__(self, other):
		return self.w <= other.w
	
	def __gt__(self, other):
		return self.w > other.w
	
	def __ge__(self, other):
		return self.w >= other.w
	
	
if __name__ == '__main__':
	arr, heap, ans = [1, 6, 8, 9, 0, 4, 6], Heap(), []
	for i in arr:
		heap.push(i)
		print(heap.heap)
	for i in range(20):
		ans.append(heap.pop(0))
		print(heap.heap)
	print(ans)
	