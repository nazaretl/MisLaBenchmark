import pandas as pd
import sys 
sys.path.insert(0, 'scripts/')

from utils import *
names = ['Adult','DryBean','Chess','Magic','Iris',
              'ClinVarReal','CleanVarArt','Encode','RNA1','RNA2','RNA3']

names = ['Adult','DryBean','Chess','Magic','Iris','ClinVarReal','ClinVarArt','Encode']
nClasses = [2,6,9,2,3,3,3,2]

for i,name in enumerate(names):
    df = pd.read_csv('datasets/'+name+'.csv.gz', sep = '\t',compression='zip')
    n = nClasses[i]    

    nl=1
    if name in ['ClinVarReal', 'Encode']:
        nl=2
        

    df = getProperLabels(df,nl)
    df = decreaseClassNumber(df,n)
    df = getProperLabels(df,nl) #need this twice

    data = df[df.columns[~df.columns.str.contains('Label',na=False)]]
    labels = df[df.columns[df.columns.str.contains('Label',na=False)]]
    data = pd.get_dummies(data)
    data = data.join(labels)
    #data = balance(data)
    data = data.fillna(0)
    print(data.shape)
    print(data.iloc[:,-1].value_counts())
    #data = data.sample(n=min(len(data),10000))
    data.to_csv('datasets/'+name+'.csv.gz',sep = '\t', index = None, 
             compression = 'zip')
