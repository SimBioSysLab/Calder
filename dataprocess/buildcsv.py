import sys
import os
import numpy as np
import pandas as pd
def build_all_csv():
    allapps = pd.DataFrame()
    files = os.listdir("./csv")
    for f in files:
        X1 = pd.read_csv("./csv/"+f,header=0,index_col=0)
        allapps = pd.concat([allapps, X1], axis=1)
    allapps = allapps.loc[:,~allapps.columns.duplicated(keep='first')]    
    allapps.to_csv("./csv/SKX_allapps.csv")

def build_csv(groupname):
    allapps = pd.DataFrame()
    for app in appnames:
        X = pd.DataFrame()
        for i,f in enumerate(files):
            if f.startswith(app+"_") and groupname in f:
                X1 = pd.read_csv("./output/"+f,header=None, index_col = 0)
                X = X.append(X1)
        # drop the duplicated event name
        X = X[~X.index.duplicated(keep='first')]
        X = X.rename(columns={1: app})
        allapps = allapps.append(X.T)
    allapps.to_csv("./csv/SKX_"+groupname+".csv")

def build_memory_csv():
    allapps = pd.DataFrame()
    for app in appnames:
        X = pd.DataFrame()
        for i,f in enumerate(files):
            if f.startswith(app+"_") and "Memory" in f and "Memory_" not in f:
                X1 = pd.read_csv("./output/"+f,header=None, index_col = 0)
                X = X.append(X1)
        # drop the duplicated event name
        X = X[~X.index.duplicated(keep='first')]
        X = X.rename(columns={1: app})
        allapps = allapps.append(X.T)
    allapps.to_csv("./csv/SKX_Memory.csv")


if __name__ == "__main__":
    files = os.listdir("./output")
    appnames = ["ExaMiniMD", "LAMMPS", "sw4lite", "sw4", "SWFFT", "HACC", "MiniQMC", "QMCPack", "miniVite", "vite", "Nekbone", "Nek5000", "XSBench", "openmc", "picsarlite", "picsar", "amg2013", "Castro", "Laghos", "pennant", "snap", "hpcc_dgemm", "hpcc_random", "hpcc_streams", "hpcg"]
    groups = ["Branch","DecodeIssue_Pipeline","Dispatch_Pipeline","Execution_Pipeline",
    "Frontend","Instruction_Cache","Instruction_Mix","L1_D_Cache",
    "L2_D_Cache","L3_D_Cache","Memory_Pipeline","Misc","Power","Retirement_Pipeline"]
    for group in groups:
        build_csv(group)
    build_memory_csv()
    build_all_csv()
