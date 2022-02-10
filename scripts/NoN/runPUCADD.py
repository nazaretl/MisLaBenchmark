import pandas as pd
import random 
import numpy as np
import sys
sys.path.insert(0, 'scripts/')
from runPU import runPU
import os


dfRaw = pd.read_csv('datasets/sampleCADD.csv', sep = '\t')

dtypes = dfRaw.dtypes.replace('object','category')#.to_dict()
dtypes = dtypes.replace({'int64':'int32', 'float64': 'float32'}).to_dict()


df = dfRaw.drop(columns = ['Pos'])
o = df.dtypes[2] # object or category
cols = df.dtypes[~df.dtypes.isin([o])].index
df = df[cols]
df = df.fillna(0)
X = df.iloc[:,:-1].to_numpy()
y = df.iloc[:,-1].to_numpy()

All = snakemake.params.All
if All:
    dfAll = pd.read_csv('datasets/CADD.csv.gz', sep = '\t', dtype = dtypes)
    name = 'PUAll'
    targetLabels = runPU(X,y,dfAll[cols].iloc[:,:-1].fillna(0))
else:
    name = 'PUSample'
    targetLabels = runPU(X,y,dfRaw[cols].iloc[:,:-1].fillna(0))

d = pd.DataFrame(targetLabels)
print(d.sum())
d.columns = ['LabelNew']
d.to_csv('data/GRCh38/NewLabels/'+name+'_labels.csv', index = None)
