import sys
import os
import numpy as np
import pandas as pd 

def average_5file(dirname,appname):
# get the mean of last 5 steps of 5 trials 
	files = os.listdir(dirname)

	X = pd.DataFrame()
	for i,f in enumerate(files):
	    if f.startswith(appname+"_"):
	        X1 = pd.read_csv(dirname+'/'+f,header = 0)
	        p = X1.iloc[-5:].mean(axis=0)
	        X = X.append(p,ignore_index=True)
	Y = X.mean(axis=0)
	Y.to_csv("output/"+appname+"_"+dirname+'.csv')
   
	return


if __name__ == "__main__":
    args = sys.argv[1:]
    average_5file(args[0],args[1])
