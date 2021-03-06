# -*- coding: utf-8 -*-
"""Modelos_gancito.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LJ7CbkRTgQ-O5TTEbJXNBOB3U-S-hvcB
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import numpy as np 
print(torch.__version__)

class Discriminator(nn.Module):
  def __init__(self, dim_x=1, dim_z=1):
    super(Discriminator,self).__init__()
    if dim_z <= 20:
        dim_h = int(3)
    else:
        dim_h = int(dim_z / 10)
    
    self.layers = nn.Sequential(nn.Linear(dim_x + dim_z, dim_h),
                                nn.ReLU(),
                                nn.Linear(dim_h,1),
                                nn.Sigmoid() 
                                )

  def forward(self, x, z):
    xz = torch.cat((x, z), dim=-1)
    p = self.layers(xz)
    return p

class Generator(nn.Module):
  def __init__(self, dim_z=1, dim_x=1, dim_v=1):
    super(Generator,self).__init__()
    if dim_z <= 20:
        dim_h = int(3)
    else:
        dim_h = int(dim_z / 10)

    self.layers = nn.Sequential(nn.Linear(dim_z + dim_v, dim_h),
                                nn.Tanh(),
                                nn.Linear(dim_h, dim_x),
                                nn.Sigmoid()
                                )
  
  def forward(self, z, v):
    zv = torch.cat((z, v), dim=-1)
    x = self.layers(zv)
    return x

class MINE(nn.Module):
  def __init__(self, dim_x=1):
    super(MINE,self).__init__()
    if dim_x <= 20:
        dim_h = int(3)
    else:
        dim_h = int(dim_x / 10)

    self.fc1 = nn.Sequential(nn.Linear(dim_x + dim_x, dim_h), nn.Tanh())
    self.fc2 = nn.Sequential(nn.Linear(dim_x + dim_x, dim_h), nn.Tanh())
    self.out = nn.Linear(dim_h, 1)

  def forward(self, x, x_hat): 
    xx = torch.cat((x,x_hat), dim=-1) 
    IM = self.out(self.fc1(xx) + self.fc2(xx))
    return IM

class zMINE(nn.Module):
  def __init__(self, dim_x=1, dim_z=1):
    super(zMINE,self).__init__()
    if dim_z <= 20:
        dim_h = int(3)
    else:
        dim_h = int(dim_z / 10)

    self.fc1 = nn.Linear(dim_x, dim_h)
    self.fc2 = nn.Linear(dim_z, dim_h)
    self.fc3 = nn.Linear(dim_h, 1)

  def forward(self, x, z): 
    h1 = F.relu(self.fc1(x)+self.fc2(z))
    IM = self.fc3(h1)
    return IM