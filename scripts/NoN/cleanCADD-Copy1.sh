#!/bin/bash 

#iter=0 # from snakemake
iter=$1
name='CADDIter'$iter
file='SNV.anno.tsv.gz'
fileImp='SNV.csv.gz'
## if iter==0

if [[ $iter ==0 ]]; then
    path1="data/GRCh38/CADDIter0_humanDerived/annotation/"
    path11="data/GRCh38/CADDIter0_humanDerived/imputation/"

    mkdir -p $path1
    mkdir -p $path11

    cp data/GRCh38/entireSet_humanDerived/annotation/SNV.anno.tsv.gz $path1$file;
    cp data/GRCh38/entireSet_humanDerived/imputation/SNV.anno.tsv.gz $path11$fileImp;

    path2='data/GRCh38/CADDIter0_simulation/annotation/'
    path22='data/GRCh38/CADDIter0_simulation/imputation/'

    mkdir -p  $path2
    mkdir -p  $path22
    cp data/GRCh38/entireSet_simulation/annotation/SNV.anno.tsv.gz $path2$file;
    cp data/GRCh38/entireSet_simulation/imputation/SNV.anno.tsv.gz $path22$fileImp;
fi
## input
simLabels='data/predictedLabels/'$name'_simulation.cvs'
humLabels='data/predictedLabels/'$name'_humanDerived.cvs'

simOld="data/GRCh38/"$name"_simulation/annotation/"
humOld="data/GRCh38/"$name"_humanDerived/annotation/"


## output
iterNew=$(($iter + 1))
nameNew='CADDIter'$iterNew

simNew="data/GRCh38/"$nameNew"_simulation/annotation/"
humNew="data/GRCh38/"$nameNew"_humanDerived/annotation/"

simNewB="data/GRCh38/balanced"$nameNew"_simulation/annotation/"
humNewB="data/GRCh38/balanced"$nameNew"_humanDerived/annotation/"

temp='data/predictedLabels/'$nameNew'_temp.csv'
col=133


(paste -d'\t'  <(zcat $simOld$file)  $simLabels ; paste -d'\t'  <(zcat $humOld$file)  $humLabels) | grep -v '#' > $temp

mkdir -p $simNew $humNew $simNewB $humNewB


(cat $temp | head -n1 |  cut -f 1-132 ; sed 1d  $temp | awk -F "\t" -v OFS="\t" -v col="$col" '{if($col == 1){print}}' |  cut -f 1-132 )  | bgzip -c > $simNew$file ;
(cat $temp | head -n1 |  cut -f 1-132 ; awk -F "\t" -v OFS="\t" -v col="$col" '{if($col == 0){print}}'  $temp |  cut -f 1-132 )  | bgzip -c > $humNew$file ;

#echo zcat $path2 | wc -l

N1=$(zcat $simNew$file | wc -l)
N2=$(zcat $humNew$file | wc -l)
N=$([ $N1 -le $N2 ] && echo "$N1" || echo "$N2")

echo $N 
(cat $temp | head -n1 |  cut -f 1-132 ; sed 1d  $temp | awk -F "\t" -v OFS="\t" -v col="$col"  '{if($col == 1){print}}' |  cut -f 1-132 )| shuf -n $N  | bgzip -c > $simNewB$file ;

(cat $temp | head -n1 |  cut -f 1-132 ; sed 1d  $temp | awk -F "\t" -v OFS="\t" -v col="$col"  '{if($col == 0){print}}'  |  cut -f 1-132 ) | shuf -n $N  | bgzip -c > $humNewB$file ;

#rm $temp0;
#rm $temp;


