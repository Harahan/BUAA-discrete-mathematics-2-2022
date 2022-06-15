import re
import time

from big_homework.arithmetic import johnson, floyd
from big_homework.util import Graph

if __name__ == '__main__':
	data, data_list, gr = open('data2.txt', 'r'), [], Graph()  # data1.txt, data2.txt, data3.txt
	pattern = re.compile(r'u: (-?\d+), v: (-?\d+), w: (-?\d+)')
	for line in data:
		matcher = pattern.match(line)
		if matcher is None:
			print("Data Error!!!")
			exit(0)
		data_list.append([int(matcher.group(1)), int(matcher.group(2)), int(matcher.group(3))])
	for d in data_list:
		gr.add(d[0], d[1], d[2])
	t1 = time.time()
	dict_johnson = johnson(gr)
	t2 = time.time()
	if dict_johnson is None:
		print("There's negative cost loop in input data!!!")
		exit(0)
	dict_floyd = floyd(gr)
	t3 = time.time()
	johnson, floyd = open('johnson.txt', 'w'), open('floyd.txt', 'w')
	
	# jonson
	johnson.write('Johnson uses : ' + str(t2 - t1) + 's' + '\n')
	for i in dict_johnson.keys():
		dict_i: dict = dict_johnson[i]
		for j in dict_i.keys():
			johnson.write('u: ' + str(i) + ', v: ' + str(j) + ', min path: ' + str(dict_i[j]) + '\n')
			
	# floyd
	floyd.write('Floyd uses : ' + str(t3 - t2) + 's' + '\n')
	for i in dict_floyd.keys():
		dict_i: dict = dict_floyd[i]
		for j in dict_i.keys():
			floyd.write('u: ' + str(i) + ', v: ' + str(j) + ', min path: ' + str(dict_i[j]) + '\n')
			