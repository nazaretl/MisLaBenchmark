#!/bin/bash

path=.snakemake/log/2023-03-15T083631.486411.snakemake.log

jobIDs=($(cat $path | grep 'external jobid' | cut -d ' ' -f 7 | sed "s/'/ /g" | sed "s/\./ /g" ))
ruleNames=($(cat $path | grep rule | cut -d ' ' -f 2 |  sed "s/\:/ /g"| sed "s/\./ /g" ))
rm -f test.txt

N=${#jobIDs[@]}
N1=${#ruleNames[@]}
echo $N $N1

fields=JobName,CPUTime,MaxDiskRead,AllocCPUS,Elapsed,MaxVMSize,MaxRSS,MaxDiskWrite,MinCPU,SystemCPU,TotalCPU,AveDiskRead,AveDiskWrite,ConsumedEnergy,ConsumedEnergyRaw
header=$(sacct -j ${jobIDs[0]} --format=$fields | head -n 1); 
echo -e  "ID,"  $fields  >> test.txt


for i in $(seq 0 $N) ; do
    ID=${jobIDs[$i]}
    echo $ID
   # name=${ruleNames[$i]}
   # echo $i
    n=$(find /data/gpfs-1/users/nazaretl_c/scratch/logs/  -name "*$ID*.err" -print)
    n=($(echo  $n  |  sed "s:\.: :g" ))
    name=${n[1]}

    #echo $(echo $name | tr '.' '\n')
    #echo ${n[$6]}

    #name=${name[$1]}
    info=$(sacct -j $ID --format=$fields | tail -n3 ); 
  #  echo $info
#    for string in  batch snakejob extern;
    for string in  batch;

      do line=$(echo -e "$info" | grep -e $string )
          echo -e  $ID "$line" | awk 'BEGIN {FS=" ";OFS=","} {$1=$1} {print $0}' >> test.txt
          #awk -v FS=' ' -OFS=';'  '{print $0}' >> test.txt; 
          done
    done 
    
