#!/bin/bash -l

#$ -N band_gap
#$ -l h_rt=72:00:0
#$ -l mem=10G
#$ -l gpu=1
#$ -ac allow=EFL

#$ -m be
#$ -M uceckz0@ucl.ac.uk

#$ -cwd

echo "This script is running on "
hostname

echo "GPU information" 
nvidia-smi

source /home/uceckz0/miniconda3/bin/activate
conda activate cgcnn
echo "Python environment activated"

timestamp=$(date +%d-%m-%Y_%H:%M:%S)
echo $timestamp
python ../main.py /home/uceckz0/Project/cgcnn/data\
    --epochs 200\
    --train-ratio 0.9\
    --target band_gap
echo $timestamp