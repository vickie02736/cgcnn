#!/bin/bash -l

#$ -N band_gap_predict
#$ -l h_rt=72:00:0
#$ -l mem=100G
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
python ../predict.py\
    --modelpath ./output/model_best.pth.tar\
    --cifpath /home/uceckz0/Project/cgcnn/data\
    --target band_gap
echo $timestamp