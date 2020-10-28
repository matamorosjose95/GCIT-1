# -*- coding: utf-8 -*-
"""Entrenamiento_GAN-CIT-0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/149EVOQBf8eGAeTg1mNdkV42ijv7s0l8J
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

from tqdm.notebook import tqdm
import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as datasets

import torch.optim as optim
import torch.autograd as autograd

import matplotlib.pyplot as plt
from matplotlib import cm

from sklearn.preprocessing import StandardScaler

#from skimage import io

import numpy as np 
import sys
from modelos_gancito import *
def data_perm(x,z,batch_size):
  idx = np.random.permutation(len(x))
  z_mb = z[idx][:batch_size]
  x_mb = x[idx][:batch_size]
  x_mb = torch.Tensor(x_mb).float()
  z_mb = torch.Tensor(z_mb).float()
  idxhat = np.random.permutation(len(x_mb))
  idzhat = np.random.permutation(len(z_mb))
  x_hat_mb = x_mb[idxhat]
  z_hat_mb = z_mb[idzhat]
  return z_hat_mb, x_hat_mb, z_mb, x_mb

def training(x_train, y_train, z_train, training_rule, l_r= 1e-4,Iterations = 1000, batch_size = 64, lambda_x = 10,lambda_z = 10, gamma = 0.8, n_z = 62):
  dimX = x_train.shape[1]
  dimZ = z_train.shape[1]
  # Models
  G_net   = Generator(dimZ, dimX, n_z)#.cuda() # z_shape, x_shape, v_shape.
  D_net   = Discriminator(dimX ,dimZ)#.cuda() # x_shape, z_shape
  xMI_net = MINE(dimX)#.cuda()             # x_shape
  zMI_net = zMINE(dimX,dimZ)#.cuda()         # x_shape, Z_shape

  # Optimizers
  D_optimizer   = optim.Adam(D_net.parameters(), lr=l_r, betas=(0.5, 0.99))
  G_optimizer   = optim.Adam(G_net.parameters(), lr=l_r, betas=(0.5, 0.99))
  xMI_optimizer = optim.Adam(xMI_net.parameters(), lr=l_r, betas=(0.5, 0.99))
  zMI_optimizer = optim.Adam(zMI_net.parameters(), lr=l_r, betas=(0.5, 0.99))
  # Train Losses Acum.
  D_loss    = []
  G_loss    = []
  zMI_loss  = []
  xMI_loss  = []
  # Noise
  v_mb = torch.FloatTensor(batch_size, n_z)#.cuda()
  # data evolution
  fine_tunning = 5
  #pbar = tqdm(total=Iterations)
  for i in range(Iterations):
    for k in range(fine_tunning):
      # ruido 
      v_mb.uniform_(0,1)#.cuda()
      # minibatch de datos permutados
      z_hat_mb, x_hat_mb, z_mb, x_mb = data_perm(x_train, z_train, batch_size)
      # muestra falsa generada
      x_fk = G_net.forward(z_mb, v_mb)
      # OPTIMIZACIÓN DEL DISCRIMINADOR
      D_optimizer.zero_grad()
      Discriminator_loss = torch.mean(D_net.forward(x_mb, z_mb) + 1 - D_net.forward(x_fk, z_mb))
      Discriminator_loss.backward()
      D_optimizer.step()
      # OPTIMIZACIÓN MINE X
      xMI_optimizer.zero_grad()
      MINE_x_loss = -1*(torch.mean(xMI_net.forward(x_fk.detach(), x_mb)) - torch.log(torch.mean(torch.exp(xMI_net.forward(x_fk.detach(), x_hat_mb)))))
      MINE_x_loss.backward()
      xMI_optimizer.step()
      # OPTIMIZACIÓN MINE Z
      zMI_optimizer.zero_grad()
      MINE_z_loss = -1*(torch.mean(zMI_net.forward(x_fk.detach(), z_mb)) - torch.log(torch.mean(torch.exp(zMI_net.forward(x_fk.detach(),z_hat_mb)))))
      MINE_z_loss.backward()
      zMI_optimizer.step()
    # end fine tunning
    D_loss.append(Discriminator_loss.detach().cpu().numpy().item())
    xMI_loss.append(-1*MINE_x_loss.detach().cpu().numpy().item())
    zMI_loss.append(-1*MINE_z_loss.detach().cpu().numpy().item())
    # Entrenar RED GENERADORA
    idx = np.random.permutation(len(x_train))
    v_mb.uniform_(0,1)#.cuda()
    z_hat_mb, x_hat_mb, z_mb, x_mb = data_perm(x_train, z_train, batch_size)
    x_fk = G_net.forward(z_mb, v_mb)
    G_optimizer.zero_grad()
    mine_x_loss = torch.mean(xMI_net.forward(x_fk, x_mb)) - torch.log(torch.mean(torch.exp(xMI_net.forward(x_fk, x_hat_mb))))
    mine_z_loss = torch.mean(zMI_net.forward(x_fk.detach(), z_mb)) - torch.log(torch.mean(torch.exp(zMI_net.forward(x_fk.detach(), z_hat_mb))))
    if training_rule =='GCIT_InfoGAN':
      Generator_loss = -1*(torch.mean(D_net.forward(x_fk.detach(),z_mb) - D_net.forward(x_mb, z_mb)) - lambda_x*mine_x_loss -  lambda_z*mine_z_loss)
      Generator_loss.backward()
      G_optimizer.step()
      G_loss.append(-1*Generator_loss.detach().cpu().numpy().item())
      #pbar.update(1)
    if training_rule == 'InfoGAN':
      Generator_loss = -1*(torch.mean(D_net.forward(x_fk.detach(),z_mb) - D_net.forward(x_mb, z_mb)) - lambda_z*mine_z_loss)
      Generator_loss.backward()
      G_optimizer.step()
      G_loss.append(-1*Generator_loss.detach().cpu().numpy().item())
      #pbar.update(1)
    if training_rule == 'GCIT':
      Generator_loss = -1*(torch.mean(D_net.forward(x_fk.detach(),z_mb) - D_net.forward(x_mb, z_mb)) - lambda_x*mine_x_loss)
      Generator_loss.backward()
      G_optimizer.step()
      G_loss.append(-1*Generator_loss.detach().cpu().numpy().item())
      #pbar.update(1)
  D_loss = np.array(D_loss)
  zMI_loss = np.array(zMI_loss)
  xMI_loss = np.array(xMI_loss)
  G_loss = np.array(G_loss)
  #pbar.close()
  return zMI_loss,xMI_loss, G_loss, D_loss, G_net
