import sys
import numpy as np
sys.path.insert(0, 'scripts/')
import random
import pandas as pd
from filtersScikiClean import filtersScikiClean
from utils import confusionMatrixScikit
from utilsFilters import *
from addNoiseScikit import *
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from runRFiltersAll import *

from addNoise import Noise
from CleanLabFilter import CleanLab

import warnings 
warnings.filterwarnings('ignore')

#names = ['Iris','ClinVarArt', 'ClinVarReal', 'RNA0', 'RNA1', 'RNA2', 'Encode']
#names = ['Iris','Magic','ClinVarArt', 'ClinVarReal', 'RNA0', 'RNA1', 'RNA2', 'Encode', 'sampleCADD']
#st = str(snakemake.output)
st = 'Magic'
noiseType = ['Sym']

#names = [st.split('/')[1].split('_')[0]]

names = ['Magic']
noiseLevels = list(np.around(np.linspace(0.05, 0.7, num=14), decimals=2))
datasetSizes = [100,200,300,500,1000,2000,3000,5000,10000]
repeats = 5
#noiseType = ['Asym']

#noiseType = ['Asym']
#noiseLevels = [0.5]
#datasetSizes = [500]
#names = ['Magic']
#repeats = 1

dfs = []
for name in names:
    df = pd.read_csv('datasets/' + name + '.csv.gz', sep = '\t')
    dfs.append(df)
    print(len(df))
    

i = 0
IDs = []
#allCVS = pd.DataFrame()
allScores = pd.DataFrame()
for dfAll in dfs:    
    name = names[i]
    datasetScores = pd.DataFrame()
    for noise_level in noiseLevels:
        for a in noiseType:                        
            for size in datasetSizes:
                repeats = repeats

                dfMeansCV = pd.DataFrame()
                dfMeansScores = pd.DataFrame()
                ID = [name, noise_level, a,size]
                IDs.append(ID)
                print(ID)
                for r in range(repeats):

                    X, y, noisyLabels = getData(dfAll,name, a, noise_level, size)
                    dR = pd.DataFrame(np.vstack([X.T, noisyLabels.tolist()]).T)

                    cvs = pd.DataFrame()
                    scores = pd.DataFrame()

                    cvP, scoresP = filtersScikiClean(X,y,noisyLabels, t = 0.5,n = noise_level)
                    cvC, scoresC  = CleanLab(X,y,noisyLabels)
                    cvR, scoresR = getAllRModels(dR, y, noisyLabels)

                    cvs = cvs.append(cvP)
                    cvs = cvs.append(cvC)
                    cvs = cvs.append(cvR)
                    scores = scores.append(scoresP)                
                    scores = scores.append(scoresC)
                    scores = scores.append(scoresR)
                    dfMeansCV = dfMeansCV.append(cvs)
                    dfMeansScores = dfMeansScores.append(scores)

               #     display(cvs)
                #    display(scores)
                cvsMean = getMeans(dfMeansCV, cvs, ID,r)
                scoresMean = getMeans(dfMeansScores, scores, ID,r)
               # allCVS = pd.concat([allCVS,cvsMean], axis = 1)
               # allScores = pd.concat([allScores,scoresMean], axis = 1)
                datasetScores = pd.concat([datasetScores,cvsMean], axis = 1) 
                datasetScores = pd.concat([datasetScores,scoresMean], axis = 1) 

    allScores = pd.concat([allScores,datasetScores], axis = 1)        
    datasetScores.to_csv('output/' + name + '_Sym_Scores.csv', sep = '\t')
    i += 1
    #print('----------------------------------------------------------')

    
allScores.to_csv('output/allScores.csv', sep = '\t')
