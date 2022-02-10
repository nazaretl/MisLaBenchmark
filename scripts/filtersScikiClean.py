import pandas as pd
from skclean.detectors import KDN, ForestKDN, RkDN, PartitioningDetector, MCS
from skclean.detectors import InstanceHardness, RandomForestDetector
from utils import *  


def getAllFilters():
    filters = []
    filters.append(('KDN', KDN()))
    filters.append(('FKDN', ForestKDN()))
    filters.append(('RkDN', RkDN()))
    filters.append(('PD', PartitioningDetector()))
    filters.append(('MCS', MCS()))
    filters.append(('IH', InstanceHardness()))
    filters.append(('RFD', RandomForestDetector()))
    return filters

# returns a list, does not have to since now is not running over a list but is parall. via snakemake

def chooseFilters(F):
    filters = getAllFilters()

    FF = pd.DataFrame(filters)
    ind = FF[FF[0].isin(F)].index.to_list()
    return pd.Series(filters)[ind].to_list()

#FF = pd.DataFrame(getAllFilters())[0].to_list()

def filtersScikiClean(X,y,noisyLabels,n,model, t = 0.5):
    
    # conf_score - the probability that it has been correctly labeled
    
    noiseInd = y[y!=noisyLabels].index
    filters = chooseFilters(model)
    filt = filters[0][1]
    conf_score = filt.detect(X, noisyLabels)
    filteredNoiseInd = y[conf_score < t].index
    
    return filteredNoiseInd
