#!/home/sthalabard/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:47:39 2019
Start-Up File for Spyder
@author: sthalabard
"""

from matplotlib import pyplot as plt
from matplotlib.pyplot import *
from matplotlib.ticker import MultipleLocator
from matplotlib import animation,cm,rc,colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource, LogNorm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib  import ticker as mticker


#%%
def newfig(a=1,b=1,figheight=12,aspectratio=0.75,fontsize=36,**kwargs):
    rc('legend', frameon=False,fancybox=False,shadow=False,fontsize=28,loc='best')
    rc('lines', linewidth=1)
    font = {'family':'serif','size':fontsize}
    rc('font',**font)
    rc('text', usetex=True)
    rc('xtick',labelsize=fontsize)
    rc('ytick',labelsize=fontsize)
    rc('savefig',format='pdf')
    return plt.subplots(a,b,figsize=(b*figheight,a*figheight*aspectratio),clear=True,tight_layout=True,**kwargs)

def newfig_3d(figheight=12,aspectratio=0.75,**kwargs):
    rc('legend', frameon=False,fancybox=False,shadow=False,fontsize=26,loc='best')
    rc('lines', linewidth=1)
    font = {'family':'serif','size':32}
    rc('font',**font)
    rc('text', usetex=True)
    rc('xtick',labelsize=32)
    rc('ytick',labelsize=32)
    rc('savefig',format='pdf')
    fig = plt.figure(figsize=(figheight,figheight*aspectratio),clear=True,tight_layout=True,**kwargs)
    ax = fig.add_subplot(111, projection='3d')
    ax.grid(False)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.xaxis._axinfo['tick']['inward_factor'] = 0
    ax.xaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.yaxis._axinfo['tick']['inward_factor'] = 0
    ax.yaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['inward_factor'] = 0
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
    ax.zaxis._axinfo['tick']['outward_factor'] = 0.4
    
#    ax.xaxis.set_major_locator(MultipleLocator(5))
#    ax.yaxis.set_major_locator(MultipleLocator(5))
#    ax.zaxis.set_major_locator(MultipleLocator(0.01))
    return fig,ax
