 #!/bin/bash 

#name='PUAll'
name=$1
#name='sampleCADDMCS'
file='SNV.anno.tsv.gz'
path1="data/GRCh38/"$name"_simulation/annotation/"
path2="data/GRCh38/"$name"_humanDerived/annotation/"
path3="data/GRCh38/balanced"$name"_simulation/annotation/"
path4="data/GRCh38/balanced"$name"_humanDerived/annotation/"

echo $path1
mkdir -p $path1 $path2 $path3 $path4

labels='data/GRCh38/NewLabels/'$name'_labels.csv'
temp0='data/GRCh38/NewLabels/'$name'_temp0.csv'
temp='data/GRCh38/NewLabels/'$name'_temp.csv'

if [[ $name =~ "All" ]]; then
   sampleCADD='datasets/CADD.csv.gz';
    else
   sampleCADD='datasets/sampleCADD.csv.gz';
fi

paste -d'\t'  <(zcat $sampleCADD)  $labels > $temp0 ;


if [[ $name =~ "sampleCADD" ]]; then
   col=133;
   cat $temp0 | awk -F "\t" -v OFS="\t"  '{if($134 >= 0.5){print}}' > $temp
    echo 'dummy' > 'data/GRCh38/NewLabels/balanced'$name'_labels.csv'

   else
   col=134;
   cp $temp0 $temp
fi

#sampleCADD='datasets/sampleCADD.csv'



(cat $temp | head -n1 |  cut -f 1-132 ; awk -F "\t" -v OFS="\t" -v col="$col" '{if($col == 1){print}}'  $temp |  cut -f 1-132 )  | bgzip -c > $path1$file ;
(cat $temp | head -n1 |  cut -f 1-132 ; awk -F "\t" -v OFS="\t" -v col="$col" '{if($col == 0){print}}'  $temp |  cut -f 1-132 )  | bgzip -c > $path2$file ;

#echo zcat $path2 | wc -l

N1=$(zcat $path1$file | wc -l)
N2=$(zcat $path2$file | wc -l)
N=$([ $N1 -le $N2 ] && echo "$N1" || echo "$N2")

echo $N 
(cat $temp | head -n1 |  cut -f 1-132 ; awk -F "\t" -v OFS="\t" -v col="$col"  '{if($col == 1){print}}'  $temp |  cut -f 1-132 )| shuf -n $N  | bgzip -c > $path3$file ;

(cat $temp | head -n1 |  cut -f 1-132 ; awk -F "\t" -v OFS="\t" -v col="$col"  '{if($col == 0){print}}'  $temp |  cut -f 1-132 ) | shuf -n $N  | bgzip -c > $path4$file ;

#rm $temp0;
#rm $temp;
