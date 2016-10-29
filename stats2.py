#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 23:06:22 2016

@author: dan
"""
from os import path

def sigma_clip_chunk(big_arr):

	chunk_start=np.arange(0,big_arr.shape[0],200)
	chunk_end=chunk_start+200
	if chunk_end[-1] > big_arr.shape[0]:
		chunk_end[-1] = big_arr.shape[0]
	result_mean = np.ma.array(np.zeros_like(big_arr[:,:,0]))
	result_dev = np.ma.array(np.zeros_like(big_arr[:,:,0]))
	result_med = np.ma.array(np.zeros_like(big_arr[:,:,0]))
	for j in range(len(chunk_start)):
		print('chunk ',j+1, 'of ',len(chunk_start))
		tmp_dat = big_arr[chunk_start[j]:chunk_end[j],:,:]
		clip_sig = 2*tmp_dat.std(axis=2)
		clip_mean = tmp_dat.mean(axis=2)
		np.clip(tmp_dat, clip_mean - clip_sig, clip_mean + clip_sig, out=tmp_dat)
		result[chunk_start[j]:chunk_end[j]] = stats.sigma_clipped_stats(tmp_dat,axis=2,iters=2)
	return result_mean, result_med, result_dev

r_arr=np.fromfunction(lambda x, y: (x % 2 == 0) & (y % 2 == 0), (3476, 5208))
g1_arr=np.fromfunction(lambda x, y: (x % 2 == 0) & (y % 2 == 1),(3476, 5208))
g2_arr=np.fromfunction(lambda x, y: (x % 2 == 1) & (y % 2 == 0),(3476, 5208))
b_arr=np.fromfunction(lambda x, y: (x % 2 == 1) & (y % 2 == 1), (3476, 5208))


bias_list = list(filter(lambda x: x.exptime < 0.1, darklist))
bias1600_list = list(filter(lambda x: x.exptime < 1 and x.ISO==1600,darklist))
bias1_list= list(filter(lambda x: x.exptime == 0.07692307692307693, bias_list))
#bias1 = build_data(bias1_list)
#bias1a= stats.sigma_clip(bias1,sig=3.0,iters=1,axis=2,copy=False)
#bias1a=stats.sigma_clip(bias1)

#bias1_avg = bias1a.mean(axis=2)

#bias1600=build_data(bias1600_list)
#bias1600_med=stats.sigma_clip(sigma_clip_chunk(bias1600), iters=2)

#bias1600a=stats.sigma_clip(bias1600,axis=2)

#bias1600_avg=bias1600a.mean()

#not_hot = (np.sum(bias1a.mask, axis=2) == 0)

sub2 = list(filter(lambda x: x.ISO == 1600 and int(x.exptime)==120 and x.temp>18,sub_EOSM))

#dark2=build_data(sub2)

#clip one exposure heavily to make a good pixel mask (auto-joined w/bias1600 mask)
#dark_clip=stats.sigma_clip(dark2[:,:,0]-np.int16(bias1600_med),sig=2,iters=4)

#resulting mask about half of the pixels. maybe should base on more than one exp?
#mask2=np.bitwise_not(dark_clip.mask)

#dev1 = bias1a.std(axis=2)
temp_arr=[]
exp_arr=[]
ISO_arr=[]
std_arr=[]


#(dark2[:,:,4]-np.int16(dark2[:,:,5])).std()

for dark in sub_EOSM:
	exp_arr.append(dark.exptime)
	temp_arr.append(dark.temp)
	ISO_arr.append(dark.ISO)
	
#	tmp_dat = get_data(dark)
#	dark_std = stats.sigma_clip((tmp_dat-np.int16(bias1600_avg))[mask2]).std()
#	std_arr.append(dark_std)
#	print(path.basename(dark.filename),':',dark.temp,'C', dark_std)
