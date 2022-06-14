import os
import random

from big_homework.arithmetic import johnson, floyd
from big_homework.util import Graph


def data_generate(n: int, m: int):
	nodes, gm = [_ for _ in range(1, n + 1)], []
	for t in range(m):
		gm.append('u: ' + str(random.choice(nodes)) + ', v: ' + str(random.choice(nodes)) + ', w: ' +
				  str(random.choice([random.randint(-5, 0), random.randint(10, 100)])) + '\n')
	return gm


if __name__ == '__main__':
	jf = open("johnson.txt", "w")
	ff = open("floyd.txt", "w")
	while True:
		data = open("data.txt", 'w')
		mg = data_generate(200, 5000)
		for i in mg:
			data.write(i)
		mg = Graph()
		data.close()
		data = open('data.txt', 'r')
		for i in data:
			j = i.split(' ')
			mg.add(int(j[1].split(',')[0]), int(j[3].split(',')[0]), int(j[5].split(',')[0]))
		if johnson(mg) is None:
			print("negative cost loop exist!!!")
			continue
		jf.write(str(johnson(mg)))
		ff.write(str(floyd(mg)))
		os.system("fc jf.txt ff.txt")
		break
