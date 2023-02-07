#!/bin/bash

output=$1
mkdir -p dataRaw/ClinVar;

for year in 2015 2016 2017 2018 2019; do
    mkdir dataRaw/ClinVar/$year
    for month in 01 02 03 04 05 06 07 08 09 10 11 12; do 
        wget   https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/$year/variant_summary_$year-$month.txt.gz -P dataRaw/ClinVar/$year;
        done
     done
     
     
# years 2020 2021 2022 are in different directory
for year in 2020 2021 2022; do
    mkdir dataRaw/ClinVar/$year
    for month in 01 02 03 04 05 06 07 08 09 10 11 12; do 
        wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/variant_summary_$year-$month.txt.gz -P dataRaw/ClinVar/$year;
        done
     done
     
# year 2023 has only one entry     
for year in 2023; do
    mkdir dataRaw/ClinVar/$year
    for month in 01; do 
        wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/archive/variant_summary_$year-$month.txt.gz -P dataRaw/ClinVar/$year;
        done
     done
     
     
echo "done" > $output
