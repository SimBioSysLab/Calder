#11/4/2021
# use the previous value to fill the negative delta, remove inst_retired events
# update the special case:MINIQMC and QMCQMCPack only 8 ranks on one node 
# and directory Power donot have instruction related events
# delete the biggest value in 32 ranks and then average
import sys
import numpy as np
import pandas as pd 


def delta_event_from_file(filename, savefile):
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

    X_delta = X.copy()
    #12 calculate delta start from the first events as well as the cpu cycle
    X_delta.iloc[:, 12:] = X_delta.iloc[:, 12:].diff().shift(-1)
    # we need to delete the last two rows of each node, last row is none, and the second last is strange
    for id in X['component_id'].unique():
        index = X_delta.index[X_delta['component_id'] == id][-2:] 
        X_delta.drop(index, axis=0, inplace=True)

    # remove the ZERO CPU CYCLE
    before_lenth=X_delta.shape[0]
    X_delta = X_delta[( X_delta.iloc[:, 12:12+rank] != 0).all(1)]  #12+32, 32 columns is cpu cycles
    after_lenth=X_delta.shape[0]
    print(filename +" delete cpu cyle=0 rate: {:.2f}".format((before_lenth-after_lenth)/before_lenth))

    # normalize by cpu cycle 
    for e in event:
        for i in range(rank):
            X_delta[e+str(i)] = X_delta[e+str(i)].div(X_delta['CPU_CLK_THREAD_UNHALTED:THREAD_P'+str(i)], axis=0)
    
    # remove the negative    
    X_delta[( X_delta.iloc[:, 12:] < 0)]=np.nan
    X_delta = X_delta.replace([np.inf, -np.inf], np.nan)
    X_delta.fillna( method = 'pad', inplace = True) 
  
    # average of 32 process on one rank,delete the biggest values (spike)
    for e in event:
        section = X_delta[[e+str(i) for i in range(rank)]]
        X_delta[e]= (section.sum(axis=1)-section.max(axis=1))/(rank-1)

    data_delta= pd.DataFrame(columns=event)
    for e in event: 
        p = pd.DataFrame()
        for id in X_delta['component_id'].unique():
            q = X_delta[X_delta["component_id"]==id][e].reset_index(drop=True)
            p = pd.concat((p,q ),axis=1)
        data_delta[e] = p.mean(axis=1)
        
    # data_delta is the final events/cpu cycle
    data_delta.to_csv(savefile,index=False)
    return 


if __name__ == "__main__":
    args = sys.argv[1:]
    delta_event_from_file(args[0],args[1])
