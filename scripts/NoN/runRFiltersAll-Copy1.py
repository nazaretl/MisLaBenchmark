import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from utils import confusionMatrixScikit
import contextlib

models = [ 
    'AENN(df)' 
     #      ,'BBNR(df, k = k)'
      #     ,'C45robustFilter(df)'
       #    ,'C45votingFilter(df, nfolds = nfolds, consensus = FALSE)'
        #   ,'C45iteratedVotingFilter(df, nfolds = nfolds, consensus = FALSE)'
         #  ,'CNN(df)'
           ,'CVCF(df, nfolds = nfolds, consensus = FALSE)'
         #  ,'DROP1(df, k = 1)'
         #  ,'DROP2(df, k = 2)'
         #  ,'DROP3(df, k = 3)'
         #  ,'dynamicCF(df, nfolds = nfolds, consensus = FALSE, m = 3)'
           ,'edgeBoostFilter(df, m = 15, percent = 0.05, threshold = 0.2)'
           ,'EF(df, nfolds = nfolds, consensus = TRUE)'
          # ,'ENG(df, graph = "RNG")'
        #   ,'EWF(df, threshold = 0.25, noiseAction = "remove")'
           ,'GE(df, k = k, kk = ceiling(k/2))'
           ,'HARF(df, nfolds = nfolds, agreementLevel = 0.7, ntrees = 500)'
           ,'hybridRepairFilter(df, consensus = FALSE, noiseAction = "remove")'
       #    ,'INFFC(df, consensus = FALSE, p = 0.01, s = 3, k = k, threshold = 0)'
           ,'IPF(df, nfolds = nfolds, consensus = FALSE, p = 0.01, s = 3, y = 0.5)'
        #   ,'ModeFilter(df, type = "classical", noiseAction = "repair", epsilon = 0.05, maxIter = 100, alpha = 1, beta = 1)'
           ,'ORBoostFilter(df, N = 20, d = 11, Naux = max(20, N), useDecisionStump = FALSE)'
        #   ,'PF(df, nfolds = nfolds, consensus = FALSE, p = 0.01, s = 3, y = 0.5, theta = 0.7)'
          # ,'PRISM(df)'
           ,'RNN(df)'
       #    ,'saturationFilter(df, noiseThreshold = noiseThreshold)'
        #   ,'consensusSF(df, nfolds = nfolds, consensusLevel = nfolds - 1, noiseThreshold = noiseThreshold)'
       #    ,'classifSF(df, nfolds = nfolds, noiseThreshold = noiseThreshold)'
        #   ,'TomekLinks(df)'
]

path='scripts/'
def runRFilters(string,df):
    r=ro.r
    r.source(path+'runRFilters.r')
    p=r.runRFilters(string, df)
    return p

def getOneRModel(model, dR, y, noisyLabels):
    with localconverter(ro.default_converter + pandas2ri.converter):
        dfR = ro.conversion.py2rpy(dR)
    filteredNoiseInd = pd.Series(runRFilters(model, dfR))
    noiseInd = y[y!=noisyLabels].index
    cv, score = confusionMatrixScikit(y,noiseInd,filteredNoiseInd)
    return cv, score

def getAllRModels(dR, y, noisyLabels):
    cvs = pd.DataFrame()
    scores = pd.DataFrame()
    for model in models:
      #  print(model.split('('))
        ind = model.split('(')[0]

        with contextlib.redirect_stdout(None):
            cv, score = getOneRModel(model, dR, y, noisyLabels )
        cv.index = [ind]
        score.index = [ind]
        cvs = cvs.append(cv)
        scores = scores.append(score)
    return cvs, scores