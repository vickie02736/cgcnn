import sys
sys.path.append(".")
import os

import torch
import torch.nn as nn
from torch import optim

# from dataset import DataBuilder
from dataset_imae import DataBuilder
from torch.utils.data import DataLoader
from tqdm import tqdm
import argparse

from model_imae import VisionTransformer, train


### Argparse
parser = argparse.ArgumentParser(description='Train Vision Transformer')

parser.add_argument('--mask_ratio', type=float, default=0.9, help='Masking ratio')
parser.add_argument('--epochs', type=int, default=200, help='Number of epochs')
parser.add_argument('--batch_size', type=int, default=128, help='Batch size')
parser.add_argument('--rollout_times', type=int, default=1, help='Rollout times')

args = parser.parse_args()
### End of Argparse


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = VisionTransformer(3, 16, 128, device)
model = model.to(device)

batch_size = args.batch_size
train_dataset = DataBuilder('data/train_file.csv',10, args.rollout_times)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_dataset = DataBuilder('data/valid_file.csv',10, args.rollout_times)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

epochs = range(0, args.epochs)

learning_rate = 1e-4
T_start = args.epochs * 0.05 * len(train_dataset) // batch_size
T_start = int(T_start)
optimizer = optim.AdamW(model.parameters(), lr=learning_rate, betas=(0.9, 0.95), weight_decay=0.03)
scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(optimizer, T_start, eta_min=1e-6, last_epoch=-1)
scaler = torch.cuda.amp.GradScaler()

train_loss = []
eval_loss = []

# Path to the checkpoint file
# checkpoint_path = "/home/uceckz0/Scratch/imae/Vit_checkpoint/epoch_{epoch}.pth".format(epoch=101)

# # Load the checkpoint
# checkpoint = torch.load(checkpoint_path)

# # Update model and optimizer with the loaded state dictionaries
# model.load_state_dict(checkpoint['model'])
# optimizer.load_state_dict(checkpoint['optimizer'])
# scaler.load_state_dict(checkpoint['scaler'])

# # Now, you can also access the train and evaluation losses if you need
# train_loss = checkpoint['train_loss']
# eval_loss = checkpoint['eval_loss']



loss_fn = nn.MSELoss()

file_number = int(args.mask_ratio * 10)

for epoch in tqdm(epochs): 
    rec_save_path = "data/Vit_rec_{file_number}".format(file_number=file_number)
    if not os.path.exists(rec_save_path):
        os.makedirs(rec_save_path)
    checkpoint_save_path = "data/Vit_checkpoint_{file_number}".format(file_number=file_number)
    if not os.path.exists(checkpoint_save_path):
        os.makedirs(checkpoint_save_path)

    train(model, optimizer, scheduler, scaler, args.mask_ratio, loss_fn, 
          train_loader, val_loader, epoch,
          checkpoint_save_path, rec_save_path, device)
    