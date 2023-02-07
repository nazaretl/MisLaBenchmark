import pandas as pd
import os
from glob import glob

output = snakemake.output
test = snakemake.params.test
# not all years have data for all months
years = [2015,2016,2017,2018,2019,2020,2021,2022,2023]  


if test:
    years = [2016]


# the ClinicalSignificance columns has various classes, take only these to avoid ambiguity 
classes = ['Uncertain significance', 'Likely benign', 'Benign', 'Conflicting interpretations of pathogenicity', 
           'Pathogenic', 'Likely pathogenic', 'Benign/Likely benign', 'Pathogenic/Likely pathogenic']

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
            df_temp = df_temp[df_temp['Type']=='single nucleotide variant']
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
            
            df_temp = df_temp[((df_temp['Ref'].isin(['A', 'T', 'C', 'G']))&(df_temp['Alt'].isin(['A', 'T', 'C', 'G'])))]
            df_temp = df_temp[df_temp['Chromosome'].astype(str).isin(CHR)]
            df_temp['Start'] = df_temp['Start'].astype(int)

            df_temp = df_temp.drop_duplicates(cols)
            print('{}: Length of the joint file is {}, dropped {} variants from loaded file'.format(d,len(df_temp),s-len(df_temp)))
            df_temp = df_temp.set_index(cols, drop = False)
            allYears = pd.concat([allYears, df_temp['ClinicalSignificance']],axis = 1, join = 'outer')

allYears.columns = dates
# unique keeps the order of the labels occurance
uniqueLabels = allYears.T.apply(lambda x: x.dropna().unique())
allYears['uniqueLabels'] = uniqueLabels
allYears['LabelOld'] = allYears['uniqueLabels'].str[0]
allYears['LabelNew'] = allYears['uniqueLabels'].str[-1]
labels = ['LabelOld', 'LabelNew']


to_replace = {'Uncertain significance': 'VUS', 
              'Conflicting interpretations':'Conflicting',
             'Pathogenic/Likely pathogenic': 'Pathogenic',
             'Likely pathogenic' :'Pathogenic',
             'Benign/likely benign' : 'Benign',
             'Likely benign' :'Benign'}
allYears[labels] = allYears[labels].replace(to_replace)


changed = (allYears['LabelOld']!=allYears['LabelNew']).sum()
allYears.index.names = cols

allYears = allYears.sort_index()

print('The final file has {} entries. {} variants changed their clinical interpretation.'.format(len(allYears),changed ))


allYears.to_csv(output[0],index = True, header = True,
                sep='\t', compression = 'zip' )

allYears[labels].to_csv(output[1],index = True, header = True,
                sep='\t', compression = 'zip' )