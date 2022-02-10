 #!/bin/bash 

file1=data/GRCh38/entireSet_simulation/annotation/SNV.anno.tsv.gz;
file2=data/GRCh38/entireSet_humanDerived/annotation/SNV.anno.tsv.gz;

file3=data/GRCh38/sampleSet_simulation/annotation/SNV.anno.tsv.gz;
file4=data/GRCh38/sampleSet_humanDerived/annotation/SNV.anno.tsv.gz;
file5=datasets/sampleCADD.csv.gz;
file6=datasets/CADD.csv.gz;


(zcat $file1 | head -n1 ; zcat $file1| grep -v '#' | shuf -n 250000 )  | bgzip -c > $file3 ;
(zcat $file2 | head -n1 ; zcat $file2| grep -v '#' | shuf -n 250000 )  | bgzip  -c > $file4 ;


(zcat $file3 | head -n1 | awk -F '\t' -v OFS='\t' -v ph="Label" '{print $0, ph}'  ; zcat $file3| grep -v '#' |awk -F '\t' -v OFS='\t' '{print $0, 1}' ; zcat $file4| grep -v '#' | awk -F '\t' -v OFS='\t' '{print $0, 0}' )| bgzip -c  > $file5


(zcat $file1 | head -n1 | awk -F '\t' -v OFS='\t' -v ph="Label" '{print $0, ph}'  ; zcat $file1| grep -v '#' |awk -F '\t' -v OFS='\t' '{print $0, 1}' ; zcat $file2| grep -v '#' | awk -F '\t' -v OFS='\t' '{print $0, 0}' ) | bgzip -c > $file6
