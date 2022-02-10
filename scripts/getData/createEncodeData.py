# https://www.encodeproject.org/experiments/ENCSR486GER/  
## pseudoreplicated ENCFF600ROA ENCFF028CDS ENCFF360OBA (hg19)
## normal ENCFF476WLE(hg19)  ENCFF475GRY 

# https://www.encodeproject.org/experiments/ENCSR502NRF/  
## ENCFF989DLF (IDR thresholded peaks) ENCFF020UCD (optimal IDR thresholded peaks) ENCFF386TTQ (hg19 optimal IDR thresholded peaks)
## conservative IDR thresholded peaks: ENCFF714AHN (hg19) ENCFF554VSA  ENCFF434MTN 

# https://www.encodeproject.org/experiments/ENCSR000BOX/ 
## (optimal) IDR thresholded peaks: ENCFF884WVM ENCFF896RCP ENCFF474KHR(hg19)
# andere DB (dbsnp)


import pandas as pd
import random
import numpy as np
import os 
os.chdir("dataProduced/Encode/")

def getSample(dfPos, dfNeg):
    df = pd.concat([dfPos,dfNeg]).drop_duplicates(keep=False).reset_index(drop = True)
    n = int(round(len(dfPos)/2))
    N = len(df)
    ind = random.sample(range(N),n)
    return df.iloc[ind,:10].reset_index(drop = True)


file381 = 'ENCFF884WVM' #Encode3
file382 = 'ENCFF896RCP' #Encode4
file19 = 'ENCFF474KHR'
fileNeg1 = 'ENCFF700TEI' #Encode3 ENCFF700TEI ENCFF186TMO
fileNeg2 = 'ENCFF071IVL' #Encode4

df1 = pd.read_csv(file381+'.bed.gz',sep = '\t', compression='infer', header = None)
df2 = pd.read_csv(file382+'.bed.gz',sep = '\t', compression='infer', header = None)
df19 = pd.read_csv(file19+'.bed.gz',sep = '\t', compression='infer', header = None)
dfNeg1 = pd.read_csv(fileNeg1+'.bed.gz',sep = '\t', compression='infer', header = None)
dfNeg1 = dfNeg1.iloc[:,:10]
dfNeg2 = pd.read_csv(fileNeg2+'.bed.gz',sep = '\t', compression='infer', header = None)

df1 = df1.loc[~df1.duplicated([1], keep = False),:]
df2 = df2.loc[~df2.duplicated([1], keep = False),:]

temp1 = getSample(df1, dfNeg1)
temp2 = getSample(df2, dfNeg2)
dfNeg = temp1.append(temp2)


df1['LabelOld'] = 1
df1['LabelNew'] = np.nan

df2['LabelNew'] = 1
df2['LabelOld'] = np.nan

dfNeg['LabelOld'] = 0
dfNeg['LabelNew'] = 0

df1 = df1.set_index([0,1])
df2 = df2.set_index([0,1])

df1.loc[df1.index.isin(df2.index),'LabelNew'] = 1
df2.loc[df2.index.isin(df1.index),'LabelOld'] = 1

df = pd.concat([df1,df2],axis = 0).reset_index(drop = False).drop_duplicates([0,1,2])
df[['LabelOld', 'LabelNew']] = df[['LabelOld', 'LabelNew']].replace(np.nan,0)

df = df.append(dfNeg)
df[10] = df[2]-df[1]+1

df = df.sort_values([0,1])

df1 = df[[4,6,8,9,10, 'LabelOld','LabelNew']]
df1.to_csv('../../datasets/EncodeReal.csv.gz',sep = '\t', index = None, compression = 'zip')

df2 = df[[4,6,8,9,10,'LabelNew']]
df2.to_csv('../../datasets/EncodeArt.csv.gz',sep = '\t', index = None, compression = 'zip')
