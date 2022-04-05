# no delta, but only remove the negative increasing with linear interpolate with hardware events and cpu cycle
# use the previous value to fill the negative delta, remove inst_retired events
# update the special case:MINIQMC and QMCQMCPack only 8 ranks on one node 
# and directory Power donot have instruction related events
# delete the biggest value in 32 ranks and then average
import sys
import numpy as np
import pandas as pd 


def clean_event_from_file(filename, savefile):
    if "QMC" in filename:
        rank=8
    else:
        rank=32

    Xp = pd.read_csv(filename,header = 0)
    #sort each node (4 nodes in each file) by time
    X = Xp.sort_values(['component_id','#Time'])
    X.reset_index(drop=True,inplace=True)

    # get the hardware events in the file
    event = [col[:-2] for col in X.columns if (col.endswith('63')and not col.endswith('_63'))]
    event.remove('Pid')
    X.drop([column for column in X.columns if column.startswith("Pid")],axis = 1, inplace=True)

    event.remove('CPU_CLK_THREAD_UNHALTED:THREAD_P')
    # only two groups Instruction_Cache and Instruction_Mix need the inst_retired events
    # directory Power donot have instruction related events
    if "Instruction" not in filename and "Power" not in filename:
        event.remove('INST_RETIRED:ANY_P')
        event.remove('INST_RETIRED:ALL')
        X.drop([column for column in X.columns if column.startswith("INST_RETIRED")],axis = 1, inplace=True)

    X_clean = X.copy()
    #12 calculate delta start from the first events as well as the cpu cycle
 
    # we need to delete the last row of each node because it's strange
    for id in X['component_id'].unique():
        index = X_clean.index[X_clean['component_id'] == id][-1:] 
        X_clean.drop(index, axis=0, inplace=True)

    # remove the ZERO CPU CYCLE
    before_lenth=X_clean.shape[0]
    #12+32, 32 columns is cpu cycles
    X_clean[X_clean.iloc[:, 12:12+rank]==X_clean.iloc[:, 12:12+rank].shift(+1)]=np.nan
    X_clean=X_clean.dropna(axis=0,how='any')

    after_lenth=X_clean.shape[0]
    print(filename +" delete cpu cyle=0 rate: {:.2f}".format((before_lenth-after_lenth)/before_lenth))

    # remove the smaller value with the linear interpolate value   
    X_clean[( X_clean.iloc[:, 12:] <  X_clean.iloc[:, 12:].shift(+1))]=np.nan
    X_clean = X_clean.replace([np.inf, -np.inf], np.nan)
    X_clean.iloc[:, 12:]=X_clean.iloc[:, 12:].interpolate( method = 'linear')

    # normalize by cpu cycle 
    for e in event:
        for i in range(rank):
            X_clean[e+str(i)] = X_clean[e+str(i)].div(X_clean['CPU_CLK_THREAD_UNHALTED:THREAD_P'+str(i)], axis=0)
  
    # average of 32 process on one rank,delete the biggest values (spike)
    for e in event:
        section = X_clean[[e+str(i) for i in range(rank)]]
        X_clean[e]= (section.sum(axis=1)-section.max(axis=1))/(rank-1)


    data_clean= pd.DataFrame(columns=event)
    for e in event: 
        p = pd.DataFrame()
        for id in X_clean['component_id'].unique():
            q = X_clean[X_clean["component_id"]==id][e].reset_index(drop=True)
            p = pd.concat((p,q ),axis=1)
        data_clean[e] = p.mean(axis=1)
        
    # data_delta is the final events/cpu cycle
    data_clean.to_csv(savefile,index=False)

    return 


if __name__ == "__main__":
    args = sys.argv[1:]
    clean_event_from_file(args[0],args[1])
