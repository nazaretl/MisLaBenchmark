import pandas as pd
import random
import numpy as np
import sys
sys.path.insert(0, 'scripts/')
from addNoiseScikit import *

def getData(dfAll,name, a, noise_level,size):
    N = min(len(dfAll), size)
    ind = random.sample(range(len(dfAll)), N)
    if name in ['ClinVarReal', 'Encode']:
        
        nErrors = int(noise_level*N)
        dfClean = dfAll[dfAll['LabelNew']==dfAll['LabelOld']]
        dfNoisy = dfAll[dfAll['LabelNew']!=dfAll['LabelOld']]
        indClean = random.sample(list(dfClean.index), N-nErrors)
        indNoisy = random.sample(list(dfNoisy.index), nErrors)
        ind = indClean + indNoisy
        df = dfAll.iloc[ind,:].reset_index(drop = True).sample(frac=1)

        X = df.iloc[:,:-2]
        y = df.iloc[:,-2].astype(int)
        noisyLabels = df.iloc[:,-1].astype(int)#.reset_index(drop = True)
        no = (y!=noisyLabels).sum()
       # print('Number of errors: ', no) 
    else:

        df = dfAll.iloc[ind,:].reset_index(drop = True)
        X = df.iloc[:,:-1]#.reset_index(drop = True)
        y = df.iloc[:,-1].astype(int)#.reset_index(drop = True)
        uniform, cc, bcn = addNoiseScikit(X, y, noise_level = noise_level)
        if a=='Sym':
            noisyLabels = pd.Series(uniform)
        else:
            noisyLabels = pd.Series(bcn)
            
    return X, y, noisyLabels



def getMeans(dfMeans, cvs, ID,r):
    n1 = cvs.shape[0]
    n2 = cvs.shape[1]
    dfMeans = dfMeans.to_numpy().reshape(r+1,n1,n2)
    dfMeans  = dfMeans.mean(axis = 0)
    
    dfMeans = pd.DataFrame(dfMeans)
    dfMeans.columns = cvs.columns +  ' '+str(ID)
   # dfMeans.index = cvs.index
    
    return dfMeans