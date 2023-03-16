import os
import numpy as np
import pandas as pd
from statistics import mean
import argparse
import sys


def data_collect(filename):
	reduce_time =[]
	sort_time = []
	
	gap = int(filename.split('+')[1][:-4]) +1

	with open(filename) as f:
		for line in f:
			line = line.strip()
			if line.startswith("invoke_udf_reduce time:") :
				reduce_time.append(float(line.split(' ')[-1]))
			if line.startswith("----------- core.py torch.sort() replace to OrderedDict time:") :
				sort_time.append(float(line.split(' ')[-1]))
			
	# print(len(reduce_time))
	reduce_time = reduce_time[gap*3:]
	sort_time = sort_time[gap*3:]
	# print(len(reduce_time))
	tmp, res = [],[]
	for i in range(len(reduce_time)):
		tmp.append(reduce_time[i]-sort_time[i])
	for j in range(0,len(tmp), gap):
		temp = sum(tmp[j:j+gap])
		res.append(temp)
	# print(len(res))
	print('average reduce runction  ', mean(res))
	print()	
	



if __name__=='__main__':
	
	for filename in os.listdir('./'):
		if filename.endswith(".log"):
			file = os.path.join('./', filename)
			print(file)
			data_collect(file)
			print()
	
	
		





