#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 08:39:50 2026

@author: robinou

À partir des paramètres d'injection, calcule le nombre de Reynolds du 
Vortex grâce aux paramètres d'injection et la formule trouvée par 
Nathan BAGSHAW
"""

# Librairies importées

import numpy as np

# Paramètres physiques

D = 0.5e-3 # Diamètre de l'aiguille utilisée (m)
nu = 1e-6 # Viscosité cinématique de l'eau (m2/s, pour 20-25 °C)

def Reynolds_Injection(Q) :
    
    '''
    Calcule le nombre de Reynolds ReI du jet d'injection
    du vortex pour un débit donné
    
    Arguments:
        - Q : float ou numpy array 
              débit en mL/min
    Renvoie : 
        - ReI : float ou numpy array
                nombre de Reynolds du jet d'injection
    '''
    
    Q_SI = Q/(1e6*60) # en m3/s
    ReI = (4*Q_SI)/(np.pi*D*nu)
    
    return ReI

def Reynolds_Vortex(Q, dt, t):
    
    '''
    Calcule le nombre de Reynolds du Vortex à une incertitude et une relation
    de proportionnalité près avec la formule trouvée par Nathan BAGSHAW
    
    Arguments : 
        - Q : float ou numpy array
              débit en mL/min
        - dt : float ou numpy array
               durée d'impulsion en s
        - t : float ou numpy array
              temps en s 
    Renvoie : 
        - ReV : float ou numpy array
                le nombre de Reynolds estimé du vortex pour Q, dt, t
        - [ReV_min, ReV_max] : float ou numpy array
                               l'intervalle de confiance sur le nombre 
                               de Reynolds estimé
    '''
    
    ReI = Reynolds_Injection(Q)
    # Nombre de Reynolds du Vortex
    ReV = np.power(ReI,3/2)*dt*np.power(t,-1/2) 
    # Bornes de l'intervalle de confiance
    ReV_min, ReV_max = np.power(ReI,3/2)*dt*np.power(t,-1/2-0.15), np.power(ReI,3/2)*dt*np.power(t,-1/2+0.15)
    
    return ReV, np.array([ReV_min, ReV_max])
    