import pandas as pd
import sys 
sys.path.insert(0, 'scripts/')

from utils import *

test = sys.argv[1]


if eval(test):
    nrows = 2000
else: 
    nrows = 1000000000
print("Processing {} rows ".format(nrows))

df = pd.read_csv('dataProduced/ClinVarAnnoLabels.csv.gz', sep = '\t',
               #  index_col = 'Unnamed: 0', 
                 compression = 'zip',
                 nrows = nrows
                )

#cv.columns.get_loc("ConsDetail")
# ConsScore delete
cv = df.iloc[:,6:]
cv['dbscSNV-rf_score'] = cv['dbscSNV-rf_score'].replace('.',np.nan).astype(float)
cv['cHmm_E6'] = cv.loc[:,'cHmm_E6'].astype(float)
#cols = cv.columns[[2,3,7,31,50,113,117]].to_list() + cv.columns[10:18].to_list() 
cols = ['AnnoType', 'Consequence', 'ConsDetail', 'motifEName', 'oAA', 'nAA', 'FeatureID', 'GeneName', 
        'CCDS', 'Intron', 'Exon','GeneID',
       'Domain', 'Dst2SplType', 'SIFTcat', 'PolyPhenCat',
       'EnsembleRegulatoryFeature', 'dbscSNV-rf_score']

print('Deleting columns ', cols)
cv = cv.drop(columns = cols)#.value_counts()
cv = cv[~cv['LabelNew'].isna()]
cv = cv[~((cv['LabelNew']=='Conflicting interpretations')|(cv['LabelOld']=='Conflicting interpretations'))]

cs = {'Uncertain significance': 2,
        'Benign':0,
        'Pathogenic':1,
        'Conflicting interpretations':3}
cs_inv = {v: k for k, v in cs.items()}
cv[['LabelOld','LabelNew']] = cv[['LabelOld','LabelNew']].replace(cs)


types = cv.dtypes.replace('object','category')
cv = cv.astype(types)

cv.to_csv('dataProduced/ClinVarReal.csv.gz',sep = '\t', index = None, 
          compression = 'zip')

cv = cv.drop(columns = ['LabelOld'])
cv = cv.rename(columns = {'LabelNew':'Label'})

cv.to_csv('dataProduced/ClinVarArt.csv.gz',sep = '\t', index = None, 
        compression = 'zip')


 