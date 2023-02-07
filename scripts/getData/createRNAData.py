import pandas as pd
import sys
sys.path.insert(0, 'scripts/')

from utils import *
import numpy as np
import random 

test = sys.argv[1]


umap = pd.read_csv('dataProduced/rnaUMAP.csv.gz',sep = '\t', header = None,
                  compression = 'zip')
labels = pd.read_csv('dataRaw/atlas/meta.tab',sep = '\t',low_memory=False)


if test:
    classes = [12,16,15,9,13]
    labels = random.choices(classes, k  =len(umap))
    labels = pd.DataFrame(pd.Series(labels, name = 'cluster'))
else:
    labels = labels.iloc[ind,:]


ind = labels[~labels['cluster'].isna()].index
umap = umap.iloc[ind,:50]

umap.loc[:,'Label'] = labels['cluster']

foundGroups = [ [12, 16],[12, 15, 16], [12, 9, 13]]
for i,gr in enumerate(foundGroups):
    df = umap.loc[umap['Label'].isin(gr),:]
   # df = getProperLabels(df)
    a = df['Label'].unique()
    repl = dict(zip(a,list(range(len(a)))))
    df.loc[:,'Label'] = df.loc[:,'Label'].replace(repl).astype(int)
    df.to_csv('dataProduced/RNA'+str(i)+'.csv.gz',sep = '\t', index = False, compression = 'zip')
