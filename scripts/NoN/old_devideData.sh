 #!/bin/bash 

#name='PUAll'
name=$1
name='PUAll'
file='SNV.anno.tsv.gz'
path1="data/GRCh38/"$name"_simulation/annotation/"
path2="data/GRCh38/"$name"_humanDerived/annotation/"
path3="data/GRCh38/balanced"$name"_simulation/annotation/"
path4="data/GRCh38/balanced"$name"_humanDerived/annotation/"

echo $path1
mkdir -p $path1 $path2 $path3 $path4

labels='data/GRCh38/NewLabels/'$name'_labels.csv'
temp='data/GRCh38/NewLabels/'$name'_temp.csv'

if [[ $name =~ "All" ]]; then
   sampleCADD='datasets/CADD.csv.gz';
    else
   sampleCADD='datasets/sampleCADD.csv.gz';
fi

#sampleCADD='datasets/sampleCADD.csv'

paste -d'\t'  <(zcat $sampleCADD)  $labels > $temp ;

(cat $temp | head -n1 |  cut -f 1-132 ; awk -F "\t" -v OFS="\t" '{if($134 == 1){print}}'  $temp |  cut -f 1-132 )  | bgzip -c > $path1$file ;
#echo zcat $path1 | wc -l
(cat $temp | head -n1 |  cut -f 1-137 ; awk -F "\t" -v OFS="\t" '{if($134 == 0){print}}'  $temp |  cut -f 1-132 )  | bgzip -c > $path2$file ;

#echo zcat $path2 | wc -l

(cat $temp | head -n1 |  cut -f 1-132 ; awk -F "\t" -v OFS="\t" '{if($134 == 1){print}}'  $temp |  cut -f 1-132 )  | bgzip -c > $path3$file ;

N=$(zcat $path3$file | wc -l)

(cat $temp | head -n1 |  cut -f 1-137 ; awk -F "\t" -v OFS="\t" '{if($134 == 0){print}}'  $temp |  cut -f 1-132 ) | shuf -n $N  | bgzip -c > $path4$file ;

