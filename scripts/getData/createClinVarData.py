import pandas as pd
import sys 
from  sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, 'scripts/')

from utils import *

test = sys.argv[1]


if eval(test):
    nrows = 2000
else: 
    nrows = 1000000000
print("Processing {} rows ".format(nrows))

# here only for info, does not run in the script
# prepare for annotaion with CADD
# df = pd.read_csv('dataProduced/ClinVarTwoLabelsJune23Sample.csv.gz',sep = '\t',compression = 'zip')
# df['ID'] = df['LabelOld']+'-'+df['LabelNew']
# cols = ['Chromosome','Start','ID', 'Ref','Alt','LabelOld','LabelNew']
# df[cols].to_csv('dataProduced/ClinVarTwoLabelsJune23Sample_to_be_ann.vcf.gz',
#                 sep = '\t',compression = 'zip', index = False)


# join the annotated file with the label file since the annotation drops the labels
# df = pd.read_csv('dataProduced/ClinVarTwoLabelsJune23Sample.csv.gz',sep = '\t',compression = 'zip')
# df = df.rename(columns = {'Chromosome':'#Chrom'})

# df_anno = pd.read_csv('datasets/ClinVarTwoLabelsJune23Sample_to_be_ann_whole.tsv.gz',sep = '\t')
# conc = pd.concat([df_anno.iloc[:,:-12],df[['LabelOld','LabelNew']]],keys = ['#Chrom','Pos','Ref','Alt'],axis = 1,
#                 join = 'inner') 

# conc.columns = conc.columns.droplevel()
# conc.to_csv('dataProduced/ClinVarAnnoTwoLabelsJune23Sample.csv.gz',sep = '\t',
#            compression = 'zip', index = False)



#ClinVarAnnoLabels
df = pd.read_csv('dataProduced/ClinVarAnnoTwoLabelsJune23Sample.csv.gz', sep = '\t',
               #  index_col = 'Unnamed: 0', 
                 compression = 'zip',
                 nrows = nrows
                )

#cv.columns.get_loc("ConsDetail")
# ConsScore delete
cv = df.iloc[:,6:]
cv['dbscSNV-rf_score'] = cv['dbscSNV-rf_score'].replace('.',np.nan).astype(float)
cv['cHmm_E6'] = cv.loc[:,'cHmm_E6'].astype(float)

cv = cv.replace('-',np.nan)
cv = cv.replace('.',np.nan)



#cols = cv.columns[[2,3,7,31,50,113,117]].to_list() + cv.columns[10:18].to_list() 
cols = ['AnnoType', 'ConsDetail', 'motifEName', 'oAA', 'nAA', 'FeatureID', 'GeneName', 
        'CCDS', 'Intron', 'Exon','GeneID',
       'Domain',
     #   'Dst2SplType', 'SIFTcat', 'PolyPhenCat', 'Consequence'
      # 'EnsembleRegulatoryFeature', 'dbscSNV-rf_score'
       ]

print('Deleting columns ', cols)
cv = cv.drop(columns = cols)#.value_counts()
cv = cv[~cv['LabelNew'].isna()]
cv = cv[~((cv['LabelNew']=='Conflicting interpretations')|(cv['LabelOld']=='Conflicting interpretations'))]

cs = {'Uncertain significance': 2,
      'VUS' :2,
        'Benign':0,
        'Pathogenic':1,
        'Conflicting interpretations':3,
      'Conflicting':3
     }
cs_inv = {v: k for k, v in cs.items()}
cv[['LabelOld','LabelNew']] = cv[['LabelOld','LabelNew']].replace(cs)

## add the PCA reduced dataset
X = cv.iloc[:,:-2].values
X = StandardScaler().fit_transform(X)
pca = PCA(n_components=72)
pca.fit(X)
X = pca.transform(X)
print('Explained variance: ',pca.explained_variance_ratio_.sum())
df_pca = pd.DataFrame(X)
df_pca = pd.concat([df_pca, cv.iloc[:,-2:]],axis = 1)
df_pca.to_csv('dataProduced/ClinVarRealPCA.csv.gz',sep = '\t',index = False, compression = 'zip') 


types = cv.dtypes.replace('object','category')
cv = cv.astype(types)

cv.to_csv('dataProduced/ClinVarReal.csv.gz',sep = '\t', index = None, 
          compression = 'zip')

cv = cv.drop(columns = ['LabelOld'])
cv = cv.rename(columns = {'LabelNew':'Label'})

cv.to_csv('dataProduced/ClinVarArt.csv.gz',sep = '\t', index = None, 
        compression = 'zip')


 