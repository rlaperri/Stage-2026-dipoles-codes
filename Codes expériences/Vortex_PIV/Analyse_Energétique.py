#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:50:08 2026

@author: Robin LAPERRIÈRE

Là il faudra mettre une description du code
s'il te plaît
"""

# Importation des librairres

import cmocean  # Jolies colormap
import lvpyio as lv  # Extraction des .vc7
import matplotlib
import matplotlib.pyplot as plt  # Graphiques
import numpy as np  # Calculs
import os  # Gestion des fichiers
from scipy.ndimage import gaussian_filter  # Filtrage spatial gaussien

# Fonctions


def extraction_Ux(dossier, n, framerate):
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


def extraction_Uy(dossier, n, framerate):
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


def extraction_Ec(dossier, n, framerate):
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

    Ux = extraction_Ux(dossier, n, framerate)
    Uy = extraction_Uy(dossier, n, framerate)

    Ec = 0.5*(np.square(Ux) + np.square(Uy))

    return Ec


def Ec_tot(dossier, n, framerate):
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

    Ec_tot = np.sum(extraction_Ec(dossier, n, framerate)[i_mur:, j_mur:])

    return Ec_tot


def rotationnel(u, v):
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

    w = (v[:-1, 1:]-v[:-1, :-1])/r + (u[1:, :-1]-u[:-1, :-1])/r

    return w


def extraction_vorticite(dossier, n, framerate, s=3):
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

    Ux = gaussian_filter(extraction_Ux(dossier, n, framerate), sigma=s, mode='constant')
    Uy = gaussian_filter(extraction_Uy(dossier, n, framerate), sigma=s, mode='constant')

    return rotationnel(Ux, Uy)


def extraction_Z(dossier, n, framerate, s=3):
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

    w = extraction_vorticite(dossier, n, framerate, s)
    Z = 0.5*np.square(w)

    return Z


def Z_tot(dossier, n, framerate, s=3):
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

    Z_tot = np.sum(extraction_Z(dossier, n, framerate, s)[i_mur:, j_mur:])

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


def D_minmax(dossier, nom, framerate):

    if not os.path.exists(nom):
        os.makedirs(nom)

    D_maxmin = np.array([])
    N = N_frames(dossier)
    n_array = np.arange(0, N)
    t_array = n_array/framerate

    for n in n_array:

        n = int(n)

        w_n = extraction_vorticite(dossier, n, framerate)

        i_max, j_max = np.where(w_n == np.max(w_n))
        i_min, j_min = np.where(w_n == np.min(w_n))

        D_n = r*np.sqrt(np.square(i_max-i_min) + np.square(j_max-j_min))
        D_maxmin = np.append(D_maxmin, D_n)

    plt.plot(t_array, D_maxmin)
    plt.title(dossier)
    # Rajouter des zéros en début de ficheir
    plt.savefig('{}/Dminmax.png'.format(nom), dpi=100)
    plt.show()

    return None


def Re_Injection(Q):
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

    Q_SI = 1/(1e6*60)*Q  # en m3/s
    ReI = (4*Q_SI)/(np.pi*D*nu)

    return ReI


def Re_Vortex(Q, dt, t):
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

    ReI = Re_Injection(Q)
    # Nombre de Reynolds du Vortex
    ReV = 1.1e-3*np.power(ReI, 3/2)*np.power(dt, 1)*np.power(t, 1/2)
    # Bornes de l'intervalle de confiance
    # ReV_min, ReV_max = np.power(ReI,3/2)*dt*np.power(t,-1/2-0.15), np.power(ReI,3/2)*dt*np.power(t,-1/2+0.15)

    return ReV


def pointage_Re(dossier, n, framerate):
    '''
    Changement de backend nécessaire pour faire marcher la fonction ginput. 
    Le backend qtagg permet de pouvoir interagir avec les figures en les 
    affichant dans un onglet à part, ce que la backend de base 
    (module://matplotlib_inline.backend_inline) ne permet pas
    '''

    matplotlib.use('qtagg')

    # Extraction des vitesses

    Ux = extraction_Ux(dossier, n, framerate)
    Uy = extraction_Uy(dossier, n, framerate)
    U_norme = np.sqrt(np.square(Ux)+np.square(Uy))

    plt.imshow(U_norme, cmap=cmocean.cm.thermal,
               aspect='equal')
    plt.title("{}, frame n°{}".format(dossier, n))
    plt.colorbar()

    print("Matplotlib plt backend: {}".format(matplotlib.get_backend()))

    print("Pointage de L")
    X1 = plt.ginput(2)
    print("Pointage de U")
    X2 = plt.ginput(1)

    plt.close()

    # On repasse sur le backend de base
    matplotlib.use('module://matplotlib_inline.backend_inline')

    L = r*np.sqrt(np.square(X1[0][0]-X1[1][0]) +
                  np.square(X1[0][1] - X1[1][1]))
    print(L)
    U = U_norme[int(X2[0][0]), int(X2[0][1])]
    print(U)

    Re = U*L/nu
    print(Re)

    return Re

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
        E = np.append(E, Ec_tot(dossier, int(n), framerate))
        Z = np.append(Z, Z_tot(dossier, int(n), framerate))

    data_name_length = int(np.floor(np.log10(N))) + 1

    for n in n_array:

        n = int(n)

        fig, axes = plt.subplots(2, 3, figsize=(6, 6))

        axes[1, 0].scatter(t_array, E, color='darkorange')
        axes[1, 0].set_xlabel(r'$t$ (en $s$)', fontsize=14)
        axes[1, 0].set_ylabel(r'$E_{tot}$ (en $m^2 / s^2$)', fontsize=14)
        axes[1, 1].scatter(t_array, Z, color='mediumblue')
        axes[1, 1].set_xlabel(r'$t$ (en $s$)', fontsize=14)
        axes[1, 1].set_ylabel(r'$Z_{tot}$ (en $s^{-2}$)', fontsize=14)

        im00 = axes[0, 0].imshow(extraction_Ec(dossier, n, framerate), cmap='cmo.thermal',
                                 aspect='equal')
        axes[0, 0].axvline(i_mur, 0, 1, color='black', linestyle='dashed')
        cbar00 = fig.colorbar(im00, ax=axes[0, 0])
        cbar00.set_label(r'$E$ (en $m^2 / s^2$)', fontsize=16)

        im01 = axes[0, 1].imshow(extraction_Z(dossier, n, framerate), cmap='coolwarm',
                                 aspect='equal')
        axes[0, 1].axvline(i_mur, 0, 1, color='black', linestyle='dashed')
        cbar01 = fig.colorbar(im01, ax=axes[0, 1])
        cbar01.set_label(r'$Z$ (en $s^{-2}$)', fontsize=16)

        im02 = axes[0, 2].imshow(extraction_vorticite(dossier, n, framerate), cmap='cmo.curl',
                                 aspect='equal')
        axes[0, 2].axvline(i_mur, 0, 1, color='black', linestyle='dashed')
        cbar02 = fig.colorbar(im02, ax=axes[0, 2])
        cbar02.set_label(r'$\omega$ (en $s^{-1}$)', fontsize=16)

        axes[1, 0].scatter(t_array[n], E[n], color='lightcoral')
        axes[1, 1].scatter(t_array[n], Z[n], color='lightcoral')

        axes[1, 2].text(0.2, 0.5,
                        '{} \n'.format(nom)+r' $Q = {} mL/min$, $\delta t = {} s$'.format(
                            Q, dt)+'\n'+'$t = {}s$'.format(t_array[n]),
                        fontsize=16)

        fig.tight_layout()
        # Rajouter des zéros en début de ficheir
        plt.savefig('{}/im{}.png'.format(nom,
                    str(n).zfill(data_name_length)), dpi=100)
        plt.show()

    return None

def verification_2D(dossier, nom, Q, dt, framerate):

    if not os.path.exists(nom):
        os.makedirs(nom)
    
    N = N_frames(dossier)
    n_array = np.arange(0, N)
    t_array = n_array/framerate
    
    Z = np.array([])
    E = np.array([])
    
    for n in n_array:
        E = np.append(E, Ec_tot(dossier, int(n), framerate))
        Z = np.append(Z, Z_tot(dossier, int(n), framerate))
        
    dtE = (E[1:]-E[:-1])*framerate
        
    fig, axes = plt.subplots(2, 3, figsize=(15, 6))
    
    axes[0,0].scatter(t_array[:-1], dtE, color = 'red', label = r'$d_t E$', s = 10)
    axes[0,0].plot(t_array[:-1], dtE, color = 'red', alpha = 0.4)
    axes[0,0].scatter(t_array, -2*nu*Z, color = 'teal', label = r'$- 2\nu Z$', s = 10)
    axes[0,0].plot(t_array, -2*nu*Z, color = 'teal', alpha = 0.4)
    axes[0,0].set_xlabel(r'$t$ (en $s$)', fontsize=14)
    axes[0,0].legend()
    axes[0,0].grid()
    
    axes[0,1].scatter(t_array[:-1], np.abs(1 + 2*nu*Z[:-1]/dtE), color = 'green', s = 10)
    axes[0,1].axhline(y = 1, label = r'$\left|1 + \frac{2\nu Z_{tot}}{d_t E_{tot}} \right|  = 1$', 
                      linestyle = 'dashed', color = 'olivedrab', alpha = 0.8)
    axes[0,1].plot(t_array[:-1], np.abs(1 + 2*nu*Z[:-1]/dtE), color = 'green', alpha = 0.4)
    axes[0,1].set_xlabel(r'$t$ (en $s$)', fontsize=14)
    axes[0,1].set_ylabel(r'$\left|1 + \frac{2\nu Z_{tot}}{d_t E_{tot}} \right|$ (en $m^2 / s$)', fontsize=14)
    axes[0,1].grid()
    axes[0,1].legend()
    
    axes[0,2].text(0.2, 0.5,
            '{} \n'.format(nom)+r' $Q = {} mL/min$, $\delta t = {} s$'.format(
                Q, dt)+'\n'+'$t = {}s$'.format(t_array[n]),
            fontsize=16)
    
    axes[1, 0].scatter(t_array, E, color='darkorange', s = 10)
    axes[1, 0].plot(t_array, E, color='darkorange', alpha = 0.4)
    axes[1, 0].set_xlabel(r'$t$ (en $s$)', fontsize=14)
    axes[1, 0].set_ylabel(r'$E_{tot}$ (en $m^2 / s^2$)', fontsize=14)
    axes[1, 0].grid()
    
    axes[1, 1].scatter(t_array, Z, color='mediumblue', s = 10)
    axes[1, 1].plot(t_array, Z, color='mediumblue', alpha = 0.4)
    axes[1, 1].set_xlabel(r'$t$ (en $s$)', fontsize=14)
    axes[1, 1].set_ylabel(r'$Z_{tot}$ (en $s^{-2}$)', fontsize=14)
    axes[1, 1].grid()
    
    fig.tight_layout()
    # Rajouter des zéros en début de ficheir
    plt.savefig('{}/dtE_Z.png'.format(nom), dpi=200)
    plt.show()

    return None

def E_Z_log(dossier, nom, Q, dt, framerate, i_min_debut, i_max_debut, i_min_fin):

    if not os.path.exists(nom):
        os.makedirs(nom)
    
    N = N_frames(dossier)
    n_array = np.arange(0, N)
    t_array = n_array/framerate
    
    
    t_log_debut = np.log(t_array[i_min_debut:i_max_debut+1])
    t_log_fin = np.log(t_array[i_min_fin:])
    
    Z = np.array([])
    E = np.array([])
    
    for n in n_array:
        E = np.append(E, Ec_tot(dossier, int(n), framerate))
        Z = np.append(Z, Z_tot(dossier, int(n), framerate))
        
    E_log_debut = np.log(E[i_min_debut:i_max_debut+1])
    Z_log_debut = np.log(Z[i_min_debut:i_max_debut+1])
    
    E_log_fin = np.log(E[i_min_fin:])
    Z_log_fin = np.log(Z[i_min_fin:])
    
    aE_debut,bE_debut = np.polyfit(t_log_debut,E_log_debut,1)
    aZ_debut,bZ_debut = np.polyfit(t_log_debut,Z_log_debut,1)
    
    aE_fin,bE_fin = np.polyfit(t_log_fin,E_log_fin,1)
    aZ_fin,bZ_fin = np.polyfit(t_log_fin,Z_log_fin,1)
        
    fig, axes = plt.subplots(1,3, figsize=(18, 6))
    
    axes[0].set_xscale('log')
    axes[0].set_yscale('log')
    axes[0].scatter(t_array, E, color='darkorange', s = 10, marker = 'x')
    axes[0].plot(t_array, E, color='darkorange', alpha = 0.4)
    axes[0].plot(t_array[i_min_debut:i_max_debut+1], np.exp(aE_debut*t_log_debut+bE_debut+0.3), color='chocolate', alpha = 1, 
                 label = 'pente {:.2f}'.format(aE_debut), linestyle = 'dashed')
    axes[0].plot(t_array[i_min_fin:], np.exp(aE_fin*t_log_fin+bE_fin+0.3), color='red', alpha = 1, 
                 label = 'pente {:.2f}'.format(aE_fin), linestyle = 'dashed')
    axes[0].set_xlabel(r'$t$ (en $s$)', fontsize=14)
    axes[0].set_ylabel(r'$E_{tot}$ (en $m^2 / s^2$)', fontsize=14)
    axes[0].legend()
    axes[0].grid()
    
    axes[1].set_xscale('log')
    axes[1].set_yscale('log')
    axes[1].scatter(t_array, Z, color='mediumblue', s = 10, marker = 'x')
    axes[1].plot(t_array, Z, color='mediumblue', alpha = 0.4)
    axes[1].plot(t_array[i_min_debut:i_max_debut+1], np.exp(aZ_debut*t_log_debut+bZ_debut+0.3), color='purple', alpha = 1, 
                 label = 'pente {:.2f}'.format(aZ_debut), linestyle = 'dashed')
    axes[1].plot(t_array[i_min_fin:], np.exp(aZ_fin*t_log_fin+bZ_fin+0.3), color='teal', alpha = 1, 
                 label = 'pente {:.2f}'.format(aZ_fin), linestyle = 'dashed')
    axes[1].set_xlabel(r'$t$ (en $s$)', fontsize=14)
    axes[1].set_ylabel(r'$Z_{tot}$ (en $s^{-2}$)', fontsize=14)
    axes[1].legend()
    axes[1].grid()
    
    axes[2].text(0.2, 0.5,
            '{} \n'.format(nom)+r' $Q = {} mL/min$, $\delta t = {} s$'.format(
                Q, dt)+'\n'+'$t = {}s$'.format(t_array[n]),
            fontsize=16)
    
    fig.tight_layout()
    # Rajouter des zéros en début de ficheir
    plt.savefig('{}/E_Z_log.png'.format(nom), dpi=200)
    plt.show()

    return None
    

# Lancement du programme
if __name__ == "__main__":

    # Paramètres physique

    D = 0.5e-3  # Diamètre de l'aiguille utilisée (m)
    nu = 1e-6  # m2 s, viscosité cinématique de l'eau

    # Emplacement du mur
    i_mur = 0
    j_mur = 0

    # Caractéristiques de la vidéo

    r = 1.4e-4  # Rapport m/px (à vérifier)
    framerate_1006 = np.zeros(12)
    framerate_1006[:2] = 2/10
    framerate_1006[2:] = 4/10

    # On passe de la dimensions des array en pixel
    r = r*8

    # Traitement des expériences du 10 juin

    Q_1006 = np.array([10, 20, 20, 40, 40, 30, 30, 30, 40, 20, 10, 10])
    dt_1006 = np.array([5, 5, 3, 1, 3, 1, 3, 5, 5, 1, 1, 3])
    
    i_debut_liste = np.array([[1,3],[1,3],[1,4],[2,6],[1,5],[1,4],[2,6],[1,6],
                              [3,8],[2,5],[6,7],[2,5]])
    i_fin_liste = np.array([5,15,15,15,15,15,15,15,15,15,15,15])
    
    for i in range(12):

        if i == 0:
            dossier = "/home/rlqperri/Desktop/Acquisitions/20260610/mov_0/TR_PIV_MPd(4x32x32_75%ov)/SlidAvg L=10/"

        else:
            dossier = "/home/rlqperri/Desktop/Acquisitions/20260610/mov_{}/TR_PIV_MPd(4x32x32_75%ov)/PostProc/SlidAvg L=10/".format(i)
        
        Q = Q_1006[i]  # débit, en mL/min
        dt = dt_1006[i]  # temps d'injection, en s
        framerate = framerate_1006[i]
        nom = '10_06/mov_{}'.format(i)
        
        i_min_debut = i_debut_liste[i][0]
        i_max_debut = i_debut_liste[i][1]
        i_min_fin = i_fin_liste[i]
        E_Z_log(dossier, nom, Q, dt, framerate, i_min_debut, i_max_debut, i_min_fin)
    
    '''
    # frame à Z et E max
    n_max_1006 = np.array([3, 7, 6, 7, 6, 6, 7, 7, 9, 5, 8, 6])
    
    for i in range(12):

        if i == 0:
            dossier = "/home/rlqperri/Desktop/Acquisitions/20260610/mov_0/TR_PIV_MPd(4x32x32_75%ov)/SlidAvg L=10/"

        else:
            dossier = "/home/rlqperri/Desktop/Acquisitions/20260610/mov_{}/TR_PIV_MPd(4x32x32_75%ov)/PostProc/SlidAvg L=10/".format(i)
        
        Q = Q_1006[i]  # débit, en mL/min
        dt = dt_1006[i]  # temps d'injection, en s
        framerate = framerate_1006[i]
        nom = '10_06/mov_{}'.format(i)
        verification_2D(dossier, nom, Q, dt, framerate)
    '''
    '''
    ReI = Re_Injection(Q_1006)
    Re_liste = []
    
    for i in range(12):

        if i == 0:
            dossier = "/home/rlqperri/Desktop/Acquisitions/20260610/mov_0/TR_PIV_MPd(4x32x32_75%ov)/SlidAvg L=10/"

        else:
            dossier = "/home/rlqperri/Desktop/Acquisitions/20260610/mov_{}/TR_PIV_MPd(4x32x32_75%ov)/PostProc/SlidAvg L=10/".format(i)
        
        framerate = framerate_1006[i]
        n = int(n_max_1006[i])
        Re_liste.append(pointage_Re(dossier, n))
        
    Re_sort = np.sort(Re_liste)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].set_xlabel(r'$t$ (en $s$)', fontsize=14)
    axes[0].set_ylabel(r'$E_{tot}$ (en $m^2 / s^2$)', fontsize=14)
    axes[1].set_xlabel(r'$t$ (en $s$)', fontsize=14)
    axes[1].set_ylabel(r'$Z_{tot}$ (en $s^{-2}$)', fontsize=14)

    colormap = plt.cm.coolwarm
    axes[0].set_prop_cycle(plt.cycler(
        'color', plt.cm.jet(np.linspace(0, 1, 12))))
    axes[1].set_prop_cycle(plt.cycler(
        'color', plt.cm.jet(np.linspace(0, 1, 12))))
    

    for Re in Re_sort:

        i = np.where(Re_liste == Re)[0][0]
        print(i)

        Q = Q_1006[i]  # débit, en mL/min
        dt = dt_1006[i]  # temps d'injection, en s

        framerate = framerate_1006[i]

        if i == 0:
            dossier = "/home/rlqperri/Desktop/Acquisitions/20260610/mov_0/TR_PIV_MPd(4x32x32_75%ov)/SlidAvg L=10/"

        else:
            dossier = "/home/rlqperri/Desktop/Acquisitions/20260610/mov_{}/TR_PIV_MPd(4x32x32_75%ov)/PostProc/SlidAvg L=10/".format(
                i)

        Z = np.array([])
        E = np.array([])

        N = N_frames(dossier)
        n_array = np.arange(0, N)
        t_array = n_array/framerate

        for n in n_array:
            E = np.append(E, Ec_tot(dossier, int(n), framerate))
            Z = np.append(Z, Z_tot(dossier, int(n), framerate))

        axes[0].plot(
            t_array, E, label=r'$Re_V \approx {:.0f}, Re_I \approx {:.0f}$'.format(Re, ReI[i]))
        axes[1].plot(
            t_array, Z, label=r'$Re_V \approx {:.0f}, Re_I \approx {:.0f}$'.format(Re, ReI[i]))

    plt.title(
        r"Mesures du 10/06, $Re_V$ : repointage, $Re_I$ : Reynolds d'Injection")
    plt.legend()
    plt.show()
    '''