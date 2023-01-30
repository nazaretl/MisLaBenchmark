import pandas as pd
import sys 
sys.path.insert(0, 'scripts/')
from utils import *
import subprocess


# Some of the dataProduced need preprocessing 

# HEPMASS
df= pd.read_csv('dataRaw/all_test.csv.gz')
to_save = df.iloc[:,1:]
to_save['Label'] = df['# label']
# same only a sample of 100 000 p
print(to_save['Label'].value_counts())

to_save.sample(n = 100000).to_csv('dataProduced/HEPMASS.csv.gz', sep = '\t',
                                  index = None, compression = 'zip' )   
                
# PokerHand                
df= pd.read_csv('dataRaw/poker-hand-training-true.data', header = None)
print(df.shape)

df['Label'] = 0
# label is 1 if something in hand, othterwise 0
df.loc[df[10]!=0,'Label'] = 1
df = df.drop(columns = [10])
df.to_csv('dataProduced/Pokerhand.csv.gz', sep = '\t',
                                  index = None, compression = 'zip' )

# IFD      
df= pd.read_csv('dataRaw/log2.csv')
print(df.shape)

to_repl = {'allow':0, 'drop':1, 'deny':2, 'reset-both':3}
df['Label'] = df['Action'].replace(to_repl)
df = df.drop(columns = 'Action')
# delete one class since the frequency is almost zero
df = df[df['Label']!=3]
df.to_csv('dataProduced/IFD.csv.gz', sep = '\t',
                                  index = None, compression = 'zip' )
      
      
# Chess
df = pd.read_csv('dataRaw/krkopt.data', header = None)
n = 9
df = decreaseClassNumber(df,n)
df.to_csv('dataProduced/Chess.csv.gz', sep = '\t',
                                  index = None, compression = 'zip' )
      
      
# Drybean
df = pd.read_csv('dataRaw/DryBeanDataset/Dry_Bean_Dataset.arff',skiprows = 25
                 , header = None)
df.to_csv('dataProduced/DryBean.csv.gz', sep = '\t',
                                  index = None, compression = 'zip' )
      
# Adult
df = pd.read_csv('dataRaw/adult.data',header = None)
df.to_csv('dataProduced/Adult.csv.gz', sep = '\t',
                                  index = None, compression = 'zip' )      

# Magic
df = pd.read_csv('dataRaw/magic04.data',skiprows = 0
                 , header = None)
df.to_csv('dataProduced/Magic.csv.gz', sep = '\t',
                                       index = None, compression = 'zip' )

subprocess.run("python scripts/getData/createRNAData.py 1", shell=True)
subprocess.run("python scripts/getData/createClinVarData.py 1", shell=True)
