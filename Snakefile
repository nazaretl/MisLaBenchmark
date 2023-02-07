import pandas as pd
configfile: "configs/params.json"

#imps = ['Python', 'CleanLab','R','DNN']
imps = ['DNN']
noiseTypes=["realNoise", "artNoise"]
#noiseTypes=["realNoise"]

Test = True
datasets = ["Adult","DryBean","Chess","Magic","ClinVarArt","ClinVarReal","RNA0","RNA1","RNA2", "HEPMASS","Pokerhand", "IFD"]



def repeat():
    return pd.read_csv('repeats.csv',header = None)[0].to_list()

  
    
rule all:
    input:
        lambda wc: expand("done_{noiseTypes}_{imp}.txt", noiseTypes=noiseTypes, imp=imps)
        
        

rule getRunParams:
    input:
        lambda wc: expand("temp/{dataset}_{noiseLevel}_{datasetSize}_{noiseType}_{model}_{imp}.tmp", 
                          model = config['implementation'][wc.imp], 
                            noiseLevel = config['parameters']['noiseLevels'],
                                datasetSize = config['parameters']['datasetSizes'],
                                    noiseType = config[wc.noiseTypes]["type"],
                                        dataset = config[wc.noiseTypes]["data"],
                                            imp = wc.imp)
    output:
        touch(temp("done_{noiseTypes}_{imp}.txt"))

## run all run from the file repeats.csv (is creacted in the notebook Auswertung if needed)
# rule all: 
#     input:
#         repeat()
       
# rule test:
#     input:
#         "temp/DryBean_0.2_1000_Sym_ERL_DNN.tmp"        
        
rule runParallel:
    input:
        "datasets/{dataset}.csv.gz"
    output:
        temp("temp/{dataset}_{noiseLevel}_{datasetSizes}_{noiseType}_{model}_{imp}.tmp")
    params:
        repeats = config['parameters']['repeats'],
        beta = config['extra_info']['beta'],
        plusLayers = config['extra_info']['plursLayers'],
        learningRate = config['extra_info']['learningRate'],
        scaling = config['extra_info']['scaling'],
        loss = config['extra_info']['loss']
    conda:
        "envs/misla.yml"
    resources: 
        mem_mb=lambda wc: int(wc['datasetSizes'])*3 
    script:
        """scripts/runFiltersAllParallel.py"""       
        
        
        

######## CREATE DATASETS ##########
rule allDatasets:
    input:
        expand("datasets/{dataset}.csv.gz",dataset = datasets)

       
rule createFinalDataSets:
    input:
        expand( "dataProduced/{dataset}.csv.gz",dataset = datasets)

    output:
        expand( "datasets/{dataset}.csv.gz", dataset = datasets),
        expand("datasetsSample/{dataset}.csv.gz", dataset = datasets)
    script:
        """scripts/getData/cleanAndSample.py"""
      
rule prepareData:
    input:
        "rawData.downloaded.txt",
        "dataProduced/ClinVarAnnoLabels.csv.gz",
        "dataProduced/rnaUMAP.csv.gz"
    output:
        temp(expand("dataProduced/{dataset}.csv.gz", dataset = datasets))
    params:
        test = Test
    script:
        """scripts/getData/prepareData.py"""    
    
    
rule annotateClinVarWithCADD:
    input:
        cv = "dataProduced/ClinVarTwoLabels.csv.gz",
        cadd = "dataRaw/all_SNV_inclAnno.tsv.gz",
        caddInd = "dataRaw/all_SNV_inclAnno.tsv.gz.tbi"
    output:
        "dataProduced/ClinVarAnnoLabels.csv.gz"
    params:
        test = Test
    script:
        """scripts/getData/annotateClinVarWithCADD.py"""
    
rule downloadCADDWholeGenome:
    input:
        
    output:
        "dataRaw/all_SNV_inclAnno.tsv.gz",
        "dataRaw/all_SNV_inclAnno.tsv.gz.tbi"
    params:
        download = False
    shell:
        """scripts/getData/downloadCADDData.sh {params.download}"""
        
    
    
rule prepareClinVarLabels:
    input:
        "Clinvar.downloaded.txt"
    output:
        "dataProduced/ClinVarTwoLabels.csv.gz",
        "dataProduced/ClinVarAllLabels.csv.gz"
    params:
        test = Test
    script:
        """scripts/getData/createClinVarOldNewLabels.py"""
        
rule runRNAUmap:
    input:
        "dataRaw/atlas/raw_counts.mtx"
    output:
        "dataProduced/rnaUMAP.csv.gz"
    params:
        test = Test
  #  resources:
   #     mem_mb = 4000
    script:
        "scripts/getData/rnaUMAP.py"
        
rule downloadClinVarData:
    output:
        temp('Clinvar.downloaded.txt')
    shell:
        """scripts/getData/downloadClinVarData.sh {output}"""        

rule downloadData:
    output:
        temp('rawData.downloaded.txt'),
        "dataRaw/atlas/raw_counts.mtx"
    shell:
        """scripts/getData/downloadData.sh {output}"""

