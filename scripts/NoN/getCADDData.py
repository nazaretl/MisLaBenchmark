import pandas as pd
import sys
import numpy as np
sys.path.insert(0, 'scripts/')
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from cleanlab.classification import LearningWithNoisyLabels
from sklearn.linear_model import LogisticRegression
exit

file1 = '/fast/groups/ag_kircher/CADD/projects/bStatistic/data/GRCh38/simulation/annotation/SNV.anno.tsv.gz'
file2 = '/fast/groups/ag_kircher/CADD/projects/bStatistic/data/GRCh38/humanDerived/annotation/SNV.anno.tsv.gz'


N = 100000
sim = pd.read_csv(file1, sep = '\t', nrows = N)

dtypes = sim.dtypes.replace('object','category')#.to_dict()
dtypes = dtypes.replace({'int64':'int32', 'float64': 'float32'}).to_dict()

N = 700000000

sim = pd.read_csv(file1, sep = '\t',
                  nrows = N, 
                  dtype = dtypes
                 )
hum = pd.read_csv(file2, sep = '\t', 
                  nrows = N, 
                  dtype = dtypes
                 )

sim['Label'] = 1
hum['Label'] = 0

df = hum.append(sim)#.sample(frac = 1)
#df = pd.get_dummies(df)
#cols = df.dtypes[~df.dtypes.isin(['category','object'].index
                                 
print(df.shape)
print('Size of data:', sys.getsizeof(df)/1024**3)

#df = df[cols]
#df = df.fillna(0)

#column_to_move = df.pop('Label')
#df.insert(len(df.columns), 'Label', column_to_move)

#scaler = preprocessing.StandardScaler().fit(df)
#df = pd.DataFrame(scaler.transform(df))
#df.iloc[:,-1] = df.iloc[:,-1].replace({-1:0})#.replace({2:1})
#df.iloc[:,-1]  = df.iloc[:,-1].astype(int)
df.to_csv('datasets/CADD.csv',sep = '\t')             

#df = df.to_numpy()                                 
#np.savez_compressed('datasets/CADD', df)                
#display(df.head())
'''
X = df.iloc[:,:-1].to_numpy()
y = df.iloc[:,-1].to_numpy()


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.7)

pu_class = 0
# Should be 0 or 1. Label of class with NO ERRORS. (e.g., P class in PU)
lnl = LearningWithNoisyLabels(clf=LogisticRegression(max_iter = 500), pulearning=pu_class)
lnl.fit(X=X_train, s=y_train)
predicted_test_labels = lnl.predict(df.iloc[:,:-1])
#predicted_test_labels = lnl.predict(X_test)
#len(predicted_test_labels[predicted_test_labels!=y_test])/len(y_test)
a = len(predicted_test_labels[predicted_test_labels!=y])/len(y)
print('Fraction of identified mislabellings:', a)

N = len(hum)
sim['Label'] = predicted_test_labels[:N]
hum['Label'] = predicted_test_labels[N:]
#!mkdir -p '../data/GRCh38/PU/annotation'
sim.append(hum).to_csv('data/GRCh38/PU/annotation/SNV.anno.tsv.gz',sep ='\t', 
                       index = False, compression = 'zip' )
'''
