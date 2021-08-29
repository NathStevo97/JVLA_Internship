import pickle
import os
import numpy as np
from numpy import median
from os import path

#Create ANTENNA LIST for reference
root = '/data/jvla/analysis_leakage'
ANT_LIST = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
ANT_LIST = sorted(ANT_LIST)
print(ANT_LIST)
SpW_List = ['SpW0', 'SpW1', 'SpW2', 'SpW3']
print(SpW_List)


for ANT_ID in ANT_LIST:
 #for each spw folder in ant_id folder
	for SpW_ID in SpW_List:
		print(SpW_ID)
		meas_list = sorted(os.listdir('/data/jvla/analysis_leakage/'+ANT_ID+'/'+SpW_ID+'/Left')) #measurement list dependent on each antenna
		med_left = [] #for each spw median, range and percentage deviations reset
		rng_left = []
		per_dev_left = []
		for i in range(0,64): #for each of the 64 channels per SpW the following will apply
			channel_left = [] #empty array for ith channel value to be added to from each measurement
			for fname in meas_list: 
				data_left = np.loadtxt('/data/jvla/analysis_leakage/'+ANT_ID+'/'+SpW_ID+'/Left/'+fname,delimiter=",", unpack=True)
				#for each measurement for the given antenna, load data
				bandpass_left = data_left[0,:]
				flag_left = data_left[1,:]
				print(fname, i, ANT_ID, SpW_ID)
				if flag_left[i] == 0.0: #as long as the data isn't flagged, add the amplitude to the array
					channel_left.append(bandpass_left[i])
				
			if len(channel_left)==0.:
				channel_left.append(0.)
				
		
			channel_left_med = np.median(channel_left) #find median value of channel considered
			med_left.append(channel_left_med) #add median value of channel i to array containing medians
			rng_channel_left = np.nanmax(channel_left) - np.nanmin(channel_left)
			rng_left.append(rng_channel_left)

			devtns_left = abs(((channel_left - channel_left_med)/channel_left_med)*100.)
			MAD_Left = np.median(devtns_left)

			per_dev_left.append(MAD_Left)
	
		med_array_left = np.asarray(med_left)
		rng_array_left = np.asarray(rng_left)
		per_dev_left_array = np.asarray(per_dev_left)
			
		savename_left = '/data/jvla/analysis_leakage/'+ANT_ID+'/'+SpW_ID+'_Left.txt'
		np.savetxt(savename_left, np.column_stack([med_array_left, rng_array_left, per_dev_left_array]),  fmt='%.18e',delimiter=",")
		
for ANT_ID in ANT_LIST:
 #for each spw folder in ant_id folder
	for SpW_ID in SpW_List:
		print(SpW_ID)
		meas_list = sorted(os.listdir('/data/jvla/analysis_leakage/'+ANT_ID+'/'+SpW_ID+'/Right')) #measurement list dependent on each antenna
		med_right = [] #for each spw median, range and percentage deviations reset
		rng_right = []
		per_dev_right = []
		for i in range(0,64): #for each of the 64 channels per SpW the following will apply
			channel_right = [] #empty array for ith channel value to be added to from each measurement
			for fname in meas_list: 
				data_right = np.loadtxt('/data/jvla/analysis_leakage/'+ANT_ID+'/'+SpW_ID+'/Right/'+fname,delimiter=",", unpack=True)
				#for each measurement for the given antenna, load data
				bandpass_right = data_right[0,:]
				flag_right = data_right[1,:]
				print(fname, i, ANT_ID, SpW_ID)
				if flag_right[i] == 0.0: #as long as the data isn't flagged, add the amplitude to the array
					channel_right.append(bandpass_right[i])
				
			if len(channel_right)==0.:
				channel_right.append(0.)	
		
			channel_right_med = np.median(channel_right) #find median value of channel considered
			med_right.append(channel_right_med) #add median value of channel i to array containing medians
			rng_channel_right = np.nanmax(channel_right) - np.nanmin(channel_right)
			rng_right.append(rng_channel_right)

			devtns_right = abs(((channel_right - channel_right_med)/channel_right_med)*100.)
			MAD_Right = np.median(devtns_right)

			per_dev_right.append(MAD_Right)
	
		med_array_right = np.asarray(med_right)
		rng_array_right = np.asarray(rng_right)
		per_dev_right_array = np.asarray(per_dev_right)
			
		savename_right = '/data/jvla/analysis_leakage/'+ANT_ID+'/'+SpW_ID+'_Right.txt'
		np.savetxt(savename_right, np.column_stack([med_array_right, rng_array_right, per_dev_right_array]),  fmt='%.18e',delimiter=",")
