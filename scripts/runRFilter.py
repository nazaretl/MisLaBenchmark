import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from utils import confusionMatrixScikit
import contextlib


modelsR = [ 
            'AENN(df)' 
            ,'BBNR(df, k = k)'
           ,'C45robustFilter(df)'
           ,'C45votingFilter(df, nfolds = nfolds, consensus = FALSE)'
           ,'C45iteratedVotingFilter(df, nfolds = nfolds, consensus = FALSE)'
           ,'CNN(df)'
           ,'CVCF(df, nfolds = nfolds, consensus = FALSE)'
           ,'DROP1(df, k = 1)'
           ,'DROP2(df, k = 2)'
           ,'DROP3(df, k = 3)'
           ,'dynamicCF(df, nfolds = nfolds, consensus = FALSE, m = 3)'
           ,'edgeBoostFilter(df, m = 15, percent = 0.05, threshold = 0.2)'
           ,'EF(df, nfolds = nfolds, consensus = FALSE)'
           ,'ENG(df, graph = "RNG")'
           ,'EWF(df, threshold = 0.25, noiseAction = "remove")'
           ,'GE(df, k = k, kk = ceiling(k/2))'
           ,'HARF(df, nfolds = nfolds, agreementLevel = 0.7, ntrees = 500)'
           ,'hybridRepairFilter(df, consensus = TRUE, noiseAction = "remove")'
           ,'INFFC(df, consensus = FALSE, p = 0.01, s = 3, k = k, threshold = 0)'
           ,'IPF(df, nfolds = nfolds, consensus = FALSE, p = 0.01, s = 3, y = 0.5)'
           ,'ModeFilter(df, type = "classical", noiseAction = "remove", epsilon = 0.05, maxIter = 100, alpha = 1, beta = 1)'
           ,'ORBoostFilter(df, N = 10, d = 11, Naux = max(20, N), useDecisionStump = FALSE)'
           ,'PF(df, nfolds = nfolds, consensus = FALSE, p = 0.01, s = 5, y = 0.3, theta = 0.3)'
           ,'PRISM(df)'
           ,'RNN(df)'
           ,'saturationFilter(df, noiseThreshold = noiseThreshold)'
           ,'consensusSF(df, nfolds = nfolds, consensusLevel = nfolds - 1, noiseThreshold = noiseThreshold)'
           ,'classifSF(df, nfolds = nfolds, noiseThreshold = noiseThreshold)'
           ,'TomekLinks(df)'
]

path='scripts/'
def runRScript(string,df):
  #  string='''suppressMessages({})'''.format(string) 
    r=ro.r
    r.source(path+'runRFilter.r')
    p=r.runRFilters(string, df) ## function from the R the script
    return p

def runOneRModel(model, dR, y, noisyLabels):
    with localconverter(ro.default_converter + pandas2ri.converter):
        dfR = ro.conversion.py2rpy(dR)
    filteredNoiseInd = pd.Series(runRScript(model, dfR))
    return filteredNoiseInd

def chooseFilters(F,filters):
    FF = pd.DataFrame(filters)
    ind = FF[FF[0].str.split('(',expand = True)[0].isin(F)].index.to_list()
    return pd.Series(filters)[ind].to_list()

def getRModel(dR, y, noisyLabels,model):
    
    models = chooseFilters(model, modelsR)
    filt = models[0]
    print(model)
    #ind = filt.split('(')#[0]
    filteredNoiseInd = runOneRModel(filt, dR, y, noisyLabels )
    if len(filteredNoiseInd)!=0:
        if filteredNoiseInd[0]!='failed!':
            filteredNoiseInd = pd.Series(filteredNoiseInd).astype(int)-1
    return filteredNoiseInd
