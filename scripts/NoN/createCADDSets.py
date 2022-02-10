import pandas as pd
import sys
import numpy as np
sys.path.insert(0, 'scripts/')
import random
import os
from filtersScikiClean import filtersScikiNoClean

file = 'datasets/sampleCADD.csv.gz'
#z = ! zcat $file | wc -l
z = 28022592
Z = list(range(z))
N = 120000
#skiprows = set(Z) - set(random.sample(Z, N)) - set([0])
df_raw = pd.read_csv(file, sep = '\t',
                  #   nrows = 1000
                     #skiprows = skiprows
                    )
#df_raw = pd.read_csv('datasets/CADD.csv.gz', sep = '\t', nrows = N)


df = df_raw.drop(columns = ['Pos'])
o = df.dtypes[2]

cols = df.dtypes[~df.dtypes.isin([o])].index
df = df[cols]
df = df.fillna(0)
X = df.iloc[:,:-1].to_numpy()
y = df.iloc[:,-1].to_numpy()

print(df.shape)

#df_raw = df_raw.drop(columns = ['Unnamed: 0'])
model = str(snakemake.wildcards.model)

#names = [st.split('/')[1].split('_')[0]]

FF = [model]
print(FF)

names, targetLabelsList = filtersScikiNoClean(X,y,FF)
for i in range(len(names)):
    name = names[i]
    print(name)    
    d = pd.DataFrame(targetLabelsList[i])
    print(len(d))
    d.columns = ['LabelNew']
    d.to_csv('data/GRCh38/NewLabels/sampleCADD'+name+'_labels.csv', index = None)

'''
    df_raw = df_raw[df_raw['Conscore']>0.5]
    df_raw = df_raw.drop(columns = 'Conscore')
    sim = df_raw[df_raw['Label']==1]
    hum = df_raw[df_raw['Label']==0]
    sim = sim.drop(columns = ['Label'])
    hum = hum.drop(columns = ['Label'])
    print(len(sim), len(hum))

   

    file1 = 'mkdir -p data/GRCh38/'+name+'_simulation/annotation'
    file2 = 'mkdir -p data/GRCh38/'+name+'_humanDerived/annotation'
    
    os.system(file1)
    os.system(file2)



    sim.to_csv('data/GRCh38/'+name+'_simulation/annotation/SNV.anno.tsv.gz',sep ='\t', 
                           index = False, compression = 'zip' )
    hum.to_csv('data/GRCh38/'+name+'_humanDerived/annotation/SNV.anno.tsv.gz',sep ='\t', 
                           index = False, compression = 'zip' )


'''