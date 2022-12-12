import sys
import os
import numpy as np
import pandas as pd 

def average_5file(dirname,appname,output):
    # Get the mean of 5 run's std 
    files = os.listdir(dirname)

    X = pd.DataFrame()
    for i,f in enumerate(files):
        if f.startswith(appname+"_"):
            X1 = pd.read_csv(dirname+'/'+f,header = 0)
            p = X1.iloc[:].std(axis=0)
            X = pd.concat([X,pd.DataFrame([p])],axis=0,ignore_index=True)
    Y = X.mean(axis=0)
    Y.to_csv(output+"/"+appname+"_"+dirname[6:]+'.csv',header=False)
   
    return


if __name__ == "__main__":
    args = sys.argv[1:]
    output = args[2]
    if not os.path.exists(output):
        os.makedirs(output)
    average_5file(args[0],args[1],args[2])


