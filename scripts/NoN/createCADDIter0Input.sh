#!/bin/bash 



for class in simulation humanDerived;  do
    for stage in  annotation imputation; do
        mkdir -p data/GRCh38/CADDIter0/$stage/$class
      #  zcat data/GRCh38/entireSet/$stage/$class/SNV.csv.gz | head -n 50000 | bgzip  > data/GRCh38/CADDIter0/$stage/$class/SNV.csv.gz;
         cp data/GRCh38/entireSet/$stage/$class/SNV.csv.gz data/GRCh38/CADDIter0/$stage/$class/SNV.csv.gz;
            done;
        done;