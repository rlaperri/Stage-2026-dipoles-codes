#!/home/rlqperri/miniconda3/envs/dedalus3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on 2024/05/14
to be launched via the script r_MAIN.py
to be initialized via r_init.py 
@author: sthalabard
"""

#% Startup 
import os, sys, glob, shutil, warnings
warnings.simplefilter('ignore')
import numpy as np
import scipy
from math import *
from PyModules.Misc import *

####### Dedalus
import dedalus.public as d3
import logging
logger = logging.getLogger(__name__)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%% Load parameters and initial condition
####################### https://fr.wikipedia.org/wiki/26_(nombre)###########
paramfile='param00.dill' ##### THIS NEEDS TO BE LINE 26!!!!
param=load_dill(paramfile)
param.timestepper= d3.RK222

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Set Bases
coords = d3.CartesianCoordinates('x', 'y')
dist = d3.Distributor(coords, dtype=param.dtype)
xbasis = d3.RealFourier(coords['x'], size=param.N, bounds=(-pi, pi), dealias=param.dealias)
ybasis = d3.RealFourier(coords['y'], size=param.N, bounds=(-pi, pi), dealias=param.dealias)
#% Subs
x, y = dist.local_grids(xbasis, ybasis)
# Set fields and problem
u = dist.VectorField(coords, name='u', bases=(xbasis,ybasis))
u['g'][0] = param.u(x,y)
u['g'][1] = param.v(x,y)
#%%
nu,eta=param.nu,param.eta

p = dist.Field(name='p', bases=(xbasis,ybasis))
tau_p = dist.Field(name='tau_p')
mask = dist.Field(name='m', bases=(xbasis,ybasis))
mask['g'] = param.m(x,y)
problem = d3.IVP([u, p, tau_p], namespace=locals())
problem.add_equation("dt(u) + grad(p) - nu*lap(u) = - u@grad(u)-eta*u*mask")
problem.add_equation("div(u) + tau_p = 0")
problem.add_equation("integ(p) = 0") 

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Set Solver
solver = problem.build_solver(param.timestepper)
solver.stop_sim_time = param.stop_sim_time #FINAL TIME

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#% Set Analysis
snapshots = solver.evaluator.add_file_handler(param.IOtmpOut, sim_dt=param.every,max_writes=100)
snapshots.add_task(-d3.div(d3.skew(u)), name='vorticity')
#snapshots.add_task(u, name='velocity')
#snapshots.add_task(p, name='pressure')
#snapshots.add_task(mask, name='mask')

# CFL
CFL = d3.CFL(solver, initial_dt=param.max_timestep, cadence=1, safety=0.2, threshold=0.,
             max_change=2., min_change=0., max_dt=param.max_timestep)
CFL.add_velocity(u)
# Flow properties
flow = d3.GlobalFlowProperty(solver, cadence=10)
flow.add_property(u@u, name='u2')

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Main loop
try:
    logger.info('Starting main loop')
    while solver.proceed:
        timestep = CFL.compute_timestep()
        solver.step(timestep)
        if (solver.iteration-1) % 10 == 0:
            rms2 = flow.grid_average('u2')
            logger.info('Iteration=%i, Time=%e, dt=%e, energy=%0.2e' %(solver.iteration, solver.sim_time, timestep,rms2))
except:
    logger.error('Exception raised, triggering end of main loop.')
    raise
finally:
    solver.log_stats()
