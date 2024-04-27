#!/bin/bash -l

#$ -N check_cif
#$ -l h_rt=10:00:0
#$ -l mem=50G
#$ -pe mpi 4

#$ -m be
#$ -M uceckz0@ucl.ac.uk

#$ -cwd

echo "This script is running on "
hostname

source /home/uceckz0/miniconda3/bin/activate
conda activate cgcnn


python ./check_cif.py ${SGE_TASK_ID}