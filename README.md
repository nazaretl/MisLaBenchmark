This repo contains code for the maniscript *Benchmarking machine learning methods for the identification of mislabeled data*. 

First, the datasets will be downloaded, processed and saved into the folder *datasets* as input for filters.
ToDo create rules for that



main file: runFiltersAllParallel.py
reads

runRFilter.py reads runRFilter.r
cleanLabFilter
filtersScikiClean
utils
addNoiseScikit
DNNwERLLoss
AEFilter (not needed now)

#### Run the workflow
sbatch_cluster_snakemake  -c cluster.json  -s Snakefile -j 10 -z -i -n
