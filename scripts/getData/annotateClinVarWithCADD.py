import pysam
import pandas as pd
from tqdm import tqdm

# file = snakemake.input.cadd
# clinvar = snakemake.input.cv
# output = str(snakemake.output)
# test = snakemake.params.test

test = False
#clinvar = "dataProduced/ClinVarTwoLabels.csv.gz"
file = "dataRaw/all_SNV_inclAnno.tsv.gz"
caddInd = "dataRaw/all_SNV_inclAnno.tsv.gz.tbi"
#output = "dataProduced/ClinVarAnnoLabels.csv.gz" 

clinvar = "dataProduced/ClinVarTwoLabelsJune23Sample.csv.gz"
output = "dataProduced/ClinVarAnnoTwoLabelsJune23Sample.csv.gz" 

        
if test:
    nrows = 500
else:
    nrows = 1000000000
    
allYears = pd.read_csv(clinvar, sep = '\t', compression = 'zip', nrows = nrows) 

tabixfile = pysam.TabixFile(file)
header = list(tabixfile.header)[1].split('\t')

lines = []
    
for row in tqdm(allYears.itertuples(),  total=allYears.shape[0]):
    for line in tabixfile.fetch(row.Chromosome, row.Start-1, row.Start):
        line = line.split('\t')
        fref = line[2]
        falt = line[3]
        if (fref==row.Ref)&(falt==row.Alt):
            lines.append(line)
df = pd.DataFrame(lines)
df.columns = header
df= df.drop_duplicates(subset = header[:4]).reset_index(drop = True)
labels = ['LabelOld', 'LabelNew']
print('Length of CADD annotated variants is {}, length of ClinVar variants {}'.format(len(df), len(allYears)))
df[labels] = allYears[labels]

df.to_csv(output, compression = 'zip',sep =  '\t',
         index = None)