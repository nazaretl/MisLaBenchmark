import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support

import random
import numpy as np
import sys
sys.path.insert(0, 'scripts/')
from addNoiseScikit import *


def decreaseClassNumber(df,n):
    ind = df.iloc[:,-1].value_counts()[0:n].index
    df = df[df.iloc[:,-1].isin(ind)]
    return df

def getProperLabels(df,nl=1):         
    a = df.iloc[:,-1].unique()
    repl = dict(zip(a,list(range(len(a)))))
    df.iloc[:,-nl:] = df.iloc[:,-nl:].replace(repl).astype(int)
    return df

def balance(df):
    n = len(df.columns)-1
    values = df.iloc[:,n].value_counts()
    sampleSize = values.min()
    df = df.groupby(df.iloc[:,n]).sample(n=sampleSize, random_state=1).sample(frac=1)
    return df

def confusionMatrixScikit(y,noiseInd,filteredNoiseInd):
    # 'True Negative', 'False Positive', 'False Negative', 'True Positive'
    y_true = y.copy()
    y_true[y.index.isin(noiseInd)]=1
    y_true[~y.index.isin(noiseInd)]=0
    y_pred = y.copy()
    y_pred[y.index.isin(filteredNoiseInd)]=1
    y_pred[~y.index.isin(filteredNoiseInd)]=0
    if y_pred.sum()==0 & y_true.sum()==0:
        li = [np.nan,np.nan,np.nan,np.nan]
    else:
        li = confusion_matrix(y_true, y_pred ).ravel()
        
    [precision, recall, fscore, support] = precision_recall_fscore_support(y_true, y_pred, average='binary')
   
    cv = pd.DataFrame(li).T
    if len(cv.columns)==4:
        cv.columns = ['True Negative', 'False Positive', 'False Negative', 'True Positive'] 
        cv = cv[['True Positive', 'False Positive', 'True Negative', 'False Negative']]
    else:
        print('Something went wrong when calculating the confusion matrix')
        
    # deleted support since always None
    scores = pd.DataFrame([precision, recall, fscore]).T
    if len(scores.columns)==3:
        scores.columns = ['Precision', 'Recall', 'F-score'] 
    else:
        print('Something went wrong when calculating the scores')
       
    return cv, scores

def getData(dfAll,name, a, noise_level,size):
    N = min(len(dfAll), size)
    ind = random.sample(range(len(dfAll)), N)
    if name in ['ClinVarReal', 'Encode']:
        
        nErrors = int(noise_level*N)
        dfClean = dfAll[dfAll['LabelNew']==dfAll['LabelOld']]
        dfNoisy = dfAll[dfAll['LabelNew']!=dfAll['LabelOld']]
        indClean = random.sample(list(dfClean.index), N-nErrors) # random.choice for replacement
        indNoisy = random.sample(list(dfNoisy.index), nErrors)   # random.choice
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
            
    X = X[X.columns[X.nunique() > 1]]     #delete columns w/o variability    
            
    return X, y, noisyLabels



def getMeans(dfMeans, cvs, ID,r):
    n1 = cvs.shape[0]
    n2 = cvs.shape[1]
    dfMeans = dfMeans.to_numpy().reshape(r+1,n1,n2)
    dfMeans  = dfMeans.mean(axis = 0)
    #dfMeans  = np.nanmean(dfMeans, axis = 0)
    dfMeans = pd.DataFrame(dfMeans)
    dfMeans.columns = cvs.columns +  ' '+str(ID)
   # dfMeans.index = cvs.index
    
    return dfMeans