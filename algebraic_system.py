import numpy as np


SYSTEM = -1
p = -1
N = -1
Cn = -1


def create_klein():
	G = {'e', 'a', 'b', 'c'}
	return G


def mul_klein(a, b):
	G = ['e', 'a', 'b', 'c']
	km = np.array([['e', 'a', 'b', 'c'], ['a', 'e', 'c', 'b'], ['b', 'c', 'e', 'a'], ['c', 'b', 'a', 'e']])
	i, j = G.index(a), G.index(b)
	c = km[i, j]
	return c


def inv_klein(a):
	"""inverse element"""
	return a


def e_klein():
	"""identity element"""
	return 'e'


def is_sociative_law(G):
	tv = True
	for a in G:
		for b in G:
			for c in G:
				f0 = mul(mul(a, b), c)
				f1 = mul(a, mul(b, c))
				tv = tv & (f0 in G) & (f1 in G) & (f0 == f1)
	return tv


def is_identity(G):
	e = ide()
	tv = e in G
	for a in G:
		f0 = mul(e, a)
		tv = tv & (f0 == a)
	return tv


def is_inverse(G):
	e = ide()
	tv = True
	for a in G:
		f0 = mul(inv(a), a)
		tv = tv & (inv(a) in G) & (f0 == e)
	return tv


def is_commutation_law(G):
	tv = True
	for a in G:
		for b in G:
			tv = tv & mul(a, b) == mul(b, a)
	return tv


def is_group(G):
	e = ide()
	tv = e in G
	tv = tv & is_sociative_law(G) & is_identity(G) & is_inverse(G)
	return tv


def create_mod_n():
	G = set(range(N))
	return G


def mul_mod_n(a, b):
	c = (a + b) % N
	return c
	
	
def e_mod_n():
	return 0


def inv_mod_n(a):
	e = e_mod_n()
	H = range(N)
	for k in H:
		if (a + k) % N == e:
			break
	av = k
	return av


def create_mod_p():
	G = set(range(1, p))
	return G


def mul_Np(a, b):
	c = (a * b) % p
	return c


def e_Np():
	return 1


def inv_Np(a):
	e = e_Np()
	H = range(1, p)
	av = -1
	for k in H:
		if (a * k) % p == e:
			av = k
			break
	return av


def create_cyclic_group():
	G = set({})
	for k in range(N):
		G = G | {Cn ** k}
	return G


def index_cyc(c):
	a, n = 1, 0
	while a != c:
		a = a * Cn
		n += 1
	n = n % N
	return n


def mul_cyc(a, b):
	m = index_cyc(a)
	n = index_cyc(b)
	r = (m + n) % N
	c = Cn ** r
	return c


def e_cyc():
	return 1


def inv_cyc(a):
	n = index_cyc(a)
	m = (N - n) % N
	return Cn ** m


def create_permutation_group():
	G = {tuple(range(1, N + 1))}
	a = list(range(1, N + 1))
	k = N - 1
	while k != 0:
		if a[k - 1] < a[k]:
			j = N - 1
			while a[k - 1] > a[j]:
				j = j - 1
			a[k - 1], a[j] = a[j], a[k - 1]
			a[k:N] = sorted(a[k:N])
			G = G | {tuple(a)}
			k = N - 1
		else:
			k = k - 1
	return G


def mul_per(a, b):
	n = len(a)
	a = list(a)
	b = list(b)
	c = list(range(1, n + 1))
	for k in range(n):
		i = a[k]
		c[k] = b[i - 1]
	return tuple(c)


def e_per():
	return tuple(range(1, N + 1))


def inv_per(a):
	n = len(a)
	a = list(a)
	inv_a = list(range(1, N + 1))
	for k in range(n):
		i = a[k]
		inv_a[i - 1] = k + 1
	return tuple(inv_a)


def mul(a, b):
	# klein
	if SYSTEM == 1:
		c = mul_klein(a, b)
	# mod_n
	if SYSTEM == 2:
		c = mul_mod_n(a, b)
	# Np
	if SYSTEM == 3:
		c = mul_Np(a, b)
	# cyclic
	if SYSTEM == 4:
		c = mul_cyc(a, b)
	# permutation
	if SYSTEM == 5:
		c = mul_per(a, b)
	return c


def ide():
	# klein
	if SYSTEM == 1:
		c = e_klein()
	# mod_n
	if SYSTEM == 2:
		c = e_mod_n()
	# Np
	if SYSTEM == 3:
		c = e_Np()
	# cyclic
	if SYSTEM == 4:
		c = e_cyc()
	# permutation
	if SYSTEM == 5:
		c = e_per()
	return c


def inv(a):
	# klein
	if SYSTEM == 1:
		c = inv_klein(a)
	# mod_n
	if SYSTEM == 2:
		c = inv_mod_n(a)
	# Np
	if SYSTEM == 3:
		c = inv_Np(a)
	# cyclic
	if SYSTEM == 4:
		c = inv_cyc(a)
	# permutation
	if SYSTEM == 5:
		c = inv_per(a)
	return c


def power_n(a):
	e = ide()
	n = 1
	b = a
	while b != e:
		b = mul(b, a)
		n += 1
	return n


def mul_set(A, B):
	C = set({})
	for a in A:
		for b in B:
			C = C | {mul(a, b)}
	return C


def inv_set(A):
	A_v = set({})
	for a in A:
		A_v = A_v | {inv(a)}
	return A_v


def create_sub_group(a, b):
	e = ide()
	H = list([e, a, b])
	n = 0
	while n != len(H):
		n = len(H)
		for a in H:
			for b in H:
				c = mul(inv(a), b)
				if c not in H:
					H = H + [c]
	H = set(H)
	H = list(sorted(H))
	return H


def sub_group(G):
	H = set({})
	for a in G:
		for b in G:
			h = create_sub_group(a, b)
			h = sorted(h)
			H = H | {tuple(h)}
	return H


def is_sub_group(G, H):
	tv = (set(H) <= set(G)) & is_group(H)
	return tv