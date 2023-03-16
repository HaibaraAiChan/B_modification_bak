import os
import numpy as np
import pandas as pd
from statistics import mean
import argparse
import sys


def data_collect(filename):
	epoch_time =[]
	epoch_wo_REG_Block_gen_time = []
	epoch_wo_to_device_time = []
	epoch_pure_train_time = []
	epoch_load_block_feature_label_time = []
	epoch_block_to_device_time = []
	bucketing_time = []
	metis_partition_time = []
	REG_and_block_gen_time = []

	sort_mapp_time = []
	optimizing_time = 0
	gap = int(filename.split('_')[2][:-4]) +1
	avg_pure_train_time = 0
	with open(filename) as f:
		for line in f:
			line = line.strip()
			# if line.startswith("_buckting time") :
			# 	bucketing_time.append(float(line.split(' ')[-1]))
			if line.startswith("----------- core.py torch.sort() replace to OrderedDict time:"):
				sort_mapp_time.append(float(line.split(' ')[-1]))
			if line.startswith("avg pure train time:"):
				avg_pure_train_time = (float(line.split(' ')[-1]))
			if line.startswith("avg optimizing time") :
				optimizing_time = (float(line.split(' ')[-1]))
			# if line.startswith("Training time/epoch"):
			# 	epoch_wo_REG_Block_gen_time.append(float(line.split(' ')[-1]))
			# if line.startswith("Training time without block to device /epoch"):
			# 	epoch_wo_to_device_time.append(float(line.split(' ')[-1]))
			# if line.startswith("Training time without total dataloading part(pure training) /epoch "):
			# 	epoch_pure_train_time.append(float(line.split(' ')[-1]))
			# if line.startswith("load block tensor time/epoch"):
			# 	epoch_load_block_feature_label_time.append(float(line.split(' ')[-1]))
			# if line.startswith("block to device time/epoch"):
			# 	epoch_block_to_device_time.append(float(line.split(' ')[-1]))
		
			# if line.startswith("block dataloader generation time/epoch"):
			# 	REG_and_block_gen_time.append(float(line.split(' ')[-1]))
			# if line.startswith("Metis partitioning:"):
			# 	metis_partition_time.append(float(line.split(' ')[2]))
			
	# sort1,sort2,sort3=[],[],[]
	# gap = 3               ## gap = num_split + 1
	sorted_time = [[] for i in range(gap)]
	res = []
	for i in range(0, len(sort_mapp_time), (gap)):
		for j in range(gap):
			sorted_time[j].append(sort_mapp_time[i+j]) 
	for j in range(gap):
		res.append(mean(sorted_time[j]))
	total_sort = sum(res) 
	# print('split ',res)
	print('avg_pure_train_time:\t\t\t\t',avg_pure_train_time)
	print('total \t\t\t\t\t\t',total_sort)
	
	print('pure train w/o mapping & sort & preparing \t',avg_pure_train_time-total_sort + optimizing_time)

	# print('average bucketing time (each bucket) ',mean(bucketing_time))
	# print()
	# print('average pure train time per epoch ',mean(epoch_pure_train_time))
	# print()	
	# print('average features & labels loading time per epoch',mean(epoch_load_block_feature_label_time))
	# print('average block to device per epoch',mean(epoch_block_to_device_time))
	# print()
	# print('average  metis partition  per epoch',mean(metis_partition_time))
	# print()
	# print('average  REG + block gen per epoch',mean(REG_and_block_gen_time))
	# print()

	# print('average epoch time w/o REG + block gen',mean(epoch_wo_REG_Block_gen_time))
	# print()
	# print('average epoch time including REG + block gen',mean(epoch_time))




if __name__=='__main__':
	
	for filename in os.listdir('./'):
		if filename.endswith(".log"):
			file = os.path.join('./', filename)
			print(file)
			data_collect(file)
			print()
	
	
		





