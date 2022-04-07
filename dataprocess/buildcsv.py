import sys
import os
import numpy as np
import pandas as pd
def build_all_csv(csv_dir):
    allapps = pd.DataFrame()
    fs = os.listdir(csv_dir)
    for f in fs:
        X1 = pd.read_csv(csv_dir+"/"+f,header=0,index_col=0)
        allapps = pd.concat([allapps, X1], axis=1)
    allapps = allapps.loc[:,~allapps.columns.duplicated(keep='first')]    
    allapps.to_csv(csv_dir+"/SKX_allapps.csv")

def build_csv(groupname,output,csv_dir):
    allapps = pd.DataFrame()
    for app in appnames:
        X = pd.DataFrame()
        for i,f in enumerate(files):
            if f.startswith(app+"_") and groupname in f:
                X1 = pd.read_csv(output+"/"+f,header=None, index_col = 0)
                X = X.append(X1)
        # drop the duplicated event name
        X = X[~X.index.duplicated(keep='first')]
        X = X.rename(columns={1: app})
        allapps = allapps.append(X.T)
    allapps.to_csv(csv_dir+"/SKX_"+groupname+".csv")

def build_memory_csv(output,csv_dir):
    allapps = pd.DataFrame()
    for app in appnames:
        X = pd.DataFrame()
        for i,f in enumerate(files):
            if f.startswith(app+"_") and "Memory" in f and "Memory_" not in f:
                X1 = pd.read_csv(output+"/"+f,header=None, index_col = 0)
                X = X.append(X1)
        # drop the duplicated event name
        X = X[~X.index.duplicated(keep='first')]
        X = X.rename(columns={1: app})
        allapps = allapps.append(X.T)
    allapps.to_csv(csv_dir+"/SKX_Memory.csv")


if __name__ == "__main__":
    appnames = ["ExaMiniMD", "LAMMPS", "sw4lite", "sw4", "SWFFT", "HACC", "MiniQMC", "QMCPack", "miniVite", "vite", "Nekbone", "Nek5000", "XSBench", "openmc", "picsarlite", "picsar", "amg2013", "Castro", "Laghos", "pennant", "snap", "hpcc_dgemm", "hpcc_random", "hpcc_streams", "hpcg"]
    groups = ["Branch","DecodeIssue_Pipeline","Dispatch_Pipeline","Execution_Pipeline",
    "Frontend","Instruction_Cache","Instruction_Mix","L1_D_Cache",
    "L2_D_Cache","L3_D_Cache","Memory_Pipeline","Misc","Power","Retirement_Pipeline"]
    args = sys.argv[1:]
    output = args[0]
    files = os.listdir(output)
    csv_dir = args[1]
    if not os.path.exists(csv_dir):
        #Create a new directory if not exist
        os.makedirs(csv_dir)
        print("The new directory "+csv_dir+" is created!")
    for group in groups:
        build_csv(group,output,csv_dir)
    build_memory_csv(output,csv_dir)
    build_all_csv(csv_dir)
