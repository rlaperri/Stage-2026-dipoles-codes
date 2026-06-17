#!/home/sthalabard/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 21:09:17 2022
Miscellaneous functions to make Python Easy
@author: sthalabard
"""


#% Startup File
import os, sys, dill
import numpy as np
from math import *
from time import perf_counter

#%%
class dic2struc:
    def __init__(self, **entries):
        self.__dict__.update(entries)

#%% SAVE/LOAD dill
def save_dill(name='tmp.dill', data=dic2struc()):
    pikd = open(name, 'wb')
    dill.dump(data, pikd)
    pikd.close()
    return None

def load_dill(file):
    pikd = open(file, 'rb')
    data = dill.load(pikd)
    pikd.close()
    return data

#%% TIMING
class tictoc:
    def __init__(self):
        self.tic0=perf_counter()

    def toc(self,message=None):
        if message is None:
            print('%0.2f s'  %(perf_counter()-self.tic0,))
        else:
            print( message, '\t ........ time elapsed:  \t ', '%0.2f s'  %(perf_counter()-self.tic0,))
        return None
    
    def tic(self):
        self.tic0=perf_counter()
        return None

#%% PDF Smoother
def smooth_pdf(pdf,bins,nbins=10,logmin=-5,scale='log'):
    xdata,ydata=bins,pdf
    cum=np.cumsum(ydata)*(xdata[2]-xdata[1])
    newbins=np.interp(np.linspace(0,1,nbins),cum,xdata)
    if scale == 'log':
        newbins_left=np.interp(10**np.linspace(logmin,0,nbins),cum,xdata)
        newbins_bulk=np.interp(np.linspace(0,1,nbins),cum,xdata)
        newbins_right=np.interp(1-10**np.linspace(logmin,0,nbins),cum,xdata)
        newbins=np.sort(np.concatenate((newbins_left,newbins_bulk,newbins_right)))

    cum=np.interp(newbins,xdata,cum)
    newpdf=np.diff(cum)/np.diff(newbins)
    newbins=(newbins[1:]+newbins[:-1])*0.5
    return newpdf,newbins

#%% Cartesian to Sherical coordonates

def cart2sph(x,y,z):
    rho= np.sqrt(x**2 + y**2)
    r=np.sqrt(rho**2+z**2)
    theta=np.arccos(z/r)
    phi=np.angle(x+1j*y)
    return r, theta, phi


 

        