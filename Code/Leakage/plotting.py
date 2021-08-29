import numpy as np
import matplotlib.pyplot as plt
import os
from os import path
channel_indx_no = []
channel_indx = []
for i in range(0,4):
	for j in range(0,64):
		channel_indx.append(j)

for i in range(0,256):
	channel_indx_no.append(i)
	
channel_dict = np.column_stack([channel_indx_no, channel_indx])
channel_indx_no = np.asarray(channel_indx_no)
print(channel_dict)

root = '/data/jvla/analysis_leakage'
ANT_LIST = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
ANT_LIST = sorted(ANT_LIST)
for ANT_ID in ANT_LIST:
	
	SPW0_Left = np.loadtxt("/data/jvla/analysis_leakage/"+ANT_ID+"/SpW0_Left.txt", delimiter=",", unpack=True)
	SPW1_Left = np.loadtxt("/data/jvla/analysis_leakage/"+ANT_ID+"/SpW1_Left.txt", delimiter=",", unpack=True)
	SPW2_Left = np.loadtxt("/data/jvla/analysis_leakage/"+ANT_ID+"/SpW2_Left.txt", delimiter=",", unpack=True)
	SPW3_Left = np.loadtxt("/data/jvla/analysis_leakage/"+ANT_ID+"/SpW3_Left.txt", delimiter=",", unpack=True)

	SPW0_Right = np.loadtxt("/data/jvla/analysis_leakage/"+ANT_ID+"/SpW0_Right.txt", delimiter=",", unpack=True)
	SPW1_Right = np.loadtxt("/data/jvla/analysis_leakage/"+ANT_ID+"/SpW1_Right.txt", delimiter=",", unpack=True)
	SPW2_Right = np.loadtxt("/data/jvla/analysis_leakage/"+ANT_ID+"/SpW2_Right.txt", delimiter=",", unpack=True)
	SPW3_Right = np.loadtxt("/data/jvla/analysis_leakage/"+ANT_ID+"/SpW3_Right.txt", delimiter=",", unpack=True)


	#Plot both Polarizations for All SPWs together
	plt.errorbar(channel_indx_no[0:64], SPW0_Left[0,:], yerr=SPW0_Left[1,:], label='SpW0 Left')
	plt.errorbar(channel_indx_no[0:64], SPW0_Right[0,:], yerr=SPW0_Right[1,:], label='SpW0 Right')
	plt.errorbar(channel_indx_no[64:128], SPW1_Left[0,:], yerr=SPW1_Left[1,:], label='SpW1 Left')
	plt.errorbar(channel_indx_no[64:128], SPW1_Left[0,:], yerr=SPW1_Left[1,:], label='SpW1 Right')
	plt.errorbar(channel_indx_no[128:192], SPW2_Left[0,:], yerr=SPW2_Left[1,:], label='SpW2 Left')
	plt.errorbar(channel_indx_no[128:192], SPW2_Right[0,:], yerr=SPW2_Right[1,:], label='SpW2 Right')
	plt.errorbar(channel_indx_no[192:256], SPW3_Left[0,:], yerr=SPW3_Left[1,:], label='SpW3 Left')
	plt.errorbar(channel_indx_no[192:256], SPW3_Left[0,:], yerr=SPW3_Left[1,:], label='SpW3 Right')
	
	plt.xlim(xmax=270)
	plt.axes().set_aspect('auto')
	plt.xlabel('Channel Index')
	plt.ylabel(r'Median Percentage Absolute deviation for the normalized amplitude (Jy) per channel')
	plt.title('Variation in median percentage')
	manager = plt.get_current_fig_manager()
	manager.resize(*manager.window.maxsize())

	plt.savefig('/data/jvla/plots/Leakage/'+ANT_ID+'_All_Pols.png', bbox_inches='tight')

	plt.clf()

	#plot left polarization for all spws
	plt.errorbar(channel_indx_no[0:64], SPW0_Left[0,:], yerr=SPW0_Left[1,:], label='SpW0')
	plt.errorbar(channel_indx_no[64:128], SPW1_Left[0,:], yerr=SPW1_Left[1,:], label='SpW1')
	plt.errorbar(channel_indx_no[128:192], SPW2_Left[0,:], yerr=SPW2_Left[1,:], label='SpW2')
	plt.errorbar(channel_indx_no[192:256], SPW3_Left[0,:], yerr=SPW3_Left[1,:], label='SpW3')
	
	plt.xlim(xmax=270)
	plt.axes().set_aspect('auto')
	plt.xlabel('Channel Index')
	plt.ylabel('Average Normalised Amplitude (Jy)')
	plt.title('Variation in Normalised Amplitude with Channel Number across all Observations (Left Polarization)')
	manager = plt.get_current_fig_manager()
	manager.resize(*manager.window.maxsize())

	plt.savefig('/data/jvla/plots/Leakage/'+ANT_ID+'_Left.png', bbox_inches='tight')

	plt.clf()
	#plot all spws for right polarization
	plt.errorbar(channel_indx_no[0:64], SPW0_Right[0,:], yerr=SPW0_Right[1,:], label='SpW0')
	plt.errorbar(channel_indx_no[64:128], SPW1_Right[0,:], yerr=SPW1_Right[1,:], label='SpW1')
	plt.errorbar(channel_indx_no[128:192], SPW2_Right[0,:], yerr=SPW2_Right[1,:], label='SpW2')
	plt.errorbar(channel_indx_no[192:256], SPW3_Right[0,:], yerr=SPW3_Right[1,:], label='SpW3')
	
	plt.xlim(xmax=270)
	plt.axes().set_aspect('auto')
	plt.xlabel('Channel Index')
	plt.ylabel('Average Normalised Amplitude (Jy)')
	plt.title('Variation in Normalised Amplitude with Channel Number across all Observations (Right Polarization)')
	manager = plt.get_current_fig_manager()
	manager.resize(*manager.window.maxsize())

	plt.savefig('/data/jvla/plots/Leakage/'+ANT_ID+'_Right', bbox_inches='tight')
	plt.clf()
	opacity = 0.8
	w = 1.0
	Left_SPWS = []
	Right_SPWS = []
	Left = []
	Right = []
	for i in range(0,64):
		Left_SPWS.append(SPW0_Left[2,i])
	for i in range(0,64):
		Left_SPWS.append(SPW1_Left[2,i])
	for i in range(0,64):
		Left_SPWS.append(SPW2_Left[2,i])
	for i in range(0,64):
		Left_SPWS.append(SPW3_Left[2,i])

	for i in range(0,64):
		Right_SPWS.append(SPW0_Right[2,i])
	for i in range(0,64):
		Right_SPWS.append(SPW1_Right[2,i])
	for i in range(0,64):
		Right_SPWS.append(SPW2_Right[2,i])
	for i in range(0,64):
		Right_SPWS.append(SPW3_Right[2,i])		

	#plot all spws median absolute percentage deviation per channel for all time
	
	plt.bar(channel_indx_no[0:64], Left_SPWS[0:64], width=w, color='red', label='SPW0: Left')
	plt.bar(channel_indx_no[0:64], Right_SPWS[0:64], width=w, color='blue', bottom=Left_SPWS[0:64], label='SPW0: Right')
	plt.bar(channel_indx_no[64:128], Left_SPWS[64:128], width=w, color='yellow', label='SPW1: Left')
	plt.bar(channel_indx_no[64:128], Right_SPWS[64:128], width=w, color='green', bottom=Left_SPWS[64:128], label='SPW1: Right')
	plt.bar(channel_indx_no[128:192], Left_SPWS[128:192], width=w, color='purple', label='SPW2: Left')
	plt.bar(channel_indx_no[128:192], Right_SPWS[128:192], width=w, color='cyan', bottom=Left_SPWS[128:192], label='SPW2: Right')
	plt.bar(channel_indx_no[192:256], Left_SPWS[192:256], width=w, color='black', label='SPW3: Left')
	plt.bar(channel_indx_no[192:256], Right_SPWS[192:256], width=w, color='orange', bottom=Left_SPWS[192:256], label='SPW3: Right')
	
	plt.axes().set_aspect('auto')
	plt.xlim(xmin=0)
	plt.xlim(xmax=260)
	plt.xlabel('Channel Index')
	plt.ylabel('Median Absolute Deviation per Channel for all time')
	plt.title('Variation in Median Absolute Deviation per Channel for all time')
	manager = plt.get_current_fig_manager()
	manager.resize(*manager.window.maxsize())

	plt.savefig('/data/jvla/plots/Leakage/'+ANT_ID+'_Percentage_Deviation_Comparison')
	plt.clf()
