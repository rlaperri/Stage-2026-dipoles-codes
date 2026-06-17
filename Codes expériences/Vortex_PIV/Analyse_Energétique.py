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
import matplotlib
import matplotlib.pyplot as plt # Graphiques
import numpy as np # Calculs
import os # Gestion des fichiers
from scipy.ndimage import gaussian_filter # Filtrage spatial gaussien

# Fonctions


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
    Uy : - array 2D numpy
         - champ de vitesse selon x en m/s
    '''
    
    return lv.read_set(dossier)[n][0].components['U0'][0]*r*framerate

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
    Uy : - array 2D numpy
         - champ de vitesse selon y en m/s
    
    Attention au signe moins.
    '''
    
    return (-1)*lv.read_set(dossier)[n][0].components['V0'][0]*r*framerate

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
    Ec : - array 2D numpy
         - champ d'énergie cinétique en m2/s2
    '''
    
    Ux = extraction_Ux(dossier, n)
    Uy = extraction_Uy(dossier, n)
    
    Ec = 0.5*(np.square(Ux) + np.square(Uy))
    
    return Ec

def Ec_tot(dossier, n):
    
    '''
    À partir d'un dossier contenant plusieurs fichier .vc7
    renvoie l'énergie cinétique totale intégrée spatialement. 
    La fonction fait appel à extraction_Ec.
    
    On se limite pour le calcul au domaine avant le mur, indexé
    par i_mur et j_mur.
    ----------
    dossier : - str
              - emplacement du dossier
    n : - int
        - numéro de la frame voulue

    Returns
    -------
    Ec_tot : - float
             - énergie cinétique totale intégrée 
    '''
    
    Ec_tot = np.sum(extraction_Ec(dossier, n)[i_mur:, j_mur:])
    
    return Ec_tot

def rotationnel(u,v):
    
    '''
    A partir d'un champ de vitesse 2D u et 
    v respectivement selon x et y, renvoie le rotationnel
    de ce champ (selon z)
    ----------
    u : - array 2D numpy
        - vitesse selon x en m/s
    v : - array 2D numpy
        - vitesse selon y en m/s

    Returns
    -------
    w : - array 2D numpy
        - le rotationnel du champ en m/s
    '''
        
    w = (v[:-1,1:]-v[:-1,:-1])/r + (u[1:,:-1]-u[:-1,:-1])/r
    
    return w

def extraction_vorticite(dossier,n, s=3):
    
    '''
    À partir d'un dossier contenant plusieurs fichier .vc7, 
    renvoie le champ de vorticité à partir du champ de vitesses.
    On applique un filtrage gaussien pour dériver. Au bords, les
    valeurs sont mises à zéro. La fonction fait appel à rotationnel().
    
    Arguments
    ----------
    dossier : - str
              - emplacement du dossier
    n : - int
        - numéro de la frame voulue
    s : - int
        - écart type en px du filtrage gaussien. Mis à 3 par défaut

    Renvoie
    -------
    TYPE
        DESCRIPTION.
    '''
    
    Ux = gaussian_filter(extraction_Ux(dossier, n), sigma = s, mode = 'constant')
    Uy = gaussian_filter(extraction_Uy(dossier, n), sigma = s, mode = 'constant')
    
    return rotationnel(Ux,Uy)

def extraction_Z(dossier, n, s=3):
    
    '''
    À partir d'un dossier contenant plusieurs fichier .vc7
    renvoie le champ de l'énergie cinétique imagée par PIV
    à un instant donné. La fonction fait appel à 
    extraction_vorticite().
    
    Arguments
    ----------
    dossier : - str
              - emplacement du dossier
    n : - int
        - numéro de la frame voulue

    Renvoie
    -------
    Z : - array numpy 2D
        - champ d'enstrophie à la frame donnée
    '''
    
    w = extraction_vorticite(dossier, n, s)
    Z = 0.5*np.square(w)
    
    return Z

def Z_tot(dossier, n, s=3):
    
    '''
    À partir d'un dossier contenant plusieurs fichier .vc7
    renvoie l'enstrophie totale intégrée spatialement. 
    La fonction fait appel à extraction_Ec.
    
    On se limite pour le calcul au domaine avant le mur, indexé
    par i_mur et j_mur.
    ----------
    dossier : - str
              - emplacement du dossier
    n : - int
        - numéro de la frame voulue
    s : - int
        - écart type du filtrage gaussien

    Returns
    -------
    Z_tot : - float
             - enstrophie totale intégrée 
    '''
    
    Z_tot =  np.sum(extraction_Z(dossier, n, s)[i_mur:, j_mur:])
    
    return Z_tot
    
    
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

def Animation_Ec_w_Z(dossier, nom, Q, dt, framerate):
    
    '''
    '''
    
    if not os.path.exists(nom):
        os.makedirs(nom)
    
    N = N_frames(dossier)
    n_array = np.arange(0, N)
    t_array = n_array/framerate
    
    Z = np.array([])
    E = np.array([])
    
    for n in n_array:
        E = np.append(E, Ec_tot(dossier, int(n)))
        Z = np.append(Z, Z_tot(dossier, int(n)))        
    
    data_name_length = int(np.floor(np.log10(N))) + 1
    
    for n in n_array:
        
        n = int(n)
        
        fig, axes = plt.subplots(2,3, figsize=(15,6))
        
        axes[1,0].plot(t_array,E, color = 'darkorange')
        axes[1,0].set_xlabel(r'$t$ (en $s$)', fontsize = 14)
        axes[1,0].set_ylabel(r'$E_{tot}$ (en $m^2 / s^2$)', fontsize = 14)
        axes[1,1].plot(t_array,Z, color = 'mediumblue')
        axes[1,1].set_xlabel(r'$t$ (en $s$)', fontsize = 14)
        axes[1,1].set_ylabel(r'$Z_{tot}$ (en $s^{-2}$)', fontsize = 14)
        
        im00 = axes[0,0].imshow(extraction_Ec(dossier, n), cmap = 'cmo.thermal',
                               aspect = 'equal')
        axes[0,0].axvline(i_mur, 0, 1, color='black', linestyle = 'dashed')
        cbar00 = fig.colorbar(im00, ax=axes[0,0])
        cbar00.set_label(r'$E$ (en $m^2 / s^2$)', fontsize = 16)

        im01 = axes[0,1].imshow(extraction_Z(dossier, n), cmap = 'coolwarm',
                               aspect = 'equal')
        axes[0,1].axvline(i_mur, 0, 1, color='black', linestyle = 'dashed')
        cbar01 = fig.colorbar(im01, ax=axes[0,1])
        cbar01.set_label(r'$Z$ (en $s^{-2}$)', fontsize = 16)
        
        im02 = axes[0,2].imshow(extraction_vorticite(dossier, n), cmap = 'cmo.curl',
                                aspect = 'equal')
        axes[0,2].axvline(i_mur, 0, 1, color='black', linestyle = 'dashed')
        cbar02 = fig.colorbar(im02, ax=axes[0,2])
        cbar02.set_label(r'$\omega$ (en $s^{-1}$)', fontsize = 16)
        
        axes[1,0].scatter(t_array[n],E[n], color = 'lightcoral')
        axes[1,1].scatter(t_array[n], Z[n], color = 'lightcoral')      
        
        axes[1, 2].text(0.2,0.5,
                        '{} \n'.format(nom)+r' $Q = {} mL/min$, $\delta t = {} s$'.format(Q,dt)+'\n'+'$t = {}s$'.format(t_array[n]),
                        fontsize = 16)

        fig.tight_layout()
        plt.savefig('{}/im{}.png'.format(nom,str(n).zfill(data_name_length)), dpi = 100) # Rajouter des zéros en début de ficheir
        plt.show()
        
    return None

def temps_collision(dossier, nom):
    
    if not os.path.exists(nom):
        os.makedirs(nom)
    
    D_maxmin = np.array([])
    N = N_frames(dossier)
    n_array = np.arange(0, N)
    t_array = n_array/framerate
    
    for n in n_array :
        
        n = int(n)
        
        w_n = extraction_vorticite(dossier, n)
        
        i_max, j_max = np.where(w_n==np.max(w_n))
        i_min, j_min = np.where(w_n==np.min(w_n))
        
        D_n = r*np.sqrt(np.square(i_max-i_min) + np.square(j_max-j_min))
        D_maxmin = np.append(D_maxmin, D_n)
        
    plt.plot(t_array, D_maxmin)
    plt.title(dossier)
    plt.savefig('{}/Dminmax.png'.format(nom), dpi = 100) # Rajouter des zéros en début de ficheir
    plt.show()
    
    return None

def pointage_Re(dossier,n):
    
    '''
    Changement de backend nécessaire pour faire marcher la fonction ginput. 
    Le backend qtagg permet de pouvoir interagir avec les figures en les 
    affichant dans un onglet à part, ce que la backend de base 
    (module://matplotlib_inline.backend_inline) ne permet pas
    '''
    
    matplotlib.use('qtagg') 
    
    # Extraction des vitesses
    
    Ux = extraction_Ux(dossier, n)
    Uy = extraction_Uy(dossier, n)
    U_norme = np.sqrt(np.square(Ux)+np.square(Uy))
    
    plt.imshow(U_norme, cmap = cmocean.cm.thermal,
                                aspect = 'equal')
    plt.title("{}, frame n°{}".format(dossier, n))
    plt.colorbar()
    
    print("Matplotlib plt backend: {}".format(matplotlib.get_backend()))

    
    print("Pointage de L")
    X1 = plt.ginput(2)
    print("Pointage de U")
    X2 = plt.ginput(1)
    
    plt.close()
    
    matplotlib.use('module://matplotlib_inline.backend_inline') # On repasse sur le backend de base
    
    L = r*np.sqrt(np.square(X1[0][0]-X1[1][0]) + np.square(X1[0][1] - X1[1][1]))
    print(L)
    U = U_norme[int(X2[0][0]), int(X2[0][1])]
    print(U)
        
    Re = U*L/nu
    print(Re)
    
    return Re



# Lancement du programme

if __name__ == "__main__" :
    
    # Paramètres physique
    
    nu = 1e-6 # m2/s, viscosité cinématique de l'eau
    
    # Emplacement du mur
    i_mur = 0
    j_mur = 0
    
    # Caractéristiques de la vidéo
    
    r = 1.4e-4 # Rapport m/px (à vérifier)
    
    # On passe de la dimensions des array en pixel
    r=r*8
    
    # Traitement des expériences du 10 juin

    Q_1006 = [10,20,20,40,40,30,30,30,40,20,10,10]
    dt_1006 = [5,5,3,1,3,1,3,5,5,1,1,3]
    
    n_max = [3,7,6,7,6,6,7,7,9,5,8,6]# frame à Z et E max
    
    Re_liste = np.array([np.float64(58.25818598804281), np.float64(261.8014853735046), np.float64(544.4480541307863), np.float64(447.87482865386477), np.float64(1234.5432737423744), np.float64(394.88745784468705), np.float64(979.0554750806876), np.float64(1020.1175911044234), np.float64(1430.1758410817656), np.float64(64.95017419515011), np.float64(10.762247392305705), np.float64(53.18649055543751)])
    Re_sort = np.sort(Re_liste)
    
    fig, axes = plt.subplots(1,2, figsize=(12,6))
    axes[0].set_xlabel(r'$t$ (en $s$)', fontsize = 14)
    axes[0].set_ylabel(r'$E_{tot}$ (en $m^2 / s^2$)', fontsize = 14)
    axes[1].set_xlabel(r'$t$ (en $s$)', fontsize = 14)
    axes[1].set_ylabel(r'$Z_{tot}$ (en $s^{-2}$)', fontsize = 14)
    
    colormap = plt.cm.coolwarm
    axes[0].set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, 12))))
    axes[1].set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, 12))))
    
    for Re in Re_sort:
            
        i = np.where(Re_liste==Re)[0][0]
        print(i)
        
        Q = Q_1006[i] # débit, en mL/min
        dt = dt_1006[i] # temps d'injection, en s
        
        if i<2:
            framerate = 2/10
        else:
            framerate = 4/10
        if i==0:
            dossier = "/home/rlqperri/Desktop/Acquisitions/20260610/mov_0/TR_PIV_MPd(4x32x32_75%ov)/SlidAvg L=10/"
            
        else: 
            dossier = "/home/rlqperri/Desktop/Acquisitions/20260610/mov_{}/TR_PIV_MPd(4x32x32_75%ov)/PostProc/SlidAvg L=10/".format(i)
            
        Z = np.array([])
        E = np.array([])
        
        N = N_frames(dossier)
        n_array = np.arange(0, N)
        t_array = n_array/framerate
        
        for n in n_array:
            E = np.append(E, Ec_tot(dossier, int(n)))
            Z = np.append(Z, Z_tot(dossier, int(n))) 
        
        axes[0].plot(t_array,E, label = r'$Re \approx {:.0f}$'.format(Re))
        axes[1].plot(t_array,Z, label = r'$Re \approx {:.0f}$'.format(Re))
        
    plt.legend()
    plt.show()
    