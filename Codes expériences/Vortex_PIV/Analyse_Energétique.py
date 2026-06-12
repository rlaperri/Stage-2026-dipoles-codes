#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:50:08 2026

@author: Robin LAPERRIÈRE

Là il faudra mettre une description du code
s'il te plaît
"""

# Importation des librairres

import cmocean # Jolies colormap
import lvpyio as lv # Extraction des .vc7
import matplotlib.animation as animation # Animations
import matplotlib.pyplot as plt # Graphiques
import numpy as np # Calculs
from scipy.ndimage import gaussian_filter # Filtrage spatial

# Fonctions

def rotationnel(u,v):
    
    '''
    Parameters
    ----------
    u : TYPE
        DESCRIPTION.
    v : TYPE
        DESCRIPTION.

    Returns
    -------
    None.
    '''
        
    dyu = u[:-1,1:] - u[1:,1:]
    dxv = v[1:,1:] - u[1:,:-1]

    return dxv - dyu

def extraction_Ux(dossier,n):
    
    '''
    À partir d'un dossier contenant plusieurs fichier .vc7
    renvoie la composante de vitesse selon x imagée par PIV
    à un instant donné.

    Parameters
    ----------
    dossier : - str
              - emplacement du dossier
    n : - int
        - numéro de la frame voulue

    Renvoie
    -------
    Un numpy array 2D de la taille égaille à la résolution
    de la vidéo contenant les composantes de la vitesse selon x
    sous la forme de float en chaque pixel
    '''
    
    return lv.read_set(dossier)[n][0].components['U0'][0]

def extraction_Uy(dossier,n):
    
    '''
    À partir d'un dossier contenant plusieurs fichier .vc7
    renvoie la composante de vitesse selon y imagée par PIV
    à un instant donné.

    Parameters
    ----------
    dossier : - str
              - emplacement du dossier
    n : - int
        - numéro de la frame voulue

    Renvoie
    -------
    Un numpy array 2D de la taille égaille à la résolution
    de la vidéo contenant les composantes de la vitesse selon y
    sous la forme de float en chaque pixel
    '''
    
    return lv.read_set(dossier)[n][0].components['V0'][0]

def extraction_Ec(dossier,n):
    
    '''
    À partir d'un dossier contenant plusieurs fichier .vc7
    renvoie le champ de l'énergie cinétique imagée par PIV
    à un instant donné. La fonction fait appel à 
    extraction_Ux() et extraction_Uy().

    Parameters
    ----------
    dossier : - str
              - emplacement du dossier
    n : - int
        - numéro de la frame voulue

    Renvoie
    -------
    Un numpy array 2D de la taille égaille à la résolution
    de la vidéo contenant en chaque point la valeur de l'énergie cinétique
    '''
    
    Ux = extraction_Ux(dossier, n)
    Uy = extraction_Uy(dossier, n)
    
    return 0.5*(np.square(Ux) + np.square(Uy))

def Ec_tot(dossier, n):
    
    '''
    Parameters
    ----------
    dossier : TYPE
        DESCRIPTION.
    n : TYPE
        DESCRIPTION.

    Returns
    -------
    None.
    '''
    
    return np.sum(extraction_Ec(dossier, n)[i_mur:, j_mur:])

def extraction_curl(dossier,n, s=3):
    
    '''
    Parameters
    ----------
    dossier : TYPE
        DESCRIPTION.
    n : TYPE
        DESCRIPTION.
    s : TYPE, optional
        DESCRIPTION. The default is 3.

    Returns
    -------
    TYPE
        DESCRIPTION.
    '''
    
    Ux = gaussian_filter(extraction_Ux(dossier, n), sigma = s, mode = 'constant')
    Uy = gaussian_filter(extraction_Uy(dossier, n), sigma = s, mode = 'constant')
    
    return rotationnel(Ux,Uy)

def extraction_Z(dossier, n, s=3):
    
    '''
    Parameters
    ----------
    dossier : TYPE
        DESCRIPTION.
    n : TYPE
        DESCRIPTION.

    Returns
    -------
    None.
    '''
    
    w = extraction_curl(dossier, n, s)
    
    return 0.5*np.square(w)

def Z_tot(dossier, n, s=3):
    
    '''
    Parameters
    ----------
    dossier : TYPE
        DESCRIPTION.
    n : TYPE
        DESCRIPTION.
    s : TYPE, optional
        DESCRIPTION. The default is 3.

    Returns
    -------
    None.
    '''
    
    return np.sum(extraction_Z(dossier, n, s)[i_mur:, j_mur:])
    
    
def N_frames(dossier):
    
    '''
    À partir d'un dossier contenant plusieurs fichier .vc7
    renvoie le nombre de frames

    Paramètres
    ----------
    dossier : - str
              - emplacement du dossier

    Renvoie
    -------
            - int
            - nombre de frames
    '''
    
    return len(lv.read_set(dossier))

#def Animation_Ec_w_Z(dossier):
    

# Lancement du programme

if __name__ == "__main__" :
    
    # Emplacement du mur
    i_mur = 60
    j_mur = 0
    
    # Caractéristiques de la vidéo
    
    r = 0.2 # Rapport px/m
    framerate = 4 # En fps
    
    # Choix du dossier
    
    dossier = "/home/rlqperri/Desktop/Acquisitions/20260610/mov_4/TR_PIV_MPd(4x32x32_75%ov)/PostProc/"
    
    
    plt.imshow(extraction_curl(dossier, 80), cmap = cmocean.cm.curl)
    plt.show()
    
    n_array = np.arange(0, N_frames(dossier))
    E = []
    Z = []
    
    for n in n_array:
        print(n)
        E.append(Ec_tot(dossier, int(n)))
        Z.append(Z_tot(dossier, int(n)))
        
    plt.plot(E)
    plt.show()
    plt.plot(Z)
    plt.show()