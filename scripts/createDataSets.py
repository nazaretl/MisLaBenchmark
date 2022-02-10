import pandas as pd
from sklearn import datasets

from utils import *
import subprocess
import random


names = ['Adult','DryBean','Chess','Magic','Bank','Iris']

df1 = pd.read_csv("dataRaw/adult.data",header = None)
df2 = pd.read_csv('dataRaw/DryBeanDataset/Dry_Bean_Dataset.arff',skiprows = 25
                 , header = None)
df3 = pd.read_csv('dataRaw/krkopt.data',skiprows = 0
                 , header = None)
df4 = pd.read_csv('dataRaw/magic04.data',skiprows = 0
                 , header = None)
df5 = pd.read_csv('dataRaw/bank/bank-full.csv',skiprows = 0, sep = ';')

iris = datasets.load_iris()
df6 = pd.DataFrame(iris.data)
df6['label'] = iris.target


dfs = [df1,df2,df3,df4,df5,df6]

for i, df in enumerate(dfs):
    df = df.rename(columns = {df.columns[-1]:'Label'})
   # print(df.head)
    df.to_csv('datasets/'+names[i]+'.csv.gz',sep = '\t', index = None, 
          header = True,compression = 'zip')
          



#for i in range(len(dfs)):
#    dfs[i] = dfs[i].rename(columns = {dfs[i].columns[-1]:'Label'})
#    dfs[i].to_csv('datasets/' + names[i] +'.csv.gz', sep = '\t', index = None, compression = 'gzip')


subprocess.run("python scripts/getData/createEncodeData.py 1", shell=True)
#subprocess.run("python scripts/getData/createRNAData.py 1", shell=True)
subprocess.run("python scripts/getData/createClinVarData.py 1", shell=True)

    