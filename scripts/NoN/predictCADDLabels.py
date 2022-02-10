import pandas as pd
import os
#model = str(snakemake.input)
#dataset = str(snakemake.wildcards.modelNew)

#project = 'CADDIter0'

project=str(snakemake.wildcards.project)
#classes = ['humanDerived','simulation']
output=str(snakemake.output)
classes=[str(snakemake.wildcards.classes)]




for cl in classes:
    path0 = 'GRCh38/'+project+'_'+cl+'_filelist.txt'
    df = pd.read_csv(path0, sep = '\t', skiprows = 0,header = None)
    files = df[0].sort_values()
    dfTemp = pd.DataFrame()
    path1 = 'data/predictedLabels/'+project+'/'+cl+'/'
    os.system('mkdir -p {}'.format(path1))
    for file in files:
     
        temp = pd.read_csv(file, sep = '\t', skiprows = 0)
        dfTemp=dfTemp.append(temp)
        
    dfTemp['LabelTrue']=0
    if classes=='simulation':
        q = dfTemp.quantile(q=0.25, axis=0)[0]
        dfTemp.loc[dfTemp['RawScore']>q,'LabelTrue']=1    
    else:
        q = dfTemp.quantile(q=0.75, axis=0)[0]
        dfTemp.loc[dfTemp['RawScore']<q,'LabelTrue']=1 

   
          
    dfTemp.loc[:,['LabelTrue']].to_csv(output, sep = '\t', 
                      index = False, header = False )
        
        
        
        