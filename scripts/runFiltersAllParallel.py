import sys
import numpy as np
import random
import pandas as pd
import warnings 
from time import time
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import traceback


warnings.filterwarnings('ignore')
sys.path.insert(0, 'scripts/')

from runRFilter import *
from cleanLabFilter import CleanLab
from filtersScikiClean import filtersScikiClean
from utils import *
from addNoiseScikit import *


path = str(snakemake.output)
#path = 'temp/Encode_0.1_100_Asym_KDN_Python.tmp'
#st = 'temp/Magic_0.1_100_Asym_edgeBoostFilter_R.tmp'
st  = path.split('/')[1].split('.tmp')[0].split('_')
name = st[0]
noiseLevel = float(st[1])
datasetSize = int(st[2])
noiseType = st[3]
model = st[4]
imp = st[5]

repeats = int(snakemake.params.repeats)

df = pd.read_csv('datasets/' + name + '.csv.gz', sep = '\t',compression='zip',
                index_col=None)

ID = [name, model, noiseLevel, noiseType,datasetSize]

dfMeansCV = pd.DataFrame()
try:
    for r in range(repeats):

        ID = [name, model, noiseLevel, noiseType,datasetSize,r]

        X, y, noisyLabels = getData(df,name, noiseType, noiseLevel, datasetSize)

        noiseInd = y[y!=noisyLabels].index

        dR = pd.DataFrame(np.vstack([X.T, noisyLabels.tolist()]).T)

        t0 = time()
        if imp=='Python':
            filteredNoiseInd = filtersScikiClean(X,y,noisyLabels, t = 0.5,n = noiseLevel, model = [model])
        if imp=='CleanLab':
            filteredNoiseInd  = CleanLab(X,y,noisyLabels)
        if imp=='R':
            filteredNoiseInd = getRModel(dR, y, noisyLabels,model = [model])
        
     #   print(filteredNoiseInd)
        cv, scores = confusionMatrixScikit(y,noiseInd, filteredNoiseInd)
        cv.index = [model]
        scores.index = [model]

        t1 = time()
        totalTime = t1-t0
        cv['Execution Time'] = totalTime
        
        temp = pd.DataFrame([len(y), noiseInd.to_list(), filteredNoiseInd.to_list(),t1],
                 index = ['N', 'NoiseInd', 'FoundNoiseInd','Time']).T
        temp.index=[model]
        cv = cv.join(scores).join(temp)
        cv.index = [str(ID)]

       # print(totalTime)
        dfMeansCV = dfMeansCV.append(cv)

    
except Exception as e: 
    print('CAUGHT AN ERROR IN ', str(ID))
    print(e)
    log = traceback.format_exc()
    #log   = ''.join(traceback.format_tb(e.__traceback__))

    pd.Series(log).to_csv('logs/'+str(ID)+'.log', sep = '\t',header = False)
    dfMeansCV = pd.DataFrame()
    dfMeansCV[str(ID)] = ['failed']

    
dfMeansCV.iloc[:,:9].to_csv('output/'+name+'_'+imp+'.csv', sep = '\t',header = False, mode='a')
dfMeansCV.iloc[:,:9].to_csv(path, sep = '\t',header = False)

dfMeansCV.to_csv('output/'+name+'_'+imp+'_Extended.csv', sep = '\t',header = False, mode='a')
dfMeansCV.to_csv(path+'Extended', sep = '\t',header = False)

#cvsMean.T.to_csv('temp/'+name+'.csv', sep = '\t')
