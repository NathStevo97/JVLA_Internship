import os
import numpy as np
import matplotlib.pyplot as plt
from os import path
from matplotlib import cm
from numpy import empty
import datetime
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from mpl_toolkits.axes_grid1 import make_axes_locatable
root = '/data/jvla/analysis_tec/Leakage'
root1 = '/data/jvla'
#Create alphabetical list of all antennae to be considered
ANT_LIST = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
ANT_LIST = sorted(ANT_LIST)
print(ANT_LIST)
timedata = np.loadtxt('/data/jvla/MT.txt', delimiter=",", unpack=True)
time_years = timedata[1,:]
time_years = np.asarray(time_years)

#create list of all observation times
meas_list_complete = [ item for item in os.listdir(root1) if os.path.isdir(os.path.join(root1, item))]
meas_list_complete.remove('anaconda2')
meas_list_complete.remove('plots')
meas_list_complete.remove('analysis')
meas_list_complete.remove('casa-release-5.3.0-143.el7')
meas_list_complete.remove('report')
meas_list_complete.remove('analysis_leakage')
meas_list_complete.remove('analysis_tec')
meas_list_complete = sorted(meas_list_complete)
print(meas_list_complete)

#initialise 28x256 array for each antenna's measurements
#these arrays are merely reference arrays to compute the percentage differences
antenna_meds_left = np.zeros((28,256))
antenna_meds_right = np.zeros((28,256)) 

ANT_ID = "ea24"
for ANT_ID in ANT_LIST:
	#import SPW Data for given antenna
	#Left Poln
	SPW0_Left = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW0_Left.txt", delimiter=",", unpack=True)
	SPW1_Left = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW1_Left.txt", delimiter=",", unpack=True)
	SPW2_Left = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW2_Left.txt", delimiter=",", unpack=True)
	SPW3_Left = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW3_Left.txt", delimiter=",", unpack=True)
	#Right Poln
	SPW0_Right = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW0_Right.txt", delimiter=",", unpack=True)
	SPW1_Right = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW1_Right.txt", delimiter=",", unpack=True)
	SPW2_Right = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW2_Right.txt", delimiter=",", unpack=True)
	SPW3_Right = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW3_Right.txt", delimiter=",", unpack=True)

	#Create two separate arrays to store median values per channel for all time
	#these values will then be appended to the big arrays defined previously
	Left_SPWS = []
	Right_SPWS = []
	#Left
	for i in range(0,64):
		Left_SPWS.append(SPW0_Left[0,i])
	for i in range(0,64):
		Left_SPWS.append(SPW1_Left[0,i])
	for i in range(0,64):
		Left_SPWS.append(SPW2_Left[0,i])
	for i in range(0,64):
		Left_SPWS.append(SPW3_Left[0,i])
	#Right
	for i in range(0,64):
		Right_SPWS.append(SPW0_Right[0,i])
	for i in range(0,64):
		Right_SPWS.append(SPW1_Right[0,i])
	for i in range(0,64):
		Right_SPWS.append(SPW2_Right[0,i])
	for i in range(0,64):
		Right_SPWS.append(SPW3_Right[0,i])
	
	#From Left and Right SPWS arrays, add to large array for row corresponding antenna
	for i in range(0,256):
		antenna_meds_left[ANT_LIST.index(str(ANT_ID)),i] = Left_SPWS[i]
		antenna_meds_right[ANT_LIST.index(str(ANT_ID)),i] = Right_SPWS[i]
	
#from here now need to initialise a 28/181 array for left and right polarisations
#the values in the array correspond to the average of the percentage deviation per channel from each channels median
#for a given observation
Final_Array = np.zeros((28,181))



fname = meas_list_complete[0]
for fname in meas_list_complete:
	filename = fname+'.txt'
	for ANT_ID in ANT_LIST:
		norm_data_left = []
		norm_data_left_flag = []
		perdevs_left = []
		perdevs_right = []
#create list of directories for corresponding antenna and SPWS
#done so to check in case an SPW wasn't recorded
		root0_left="/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW0/Left"
		root1_left="/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW1/Left"
		root2_left="/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW2/Left"
		root3_left="/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW3/Left"

		meas_list0_left = sorted([ item for item in os.listdir(root0_left)])
		meas_list1_left = sorted([ item for item in os.listdir(root1_left)])
		meas_list2_left = sorted([ item for item in os.listdir(root2_left)])
		meas_list3_left = sorted([ item for item in os.listdir(root3_left)])
	
		if filename in meas_list0_left: #repeat this one for each spw for both polarizations
			norm_data0_left = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW0/Left/"+fname+".txt", delimiter=",", unpack=True)
			for i in range(0,64):
				if norm_data0_left[1,i] == 0.0: #if the ith value in the first column indicates the data isn't flagged do the calculation
					perdevs_left.append(((norm_data0_left[0,i] - antenna_meds_left[ANT_LIST.index(str(ANT_ID)),i])/antenna_meds_left[ANT_LIST.index(str(ANT_ID)),i])*100.)
			
			
		if filename in meas_list1_left:
			norm_data1_left = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW1/Left/"+fname+".txt", delimiter=",", unpack=True)
			for i in range(64,128):
				if norm_data1_left[1,i-64] == 0.0: #if the ith value in the first column indicates the data isn't flagged do the calculation
					perdevs_left.append(((norm_data1_left[0,i-64] - antenna_meds_left[ANT_LIST.index(str(ANT_ID)),i])/antenna_meds_left[ANT_LIST.index(str(ANT_ID)),i])*100.)
	
		if filename in meas_list2_left:
			norm_data2_left = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW2/Left/"+fname+".txt", delimiter=",", unpack=True)
			for i in range(128,192):
				if norm_data2_left[1,i-128] == 0.0: #if the ith value in the first column indicates the data isn't flagged do the calculation
					perdevs_left.append(((norm_data2_left[0,i-128] - antenna_meds_left[ANT_LIST.index(str(ANT_ID)),i])/antenna_meds_left[ANT_LIST.index(str(ANT_ID)),i])*100.)		
	
		if filename in meas_list3_left:
			norm_data3_left = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW3/Left/"+fname+".txt", delimiter=",", unpack=True)
			for i in range(192,256):
				if norm_data3_left[1,i-192] == 0.0: #if the ith value in the first column indicates the data isn't flagged do the calculation
					perdevs_left.append(((norm_data3_left[0,i-192] - antenna_meds_left[ANT_LIST.index(str(ANT_ID)),i])/antenna_meds_left[ANT_LIST.index(str(ANT_ID)),i])*100.)
				
		perdevs_left_avg = np.nanmean(perdevs_left)

#repeating above for right polarisation

#create list of directories for corresponding antenna and SPWS
#done so to check in case an SPW wasn't recorded
		root0_right="/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW0/Right"
		root1_right="/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW1/Right"
		root2_right="/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW2/Right"
		root3_right="/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW3/Right"

		meas_list0_right = [ item for item in os.listdir(root0_right)]
		meas_list1_right = [ item for item in os.listdir(root1_right)]
		meas_list2_right = [ item for item in os.listdir(root2_right)]
		meas_list3_right = [ item for item in os.listdir(root3_right)]

		if filename in meas_list0_right: #repeat this one for each spw for both polarizations
			norm_data0_right = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW0/Right/"+fname+".txt", delimiter=",", unpack=True)
			for i in range(0,64):
				if norm_data0_right[1,i] == 0.0: #if the ith value in the first column indicates the data isn't flagged do the calculation
					perdevs_right.append(((norm_data0_right[0,i] - antenna_meds_right[ANT_LIST.index(str(ANT_ID)),i])/antenna_meds_right[ANT_LIST.index(str(ANT_ID)),i])*100.)
			
			
		if filename in meas_list1_right:
			norm_data1_right = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW1/Right/"+fname+".txt", delimiter=",", unpack=True)
			for i in range(64,128):
				if norm_data1_right[1,i-64] == 0.0: #if the ith value in the first column indicates the data isn't flagged do the calculation
					perdevs_right.append(((norm_data1_right[0,i-64] - antenna_meds_right[ANT_LIST.index(str(ANT_ID)),i])/antenna_meds_right[ANT_LIST.index(str(ANT_ID)),i])*100.)
	
		if filename in meas_list2_right:
			norm_data2_right = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW2/Right/"+fname+".txt", delimiter=",", unpack=True)
			for i in range(128,192):
				if norm_data2_right[1,i-128] == 0.0: #if the ith value in the first column indicates the data isn't flagged do the calculation
					perdevs_right.append(((norm_data2_right[0,i-128] - antenna_meds_right[ANT_LIST.index(str(ANT_ID)),i])/antenna_meds_right[ANT_LIST.index(str(ANT_ID)),i])*100.)		
	
		if filename in meas_list3_right:
			norm_data3_right = np.loadtxt("/data/jvla/analysis_tec/Leakage/"+ANT_ID+"/SpW3/Right/"+fname+".txt", delimiter=",", unpack=True)
			for i in range(192,256):
				if norm_data3_right[1,i-192] == 0.0: #if the ith value in the first column indicates the data isn't flagged do the calculation
					perdevs_right.append(((norm_data3_right[0,i-192] - antenna_meds_right[ANT_LIST.index(str(ANT_ID)),i])/antenna_meds_right[ANT_LIST.index(str(ANT_ID)),i])*100.)
				
		perdevs_right_avg = np.nanmean(perdevs_right)

		Final_Array[ANT_LIST.index(str(ANT_ID)), meas_list_complete.index(str(fname))] = np.nanmean([perdevs_left_avg, perdevs_right_avg])
		
		
#create colour plot
f = plt.figure()
ax = f.add_subplot(111)
cax = ax.imshow(Final_Array,interpolation='nearest', cmap=cm.coolwarm, vmin=-100., vmax = 100. )
cbar = f.colorbar(cax)
cbar.set_label('Average Percentage Deviation from Median \n Amplitude per Channel per Polarization per observation')
ax.set_yticks(np.arange(0,28))
ax.set_yticklabels(ANT_LIST)
ax.set_xticks([0.,45., 84., 133., 180.])
ax.set_xticklabels(['25/10/2013', '25/02/2015', '19/05/2016', '11/11/2017', '29/01/2018'])
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
f.autofmt_xdate()
plt.ylabel('Antenna ID')
plt.xlabel('Date')
for tick in ax.get_xticklabels():
	tick.set_rotation(15)
ax.set_aspect('auto')
manager = plt.get_current_fig_manager()
manager.resize(*manager.window.maxsize())

plt.savefig('/data/jvla/plots/Leakage_tec/Masterplot.png')
