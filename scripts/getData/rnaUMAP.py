import umap.umap_ as umap
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from scipy.sparse import csc_matrix

file = 'dataRaw/atlas/raw_counts.mtx'
df = pd.read_csv(file,sep = ' ', skiprows = 2, header = None, 
               #  nrows = 2000000, 
                 dtype = {0: 'int16', 1: 'int32', 2: 'int16'})


row = df[1].to_numpy()
col = df[0].to_numpy()
data = df[2].to_numpy()
d = pd.DataFrame(csc_matrix((data, (row, col))).toarray())
d[0].sum()

d = d[1:]


n_components = d.shape[0]
n_components = 50


reducer = umap.UMAP(n_components = n_components)
scaled_data = StandardScaler().fit_transform(d.values)
embedding = reducer.fit_transform(scaled_data)
pd.DataFrame(embedding).to_csv('dataProduced/rnaUMAP.csv.gz',sep = '\t', index = None, 
                               header = None, compression = 'zip')