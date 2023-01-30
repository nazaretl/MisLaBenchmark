import pandas as pd
#include: "/fast/groups/ag_kircher/CADD/projects/bStatistic/github_repo_fork/scripts/pipeline/SnakefileSKMisLa"
configfile: "configs/params.json"
#configfile: "configs/testParams.json"

#imps = ['Python', 'CleanLab','R','DNN']
imps = ['DNN']
noiseTypes=["realNoise", "artNoise"]
#noiseTypes=["realNoise"]

#rule getTempFiles:
#rule preAll:
 #   expand("temp/{dataset}_{noiseLevel}_{datasetSizes}_{noiseType}_{model}_{imp}.tmp", )
'''
def repeat():
    return pd.read_csv('repeatsReal.csv',header = None)[0].to_list()

rule all:
    input:
        repeat()
       
rule test:
    input:
        "temp/DryBean_0.2_1000_Sym_ERL_DNN.tmp"
'''  
    
rule all:
    input:
        lambda wc: expand("done_{noiseTypes}_{imp}.txt", noiseTypes=noiseTypes, imp=imps)
        
        

rule All:
    input:
     #   expand("output/{dataset}_{imp}.csv",dataset = config['parameters']['datasets'],imp = imps),
        lambda wc: expand("temp/{dataset}_{noiseLevel}_{datasetSize}_{noiseType}_{model}_{imp}.tmp", 
                          model = config['implementation'][wc.imp], 
                            noiseLevel = config['parameters']['noiseLevels'],
                                datasetSize = config['parameters']['datasetSizes'],
                                    noiseType = config[wc.noiseTypes]["type"],
                                        dataset = config[wc.noiseTypes]["data"],
                                            imp = wc.imp)
    output:
        touch(temp("done_{noiseTypes}_{imp}.txt"))
rule runParallelShort:
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

    script:
        """scripts/runFiltersAllParallel.py"""       
        
        
'''
rule runParallelLong:
    input:
        "datasets/{dataset}.csv.gz"
    output:
        temp("temp/{dataset}_{noiseLevel}_{datasetSizes}_{noiseType}_{model}_{imp}.tmp")
    params:
        repeats = config['parameters']['repeats']
    script:
        """scripts/runFiltersAllParallel.py"""                                                  
        
        
        
                                

rule createDataSets:
    output:
        "datasets/{dataset}.csv.gz",
    script:
        """scripts/createDataSets.py"""

'''