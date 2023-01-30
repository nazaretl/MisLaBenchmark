import pandas as pd
import sys 
sys.path.insert(0, 'scripts/')
from utils import *

# fill nas with 0
# convert classes to 0,1,2 etc. (somethimes strings or 10,20 etc)
# get dummies for categorical data
# label column os last column and is named Label (or LabelOld, LabelNew for ClinVar)
# can decrease the number of classes or balance the data (NOT DONE)


names = ['Adult','DryBean','Chess','Magic','ClinVarReal','ClinVarArt','RNA0','RNA1','RNA2', 'HEPMASS','Pokerhand', 'IFD']

for i,name in enumerate(names):
    print(name)
    df = pd.read_csv('dataProduced/'+name+'.csv.gz', sep = '\t',compression='zip')
    # n is the numbre of classes
    n = len(df.iloc[:,-1].value_counts())
    
    # nl is the number of labels
    nl=1
    if name in ['ClinVarReal']:
        nl=2
    else:
        df = df.rename(columns = {df.columns[-1]:'Label'})

        

    df = getProperLabels(df,nl)
   # df = decreaseClassNumber(df,n) 
   # df = getProperLabels(df,nl) #need this twice when decreasing the number of classes

    data = df[df.columns[~df.columns.str.contains('Label',na=False)]]
    labels = df[df.columns[df.columns.str.contains('Label',na=False)]]
    data = pd.get_dummies(data)
    data = data.join(labels)
    #data = balance(data)
    data = data.fillna(0)
    print(name, data.shape)
    print(data.iloc[:,-1].value_counts())
 #   data.to_csv('datasets/'+name+'.csv.gz',sep = '\t', index = None, 
  #           compression = 'zip')
    data = data.sample(n=min(len(data),10000))
    data.to_csv('datasetsSample/'+name+'.csv.gz',sep = '\t', index = None, 
             compression = 'zip')

