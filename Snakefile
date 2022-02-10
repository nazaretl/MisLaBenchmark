#include: "/fast/groups/ag_kircher/CADD/projects/bStatistic/github_repo_fork/scripts/pipeline/SnakefileSKMisLa"
configfile: "configs/params.json"
#configfile: "configs/testParams.json"

names = ['Iris', 'RNA0', 'RNA1','RNA2', 'TestT5', 'TestT10', 'ClinVar', 'ClinVarReal']
#models = ['PU']
models = ['entireSet','sampleSet']


datasets = ['Iris','Magic','ClinVarArt', 'ClinVarReal', 'RNA0', 'RNA1', 'RNA2', 'Encode']
#datasets = [Iris,Magic,ClinVarArt,ClinVarReal,RNA0,RNA1,RNA2,Encode,sampleCADD]
#models = [KDN,FKDN,RkDN,PD,MCS,IH,RFD]
#models = [KDN,FKDN,PD,MCS,IH,RFD]

imps = ['Python', 'CleanLab','R']
#imps = ["R"]
noiseTypes=["realNoise", "artNoise"]
#noiseTypes=["realNoise"]


#['ORBoostFilter', 'IPF', 'CNN', 'HARF', 'C45robustFilter', 'C45votingFilter', 'BBNR', 'CVCF', 'C45iteratedVotingFilter'],
#["AENN","CVCF", "edgeBoostFilter", "EF","GE", "HARF", "hybridRepairFilter", "IPF", "ORBoostFilter", "RNN"],
 

#rule getTempFiles:
#rule preAll:
 #   expand("temp/{dataset}_{noiseLevel}_{datasetSizes}_{noiseType}_{model}_{imp}.tmp", )
    
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
        repeats = config['parameters']['repeats']
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
        
        
'''        
                                
'''
rule createDataSets:
    output:
        "datasets/{dataset}.csv.gz",
    script:
        """scripts/createDataSets.py"""

'''