#!/bin/bash

# download the data from archive.ics.uci.edu 

# HEPMASS (download test because smaller)
wget http://archive.ics.uci.edu/ml/machine-learning-databases/00347/all_test.csv.gz -P dataRaw/
# PockerHand
wget https://archive.ics.uci.edu/ml/machine-learning-databases/poker/poker-hand-training-true.data -P dataRaw/
# Internet+Firewall+Data (IFD)
wget https://archive.ics.uci.edu/ml/machine-learning-databases/00542/log2.csv -P dataRaw/
# Magic
wget https://archive.ics.uci.edu/ml/machine-learning-databases/magic/magic04.data -P dataRaw/
# DryBean
wget https://archive.ics.uci.edu/ml/machine-learning-databases/00602/DryBeanDataset.zip -P dataRaw/
# Adult
wget https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data -P dataRaw/
# Chess
wget https://archive.ics.uci.edu/ml/machine-learning-databases/chess/king-rook-vs-king/krkopt.data -P dataRaw/

# download RNA data
wget https://content.cruk.cam.ac.uk/jmlab/atlas_data.tar.gz -P dataRaw/
tar -xzvf dataRaw/atlas_data.tar.gz -C dataRaw/
rm dataRaw/atlas_data.tar.gz