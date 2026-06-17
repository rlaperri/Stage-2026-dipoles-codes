#!/home/sthalabard/Software/anaconda3/envs/dedalus3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s
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
from PyModules.Streams import streams_2d as stream

#%% Calcule fonction de courant et vitesses a partir d'une distribution de vorticite via des fft
def smooth(om,alpha=0):
    N,dum=om.shape

    kx,ky=np.fft.rfftfreq(N,d=1/N),np.fft.fftfreq(N,d=1/N)
    kx,ky=np.meshgrid(kx,ky,indexing ='xy')#psi['g'] = psi['g']*np.exp(-rr**2/eta)
    k=(kx**2+ky**2)**0.5
    om_k=np.fft.rfft2(om,norm='forward')
    om_k=om_k*np.exp(-alpha*k**2)
    om_k[k>N/2]=0.
    om=np.fft.irfft2(om_k,norm='forward')
    return om


def flow(om,g=2,norm=1):
    s=dic2struc()
    N,dum=om.shape
    kx,ky=np.fft.rfftfreq(N,d=1/N),np.fft.fftfreq(N,d=1/N)
    kx,ky=np.meshgrid(kx,ky,indexing ='xy')#psi['g'] = psi['g']*np.exp(-rr**2/eta)
    k=(kx**2+ky**2)**0.5
    s.om_k=np.fft.rfft2(om,norm='forward')
    s.om_k[k>N/2]=0.
    
    s.psi_k=s.om_k/k**g; s.psi_k[0,0]=0
    s.psi=np.fft.irfft2(s.psi_k,norm='forward')

    s.u_k,s.v_k=-1j*ky*s.psi_k,1j*kx*s.psi_k
    s.u=np.fft.irfft2(s.u_k,norm='forward')
    s.v=np.fft.irfft2(s.v_k,norm='forward')
    s.om=om.copy()
    s.kx,s.ky=kx,ky

    bins_c=np.arange(N)
    Ek0,dum=np.histogram(k[:,0],bins=-0.5+bins_c,weights=np.abs(s.u_k[:,0])**2+np.abs(s.v_k[:,0])**2)
    Ek1,dum=np.histogram(k[:,1:],bins=-0.5+bins_c,weights=np.abs(s.u_k[:,1:])**2+np.abs(s.v_k[:,1:])**2)
    s.Ek=Ek0+2*Ek1
    s.kbins=(bins_c[1:]+bins_c[:-1])*0.5

    return s

def compute_spectrum(om):
    s=dic2struc()
    N,dum=om.shape
    kx,ky=np.fft.rfftfreq(N,d=1/N),np.fft.fftfreq(N,d=1/N)
    kx,ky=np.meshgrid(kx,ky,indexing ='xy')
    k=(kx**2+ky**2)**0.5
    s.om_k=np.fft.rfft2(om,norm='forward')
#    s.om_k[k>N/2]=0.

    bins_c=np.arange(N)
    Ek0,dum=np.histogram(k[:,0],bins=-0.5+bins_c,weights=np.abs(s.om_k[:,0])**2)
    Ek1,dum=np.histogram(k[:,1:],bins=-0.5+bins_c,weights=np.abs(s.om_k[:,1:])**2)
    s.Ek=Ek0+2*Ek1
    s.kbins=(bins_c[1:]+bins_c[:-1])*0.5

    return s

#%% Kaufman Vortex
def Kaufmann(G=1,R=1,x=None,y=None,epsilon=0.):
    r=(x**2+y**2)**0.5
#    om=np.zeros_like(x)
    om=G/(pi*R**2)*(1+(r/R)**2)**2
    return om

#%% Lamb Dipole
def Lamb(U=1,R=1,eta=0,x=None,y=None,epsilon=None):
    N,dum=x.shape
    if epsilon==None:
        epsilon=2*pi/N
    b=scp.jn_zeros(1,1)[0]
    r=(x**2+y**2)**0.5
    #régularisation
    r[r<epsilon]=(x[r<epsilon]**2+y[r<epsilon]**2)/(2*epsilon)+epsilon/2
    coeff=-2*U*b/scp.j0(b)
    om=scp.j1(b*r/R)*(y/r)-eta*b/(2*U)*scp.j0(b*r/R)
    om=coeff*om
    om[r>R]=0
    return om

#%%
def Sheet(G=1,x=None,y=None):
    N,dum=x.shape
    om=np.zeros_like(x)
    om[:,N//2]=G
    return om

#%% 
def Mexican(G=1,R=1,x=None,y=None):
    r=(x**2+y**2)**0.5
    om=G/(pi*R**4)*(1-0.5*(r/R)**2)*np.exp(-0.5*(r/R)**2)
    return om

def Haar(G=1,R=1,x=None,y=None):
    r=(x**2+y**2)**0.5
    om=G*np.sign(R-r)
    return om

def Morlet(G=1,R=1,x=None,y=None):
    r=(x**2+y**2)**0.5
    om=G*np.cos(r/R)*np.exp(-0.5*(r/R)**2)
    return om

def MexicanBumpVortex(G=1,R=1,x=None,y=None):
    r=(x**2+y**2)**0.5
    om=G/(pi*R**4)*(1-0.5*(r/R)**2)*np.exp(-1/(1-(r/R)**2))
    om[r>R]=0
    return om

#%%
def initialize(param,sep=None):
    p=dic2struc(**param)
    if sep==None:
        sep=p.R

    kmax=p.N//2
    x=2*pi*(np.arange(p.N)/p.N-0.5)
    xx,yy=np.meshgrid(x,x)
    if p.VORTEXTYPE=='MEXICAN':
        om=Mexican(G=1,R=p.R,x=xx,y=yy-sep)+Mexican(G=-1,R=p.R,x=xx,y=yy+sep)
    elif p.VORTEXTYPE=='LAMB':
        om=Lamb(U=1,R=p.R,x=xx,y=yy)
    elif p.VORTEXTYPE=='HAAR':
        om=Haar(G=1,R=p.R,x=xx,y=yy-sep)+Haar(G=-1,R=p.R,x=xx,y=yy+sep)
    elif p.VORTEXTYPE=='MORLET':
        om=Morlet(G=1,R=p.R,x=xx,y=yy-p.R)+Morlet(G=-1,R=p.R,x=xx,y=yy+p.R)

    init=flow(om,g=2)
    E0=init.Ek.sum()
    om=om/np.sqrt(E0)
    init=flow(om,g=2)
    E0=init.Ek.sum()
    epsd = np.finfo(np.float64).eps
    print("Machine epsilon for double precision : ",epsd)
    Emax=max(epsd,init.Ek[kmax])
    alpha=0.5*np.log(1+init.Ek[kmax]/epsd)/(kmax**2)
    om=smooth(om,alpha=alpha)
    init=flow(om,g=2)
    E0=init.Ek.sum()
    print('energy:', E0)
    
    init.x=x.copy()
    init.y=x.copy()

    init.xx,init.yy=xx,yy
    return init


