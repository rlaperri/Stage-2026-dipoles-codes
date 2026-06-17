#!/home/sthalabard/Software/anaconda3/envs/dedalus3/bin/python3

# -*- coding: utf-8 -*-
"""
Created on 2024/04/30
Analysis
@author: sthalabard
"""

#% Startup 
import os, sys, glob, shutil, warnings
warnings.simplefilter('ignore')
import numpy as np
from math import *
import scipy.special as scp
#######
from PyModules.Misc import *
from PyModules.PrettyFigs import *
#%% import dedalus
import dedalus.public as d3
import logging
logger = logging.getLogger(__name__)
import h5py
import VortexFlows as vortex

####################################
#%% STEP 0 : Choose datafolder
N=128
eta=1e2
nu=1e-2
R0=pi/16
DATAFOLDER='TESTRUN/LAMB_FLAT/'
IO=os.path.join(DATAFOLDER,'R%0.3f' %R0,'%d_nu%0.2e_eta%0.2e' %(N,nu,eta))
files = glob.glob(os.path.join(IO,'*.h5'))
nfiles=len(files)
t=np.zeros(nfiles)
for i,f in enumerate(files):
    tmp=f.split(sep='/')[-1].split(sep='out_s')[-1].split(sep='.h5')[0]
    t[i]=float(tmp)
ix=np.argsort(t)
files=list(np.array(files)[ix])
for i,f in enumerate(files): print(f)
print('found %d files' %(len(files),))
#########################################
#%% STEP1: find T
ListOfTaus=[]
ListOfFiles=[]
for i,file in enumerate(files):
    tmp=h5py.File(file,mode='r')
    w = tmp['tasks']['vorticity']
    tau=w.dims[0]['sim_time'][()]
    ListOfTaus.append(tau)
    ListOfFiles.append(tau*0+i)
ListOfTaus=np.concatenate(ListOfTaus)
ListOfFiles=np.concatenate(ListOfFiles)

def find_tau(TAU,ListOfFiles=ListOfFiles,ListOfTaus=ListOfTaus):
    i=np.argmin((ListOfTaus-TAU)**2)
    ifile=int(ListOfFiles[i])
    NewTau=ListOfTaus[ListOfFiles==ifile]
    itau=np.argmin((NewTau-TAU)**2)
    return ifile,itau

#%%
fig,axs=newfig(1,2,num='evo')
f=fig.canvas
ax=axs[0]
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title('$\\omega$')

ax=axs[1]
ax.set_xlabel('$\\tau$')
ax.set_ylabel('$Z$')
ax.set_ylim(0,10)
ax.set_xlim(0,10)

for it,tau in  enumerate(ListOfTaus):
    i,j=find_tau(tau)
    tmp=h5py.File(files[i],mode='r')
    w = tmp['tasks']['vorticity']
    winst=w[j,:,:]
    s=vortex.flow(winst)
    data=winst.T; 
    wmax=np.abs(data).max()
    Z=(np.abs(data)**2).mean()**0.5

    if it==0:
        x=w.dims[1]['x'][()]
        z=w.dims[2]['y'][()]
        xx,zz=np.meshgrid(x,x)
        ax=axs[0]
        ha=ax.imshow(data/wmax,vmin=-4,vmax=4,cmap=cm.PiYG)

    ha.set_data(data)
    ax=axs[1]
    ax.plot([tau],[Z],'bo',ms=20)

    f.flush_events()
    f.draw()



