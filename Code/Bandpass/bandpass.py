import pickle
import os.path
import numpy as np
from numpy import median
from os import path

count = 0
root='/data/jvla'
dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
dirlist.remove('anaconda2')
dirlist.remove('plots')
dirlist.remove('analysis')
dirlist.remove('casa-release-5.3.0-143.el7')
dirlist.remove('report')
dirlist.remove('analysis_leakage')
dirlist.remove('analysis_tec')
dirlist = sorted(dirlist)
print(dirlist)
for fname in dirlist:
	DDID = []
	tb.open(fname+'/13B-266_'+fname+'.mms')
	DDID= np.unique(tb.getcol("DATA_DESC_ID"))
	tb.close()
	print(DDID)
	ANT_DICT = []
	tb.open(fname+"/13B-266_"+fname+".mms/ANTENNA") #this creates a dynamic list of every antenna involved in the current observation
	ANT_DICT = tb.getcol("NAME") #list contents will change for each measurement
					#e.g in the first measurement every antenna except ea07 could be used
					#but in the next one 
	tb.done()
	tb.open(fname+"/13B-266_"+fname+".B")
	SPW_LIST = np.unique(tb.getcol("SPECTRAL_WINDOW_ID")) #this creates a dynamic list of every SPW recorded for this observation
	tb.done()						#as with ANT_DICT, this lists contents will change 
	for SPW_NO in SPW_LIST: #For all the SPW numbers in SPW_LIST, the following will occur
				#this prevents the possibility of the code failing if an SPW wasn't recorded
			tb.open(fname+"/13B-266_"+fname+".B")
			for ANT_ID in ANT_DICT: #for each antenna that was included in the observation, the following will be done for each SPW
						#recorded in the observation
						#this means that the data for each antenna for each separate spw in a given observation will be
						#manipulated and normalized i.e. for a  given observation, each antenna's SPW0 will be normalised,
						#based on the values obtained for that specific antenna, then SPW1, 2 and 3
						#then the next observation will be considered, ANT_DICT and SPW_LIST will change to some extent
						#process repeats itself
				mydata= []
				CParam_L = []
				CParam_R = []
				subtb = tb.query('ANTENNA1=='+str(ANT_DICT.tolist().index(str(ANT_ID)))+'&&SPECTRAL_WINDOW_ID=='+str(SPW_NO))
				spw = subtb.getcol("SPECTRAL_WINDOW_ID") #Collate SpW data into 1 ar    	
				antenna = subtb.getcol("ANTENNA1") #Defines Antenna Index as Appropriate     				
				mydata = subtb.getcol("CPARAM") #Collate Cparameter data into array
				mydataflag=subtb.getcol("FLAG") #collate flagged data values
				print fname , ANT_ID , ANT_DICT
				CParam_L = abs(mydata[0,:]) #isolate left and right pols based on comparison of data with plot
				CParam_R = abs(mydata[1,:])
			
				count = count+1
				print(count)
				
				data_flag_left = np.array(mydataflag[0,:]) #separate flagged data for left and right pols
				data_flag_right = np.array(mydataflag[1,:])
				
				MED_LEFT_TEMP = []
				MED_RIGHT_TEMP = []
				#to determine the median across the central third accurately, create temporary array containing
				#values across the central third of the SPW that have not been flagged
				for i in range(20,42):
					if data_flag_left[i] == False:
						MED_LEFT_TEMP.append(CParam_L[i])
					if data_flag_right[i] == False:
						MED_RIGHT_TEMP.append(CParam_R[i])
				#find median across central third of the SPW neglecting any flagged data
				#this median is found for each antenna for each SPW considered in each observation		
				MED_LEFT_TEMP = np.asarray(MED_LEFT_TEMP)
				MED_LEFT = np.median(MED_LEFT_TEMP)
				MED_RIGHT = np.median(MED_RIGHT_TEMP)		
				print(MED_LEFT)		
				CParam_L_Norm = CParam_L/MED_LEFT 
    				CParam_R_Norm = CParam_R/MED_RIGHT
		
				name_left = 'analysis/'+str(ANT_ID)+'/SpW'+str(SPW_NO)+'/Left/'+fname+'.txt'
				np.savetxt(name_left, np.column_stack([CParam_L_Norm, data_flag_left]),  fmt='%.18e',delimiter=",")


				name_right = 'analysis/'+str(ANT_ID)+'/SpW'+str(SPW_NO)+'/Right/'+fname+'.txt'
				np.savetxt(name_right, np.column_stack([CParam_R_Norm, data_flag_right]), fmt='%.18e',delimiter=",")

			tb.done()
