#!/home/rlqperri/miniconda3/envs/dedalus3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 15:59:01 2024

@author: sthalabard
"""


#% Startup File
import os, sys, glob, shutil, warnings
warnings.simplefilter('ignore')
import numpy as np
from math import *

import scipy
from PyModules.Misc import *
from PyModules.PrettyFigs import *
import VortexFlows as vortex

#%%
param={
       'N':128, # Resolution
       'R':pi/16,
       'nu': 1e-2,
       'eta':1e3,
       'dealias' : 3/2,
       'stop_sim_time' : 10, #1e-3 for 512
       'dtype' : np.float64,
#       'timestepper' : d3.RK222,
        'every':0.1,
       'VORTEXTYPE':'LAMB',
       'WALL':'FLAT'}
param['max_timestep']=1e-2*(128/param['N'])
param['delta']=6*pi/param['N'] #%%SMOOTHENING OF THE MASK

#%%
p=dic2struc(**param)

#VORTEX
om=vortex.initialize(param)
p.u=scipy.interpolate.RectBivariateSpline(om.x, om.x, om.u.T)
p.v=scipy.interpolate.RectBivariateSpline(om.x, om.x, om.v.T)

#WALL
if p.WALL == 'CIRCULAR':
    mm= (1+np.tanh((np.sqrt(om.xx**2+om.yy**2)-pi/2)/param['delta']))*0.5
elif p.WALL== 'FLATy':
    mm= (1+np.tanh((np.abs(om.yy)-pi/2)/param['delta']))*0.5
elif p.WALL== 'FLAT':
    mm= (1+np.tanh((np.abs(om.xx)-pi/2)/param['delta']))*0.5
else:
    mm_x= (1+np.tanh((np.abs(om.xx)-pi/2)/param['delta']))*0.5
    mm_y= (1+np.tanh((np.abs(om.yy)-pi/2)/param['delta']))*0.5
    mm=mm_x+mm_y
    del mm_x, mm_y
    p.WALL='SQUARE'

p.m=scipy.interpolate.RectBivariateSpline(om.x, om.x, mm.T)
del om, mm
#%%
#TMPFolder='/home/sthalabard/Projects/Estourdi/ArnaudGuardia/dedalus/TMP'
#TMPFolder='/Scratch/VortexData/TMP'
TMPFolder='TESTRUN'
IOtmp=os.path.join(TMPFolder,'0')
i=0
while os.path.exists(IOtmp):
    i+=1
    IOtmp=os.path.join(TMPFolder,'%d' %i)
IOtmpOut=os.path.join(IOtmp,'out')
os.makedirs(IOtmpOut,exist_ok=True)

p.IOtmp=IOtmp
p.IOtmpOut=IOtmpOut
save_dill(data=p,name='param%02d.dill' %i)
