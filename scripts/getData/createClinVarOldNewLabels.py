import pandas as pd
import os
from glob import glob

#output = snakemake.output
#test = snakemake.params.test
# not all years have data for all months
years = [2015,2016,2017,2018,2019,2020,2021,2022,2023]  
#years = [2023]  

test = False

if test:
   years = [2016]


sample = False
if sample:
    
    output = ["dataProduced/ClinVarTwoLabelsSample.csv.gz",
        "dataProduced/ClinVarAllLabelsSample.csv.gz",
         "dataProduced/ClinVarTwoLabelsJune23Sample.csv.gz"]
else:
    output = ["dataProduced/ClinVarTwoLabelsAllVarians.csv.gz",
        "dataProduced/ClinVarAllLabelsAllVariants.csv.gz",
             "dataProduced/ClinVarTwoLabelsJune23AllVariants.csv.gz"]

print(output[0])
print(output[1])
# the ClinicalSignificance columns has various classes, take only these to avoid ambiguity 
classes = ['Uncertain significance', 'Likely benign', 'Benign', 'Conflicting interpretations of pathogenicity', 
           'Pathogenic', 'Likely pathogenic', 'Benign/Likely benign', 'Pathogenic/Likely pathogenic']

to_replace = {'Uncertain significance': 'VUS', 
              'Conflicting interpretations':'Conflicting',
              'Conflicting interpretations of pathogenicity':'Conflicting',
             'Pathogenic/Likely pathogenic': 'Pathogenic',
             'Likely pathogenic' :'Pathogenic',
             'Benign/Likely benign' : 'Benign',
             'Likely benign' :'Benign'}

CHR = pd.Series(list(range(1,23))+['X','Y']).astype(str)

dates = []
di = {'Ref': ['ReferenceAllele', 'ReferenceAlleleVCF'],
                 'Alt' : ['AlternateAllele', 'AlternateAlleleVCF' ]}
allYears = pd.DataFrame()
for year in years:
    y = str(year)
    print(year)
    files = pd.Series(glob('dataRaw/ClinVar/'+y+'/*')).sort_values()[:]
    for file in files:
        df_temp = pd.read_csv(file,sep = '\t',low_memory=False, na_values = ['na'])
        
        # some months in 2015 do not have any allele column: ignore them 
        if not sum(df_temp.columns.str.contains('ReferenceAllele')):
            print(file)
            pass 
        else:
            
            d = file.split('_')[2].split('.')[0]
            dates.append(d)
            # drop unnecessary information
            #df_temp = df_temp[df_temp['Type']=='single nucleotide variant']
            df_temp = df_temp[df_temp['Assembly']=='GRCh38']
            df_temp = df_temp[df_temp['ClinicalSignificance'].isin(classes)]
            
            
            
            
            for key in di.keys():
            
                df_temp[key] = df_temp[di[key][0]]
                ind = df_temp[df_temp[key].isna()].index
                # from end of 2020, the ReferenceAllele and AlternateAllele are not used anymore
                # but columns ReferenceAlleleVCF and AlternateAlleleVCF
                if sum(df_temp.columns.str.contains(di[key][1])):

                    df_temp.loc[ind, key] = df_temp.loc[ind, di[key][1]]
                    
            s = len(df_temp)

            cols = ['Chromosome', 'Start', 'Ref', 'Alt']
            df_temp = df_temp.dropna(subset = cols, how = 'any')
            
            if sample:
                df_temp = df_temp[((df_temp['Ref'].str.len()<=50)&(df_temp['Alt'].str.len()<=50))]
                df_temp = df_temp[df_temp['Type'].isin(['single nucleotide variant', 'Deletion', 
               'Indel', 'Insertion'])]
               # df_temp = df_temp[((df_temp['Ref'].isin(['A', 'T', 'C', 'G']))&(df_temp['Alt'].isin(['A', 'T', 'C', 'G'])))]


            
            df_temp = df_temp[df_temp['Chromosome'].astype(str).isin(CHR)]
            df_temp['Start'] = df_temp['Start'].astype(int)

            df_temp = df_temp.drop_duplicates(cols)
           # print('{}: Length of the joint file is {}, dropped {} variants from loaded file'.format(d,len(df_temp),s-len(df_temp)))
            df_temp = df_temp.set_index(cols, drop = False)
            df_temp['ClinicalSignificance'] = df_temp['ClinicalSignificance'].replace(to_replace)
            allYears = pd.concat([allYears, df_temp['ClinicalSignificance']],axis = 1, join = 'outer')
            if allYears.shape[1]>1:
                temp = allYears[~allYears.iloc[:,-1].isna()&~allYears.iloc[:,-2].isna()]

                ch = temp[temp.iloc[:,-1]!=temp.iloc[:,-2]].shape[0]
                print('{}: Length of the joint file is : {}, {} less than the original. {} variants changed their label'\
                      .format(d,len(df_temp),s-len(df_temp),ch))


allYears.columns = dates
# unique keeps the order of the labels occurance
uniqueLabels = allYears.T.apply(lambda x: x.dropna().unique())
allYears['uniqueLabels'] = uniqueLabels
allYears['LabelOld'] = allYears['uniqueLabels'].str[0]
allYears['LabelNew'] = allYears['uniqueLabels'].str[-1]
labels = ['LabelOld', 'LabelNew']



allYears[labels] = allYears[labels].replace(to_replace)


changed = (allYears['LabelOld']!=allYears['LabelNew']).sum()
allYears.index.names = cols

allYears = allYears.sort_index()

print(pd.crosstab(allYears['LabelOld'],allYears['LabelNew']))

print('The final file has {} entries. {} variants changed their clinical interpretation.'.format(len(allYears),changed ))


allYears.to_csv(output[0],index = True, header = True,
                sep='\t', compression = 'zip' )

allYears[labels].to_csv(output[1],index = True, header = True,
                sep='\t', compression = 'zip' )

### drop newsest varints
allYears = allYears[~((allYears['LabelOld'].str.contains('Conflicting'))|(allYears['LabelNew'].str.contains('Conflicting')))]#.sum()

noisy = allYears[allYears['LabelOld']!=allYears['LabelNew']]
#noisy = noisy[~((noisy['LabelOld'].str.contains('Conflicting'))|(noisy['LabelNew'].str.contains('Conflicting')))]#.sum()
print(noisy.shape)
rest = allYears[allYears['LabelOld']==allYears['LabelNew']]

rest.columns[4]
rest.columns[77]
temp = rest.iloc[:,4:77].dropna(how = 'all')

ind = temp.index
cols = ['Chromosome', 'Start','Ref','Alt','LabelOld','LabelNew']
clean = rest.loc[ind,cols]
noisy = noisy[cols]

df = pd.concat([clean, noisy])


df['ID'] = df['LabelOld']+'-'+df['LabelNew']
cols = ['Chromosome','ID', 'Start','Ref','Alt','LabelOld','LabelNew']


df[cols].to_csv(output[2],sep = '\t',index = False,
         compression = 'zip')