import pandas as pd
import numpy as np
from skclean.simulate_noise import flip_labels_uniform
from skclean.simulate_noise import flip_labels_cc # Class Conditional Noise:
from skclean.simulate_noise import UniformNoise
from skclean.simulate_noise import CCNoise
from skclean.simulate_noise import BCNoise
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def getNoiseCount(labels,noisyLabels):    
    ind = labels[labels!=noisyLabels].index
    d = pd.DataFrame([labels,noisyLabels]).T
    d  =d.iloc[ind,:]
    d = (d.iloc[:,0].astype(str)+'-'+d.iloc[:,1].astype(str))
    return d

def correctTM(lcm, N, noiseLevel):
    s = 0
    n = N*noiseLevel

    lcmNew = np.zeros(lcm.shape)
    for i in range(len(lcm)):
        for j in range(len(lcm)):
            if i!=j:
                z = lcm[i,j]
                s+=z 
              #  print(z)
    for i in range(len(lcm)):
        for j in range(len(lcm)):
            if i!=j:
                z = lcm[i,j]
                zz = (z/s)*n
             #   print(zz)
                lcmNew[i,j]=zz
    for i in range(len(lcm)):
            lcmNew[i,i] = (lcm[i,:]*N).sum() -lcmNew[i,:].sum()
 #   print(lcmNew)
    return lcmNew
'''
def getTransitionMatrix(data, labels, max_iter = 500, model = None, normalize = True, noiseLevel = 0.2):
   
    if model is None:
        model = LinearDiscriminantAnalysis()
    X = data.copy()
    y = labels.copy()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
    model.fit(X_train, y_train)
    pred = model.predict(X)
    #acc = accuracy_score(pred, y_test)
   # print('Accuracy: ', acc)
    pred = pd.Series(pred)
    lcm = pd.crosstab(y, pred, normalize = normalize).to_numpy()
    N = len(data)
  #  print(lcm)
    lcmNew = correctTM(lcm, N, noiseLevel)
    return lcmNew
'''
def addNoiseScikit(data, labels, noise_level = 0.2, rs = 3423, classifier = LinearDiscriminantAnalysis()):
 #   lcm = getTransitionMatrix(data, labels,normalize = True, noiseLevel = noise_level)
  #  print(lcm)
    noisyLabelsUniform = flip_labels_uniform(labels, noise_level = noise_level, random_state = rs)
   # noisyLabelsCC = flip_labels_cc(labels,lcm = lcm,random_state = rs)
    bcnoise = BCNoise(noise_level = noise_level, classifier = classifier , random_state = rs)
    noisyLabelsBCNoise = bcnoise.simulate_noise(data, labels)[1]
    
    return noisyLabelsUniform, None, noisyLabelsBCNoise

