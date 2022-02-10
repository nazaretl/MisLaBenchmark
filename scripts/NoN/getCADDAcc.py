import pandas as pd

st =str(snakemake.output)
name = st.split('/')[1].split('_')[0]
#name = 'GRCh38-PU'
file = '/fast/users/nazaretl_c/work/MisLaProject/data/skmodels/'+name+'/logs/LR-Ce-01-wmo'
text = pd.read_csv(file, sep = '\n',header = None)

str1  = 'The training reached an accuracy of'
str2 = 'The test classification has an accuracy of'

trainAcc =  text[0][text[0].str.contains(str1)].str.split(' ',  expand = True)[6].astype(float)
testAcc =  text[0][text[0].str.contains(str2)].str.split(' ',  expand = True)[7].astype(float)

def results(res):
    return [res.mean(), res.min(), res.max(), res.std()]

trainAcc = results(trainAcc)
testAcc = results(testAcc)


cols = ['Mean', 'Min', 'Max', 'Std']
file = 'output/'+name+'_results.txt'
df = pd.DataFrame([testAcc])
df.columns = cols
df.to_csv(file, sep = '\t')