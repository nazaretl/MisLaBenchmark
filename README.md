This repo contains code for the maniscript *Benchmarking machine learning methods for the identification of mislabeled data*. 

First, the datasets will be downloaded, processed and saved into the folder *datasets* as input for filters. After that, the configs/params.json is read and the filter runs are started.



main file: *runFiltersAllParallel.py* reads
- runRFilter.py reads runRFilter.r
- cleanLabFilter
- filtersScikiClean
- utils
- addNoiseScikit
- DNNwERLLoss

#### Run the workflow
snakemake --use-conda -p   --snakefile Snakefile --rerun-incomplete --cluster-config cluster-ClinVar.json --cluster-status status.py --cluster "sbatch --parsable --nodes=1 --ntasks={cluster.threads} --mem={cluster.mem} -t {cluster.time} -p {cluster.queue} -o {cluster.output} -e {cluster.error}"  --jobs 10 -n 




squeue --me | grep 'medium' |  awk 'BEGIN {FS=" "; ORS=" "} {print $1}' > jobs.txt