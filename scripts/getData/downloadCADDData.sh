#!/bin/bash

download=$1


if [[ $download == True ]]; then
    wget https://kircherlab.bihealth.org/download/CADD/v1.6/GRCh38/whole_genome_SNVs_inclAnno.tsv.gz -P dataRaw/
    wget https://kircherlab.bihealth.org/download/CADD/v1.6/GRCh38/whole_genome_SNVs_inclAnno.tsv.gz.tbi dataRaw/
else
    ln -sf /fast/work/groups/ag_kircher/CADD/projects/genome16/whole_genome_GRCh38/all_SNV_inclAnno.tsv.gz dataRaw/
    ln -sf /fast/work/groups/ag_kircher/CADD/projects/genome16/whole_genome_GRCh38/all_SNV_inclAnno.tsv.gz.tbi dataRaw/
        fi