import sys
import numpy as np
import random
import pandas as pd
import warnings 
from time import time
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import traceback
from sklearn.preprocessing import StandardScaler


warnings.filterwarnings('ignore')
sys.path.insert(0, 'scripts/')

from runRFilter import *
from cleanLabFilter import CleanLab
from filtersScikiClean import filtersScikiClean
from utils import *
from addNoiseScikit import *
from DNNwERLLoss import DNNwERLLoss
from AEFilter import AEFilter

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
beta = float(snakemake.params.beta)
plusLayers =  int(snakemake.params.plusLayers)
learningRate = float(snakemake.params.learningRate)
scaling = eval(snakemake.params.scaling)
loss = snakemake.params.loss
selection = snakemake.params.selection

#selection = True

di = {'Real' : 2, 'Sym':1, 'Asym' :1}

df = pd.read_csv('datasets/' + name + '.csv.gz', sep = '\t',compression='zip',
                index_col=None)

df = df.fillna(0)
df = df[[i for i in df if df[i].nunique()>1]]

if scaling:
    scaler = StandardScaler()        
    n = 2 if name in ['ClinVarReal', 'ClinVarRealPCA'] else 1
    scaler = scaler.fit(df.iloc[:,:-n])

ID = [name, model, noiseLevel, noiseType,datasetSize]

dfMeansCV = pd.DataFrame()
try:
    for r in range(repeats):
        
        status = 'F' # F:Failure S: Success N: No noise found
        ExtraInfo = {}
        ID = [name, model, noiseLevel, noiseType,datasetSize,r]
        X, y, noisyLabels = getData(df,name, noiseType, noiseLevel, datasetSize)
        
        X = pd.DataFrame(scaler.transform(X))
        X = X[X.columns[X.nunique() > 1]] # delete rows w/o variability
        
        noiseInd = y[y!=noisyLabels].index
        dR = pd.DataFrame(np.vstack([X.T, noisyLabels.tolist()]).T)
        t0 = time()
        
        if imp=='Python':
            foundNoiseInd = filtersScikiClean(X,y,noisyLabels, t = 0.5,n = noiseLevel, model = [model])
        if imp=='CleanLab':
            foundNoiseInd = CleanLab(X,y,noisyLabels)
        if imp=='R':
            foundNoiseInd = getRModel(dR, y, noisyLabels,model = [model])
        if model=='ERL':
            foundNoiseInd, metrics = DNNwERLLoss(X,y,noisyLabels,beta,plusLayers,learningRate, loss)
            ExtraInfo.update({'beta' :beta, 'plusLayers' :plusLayers, 'learningRate' : learningRate, 'scaling' : scaling,
                              'loss' : loss, 
                            #  'metrics' : metrics
                             })
            
        if model=='AE':
            foundNoiseInd, cms = AEFilter(X,y,noisyLabels)
          #  ExtraInfo = 'cms:{}'.format(cms)
            
        t1 = time()

        cv, scores = confusionMatrixScikit(y,noiseInd, foundNoiseInd)
        
        if len(foundNoiseInd)==0:
            status = 'N'
        else:
            status = 'S'
            
        if selection:
            ExtraInfo.update({'SmallSample':True})

        
        
        cv.index = [model]
        scores.index = [model]
        cv.insert(0,'Status',status)

        totalTime = t1-t0
        cv['Execution Time'] = totalTime
        
        temp = pd.DataFrame([str(ExtraInfo),str(noiseInd.to_list()), str(foundNoiseInd.to_list()),t1],
                 index = ['ExtraInfo','NoiseInd', 'FoundNoiseInd','Time']).T
        temp.index=[model]
        cv = cv.join(scores).join(temp)
        cv.index = [str(ID)]

        dfMeansCV = dfMeansCV.append(cv)
        dfMeansCV = dfMeansCV.round(4)
    
except Exception as e: 
    print('CAUGHT AN ERROR IN ', str(ID))
    print(e)
    log = traceback.format_exc()

    pd.Series(log).to_csv('logs/'+str(ID)+'.log', sep = '\t',header = False)
    cv = pd.DataFrame([np.nan]*13).T
    cv.insert(0,'Status',status)
    cv.index = [str(ID)]
    dfMeansCV = dfMeansCV.append(cv)

    

    
dfMeansCV.iloc[:,:10].to_csv('output/'+name+'_'+imp+'.csv', sep = '\t',header = False, mode='a')
dfMeansCV.iloc[:,:10].to_csv(path, sep = '\t',header = False)

dfMeansCV.to_csv('output/'+name+'_'+imp+'_Extended.csv', sep = '\t',header = False, mode='a')
#dfMeansCV.to_csv(path+'Extended', sep = '\t',header = False)

