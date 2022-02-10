import random
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


class Noise:
    # returns a list of corrupted labels
    def __init__(self, X, y, n=0.2):
        
        self.X = X
        self.y = y
        
        self.df = X.copy()
        self.labels = y.astype(str).copy()
        self.n = n
      #  display(self.labels)
    
    
    def getError(self, values, x):
        values = list(set(values) - set(x))
        e = random.choices(values, k = 1)
        return e[0]

    def symmetricNoise(self):
        col = 'Symmetric noise'
        self.df[col] = self.labels
        ## define the number of errors
        self.nErrorsSym = round(len(self.df)*self.n)
       # print(self.nErrorsSym)
        ## set index of error data points
        self.idxErrorSym = random.sample(range(len(self.df)),self.nErrorsSym)
        self.values = np.unique(self.labels)
        self.df.iloc[list(self.idxErrorSym),-1] = self.df.iloc[list(self.idxErrorSym),-1].apply(lambda x: self.getError(self.values, x ))
        print('Number of symmetric errors: ', (self.df.iloc[:,-1] !=self.labels).sum())

        return self.df.loc[:,col].astype(float).astype(int)


    def getNoiseGroups(self):
        X = self.X.copy()
        y = self.y.copy()

        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        model = LogisticRegression(solver='lbfgs', multi_class='auto', max_iter=5)
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        acc = accuracy_score(pred, y_test) # if acc==1, the return table is empty
        print('Accuracy: ', acc)
        a = pred[pred!=y_test]
        b = y_test[pred!=y_test]

        c = pd.Series(a).reset_index(drop = True).astype(str)+' ' + pd.Series(b).reset_index(drop = True).astype(str)
        cc = pd.DataFrame(c.value_counts(normalize = False))

        errorTable = pd.Series(cc.index).str.split(' ', expand = True)
        errorTable['Frequency'] = cc[0].astype(int).tolist()
        errorTable = errorTable.astype(float).astype(int)
        if len(errorTable)>0:
            errorTable.columns = ['True label', 'False label', 'Frequency']
    
        return errorTable


    def asymmetricNoise(self):

        col = 'Asymmetric Noise'
        self.df[col] = self.labels.astype(str)
        self.cc = self.getNoiseGroups()
        # total number of errors to be inserted
        self.nErrors = int(round(len(self.df)*self.n))
        print('Number of errors to impute: ', self.nErrors)
 
        if len(self.cc)<1:
            print('Not enough errors in the model predictions')
        else:
            a = self.nErrors/self.cc['Frequency'].sum()
            self.cc['New Frequency']= (self.cc['Frequency']*a).astype(int)
    
            self.indExclude = np.array([])
            labelsFr = self.labels.value_counts()
      #      display( self.cc)
            
       #     display(labelsFr)

            for i in range(len(self.cc)):
                # error type (eg change label A to label B)
                self.repl = dict(zip(str(int(self.cc.iloc[i,0])),str(int(self.cc.iloc[i,1]))))
                                
                self.fr = self.cc.index[i]
                # absolute number or errors (of one type)
                self.nE = self.cc.loc[i,'New Frequency']
                
               # print('here ', labelsFr[labelsFr.index.astype(float).astype(int)==self.cc.iloc[i,0].astype(float).astype(int)])
                if self.nE >= int(labelsFr[labelsFr.index.astype(float).astype(int)==self.cc.iloc[i,0].astype(float).astype(int)][0]):
                    print('Too few data points with this label')
                    pass
                else:
                      #  self.nE = int(round(int(self.cc.iloc[i,1])*self.n))

                    # index of all data points with matching label
                    self.indLabel = self.df[self.labels.astype(float).astype(int)==self.cc.iloc[i,0].astype(float).astype(int)].index
                    # index of errors (data points with matching label to be replaced)
                  #  display(self.indLabel, self.nE)
                    self.ind = random.sample(list(set(self.indLabel)-set(self.indExclude)), self.nE)
                    self.indExclude = np.hstack([self.indExclude, self.ind])
                #    print('Number of replacements of one type: ',len(self.ind))
                    self.df.loc[self.ind,col] = self.df.loc[self.ind,col].replace(self.repl)
            print('Total number of asymmetric errors ', (self.df.loc[:,col]!=self.labels).sum())
        return self.df.loc[:,col].astype(float).astype(int)
