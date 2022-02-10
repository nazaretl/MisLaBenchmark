#!/bin/bash 

#iter=0 # from snakemake
iter=$1
name='CADDIter'$iter
iterOld=$(($iter - 1))
nameOld='CADDIter'$iterOld
file='SNV.csv.gz'



for class in simulation humanDerived;  do
    for stage in  annotation imputation; do
        path="data/GRCh38/"$nameNew"/"$stage"/"$class"/"
        mkdir -p $path;
        labels='data/predictedLabels/'$nameOld'/'$class'/'$class'_labels.csv'
        old="data/GRCh38/"$nameOld"/"$stage"/"$class"/"
        new="data/GRCh38/"$name"/"$stage"/"$class"/"
        
        

            if [[ $stage == imputation ]]
            then
                echo $old$file;
                paste -d','  <(zcat $old$file)  $labels | awk -F "," -v OFS="," '{if($NF == 1){NF--;print}}'  | bgzip -c >$new$file ;
            else
        (zcat $old$file | head -n 1;  paste -d'\t'  <(zcat $old$file | sed 1d )  $labels | awk -F "\t" -v OFS="\t" '{if($NF == 1){NF--;print}}' ) | bgzip -c >$new$file  
            
            
            fi

      
        #fi
        
        
        
        
       done;
done;

