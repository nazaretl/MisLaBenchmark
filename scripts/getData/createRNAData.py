import pandas as pd
import sys
sys.path.insert(0, 'scripts/')

from utils import *
import numpy as np

umap = pd.read_csv('rnaUMAP.csv',sep = '\t', header = None)
labels = pd.read_csv('dataRaw/RNA-seq/atlas/meta.tab',sep = '\t',low_memory=False)

ind = labels[~labels['cluster'].isna()].index
umap = umap.iloc[ind,:50]
labels = labels.iloc[ind,:]
umap.loc[:,'Label'] = labels['cluster']

foundGroups = [ [12, 16],[12, 15, 16], [12, 9, 13]]
for i,gr in enumerate(foundGroups):
    df = umap.loc[umap['Label'].isin(gr),:]
   # df = getProperLabels(df)
    a = df['Label'].unique()
    repl = dict(zip(a,list(range(len(a)))))
    df.loc[:,'Label'] = df.loc[:,'Label'].replace(repl).astype(int)
    df.to_csv('datasets/RNA'+str(i)+'.csv.gz',sep = '\t', index = False, compression = 'gzip')
