#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Jun  4 09:15:37 2026

@author: Robin Laperrière

Données expérimentales sur les essais de jet de vortex par colorant
sur la semaine 1/07/2026 - 5/07/2026. Dans ce code, on regarde le 
comportement des vortex
"""

# Librairies
import numpy as np
import matplotlib.pyplot as plt

#Liste des expériences faites (indexées par les fichiers mov)

'''
Les résultats des expériences sont donnés par : 
    - Une liste "Parametres", où on décrit les débits et les temps 
    d'injection utilisés. Il s'agit d'une liste de listtes de deux
    éléments : 
        - Le premier élément étant le débit en mL/min
        - Le second étant le temps d'injection en seconde
        - None signifie qu'il s'agit juste de tests pour vérifier que 
        la caméra fonctionne
    - Une liste "Comportement" de str, où on décrit ce qu'il se passe :
        - "Pb_hauteur" signifie que la hauteur était vraiment trop mal réglée
        - "Col_dp" signifie qu'on forme bien un dipole et que celui ci touche
        la paroi mais qu'on a pas d'effets supplémentaires
        - "Pas_col_dp" signifie qu'on forme bien un dipole mais qu'il n'y a pas
        de collision
        - "Dev_dp" signifie qu'on a bien formé un dipole mais que celui si
        est devié dans sa trajectoire et ne collisionne pas
        - "Nvdp_pas_dp" signifie qu'on observe des nouveaux dipoles à la paroi mais
        que le dipole initial n'a pas eu le temps de se former avant collision
        - "Nvdp_dp" signifie qu'on a bien un dipole qui a eu le temps de se forme
        et qu'on observe des nouveaux dipoles
'''

## 2 Juin 2026
Parametres_0206 = np.array([[10,5], [10,5], [20,1], [20,10], [50,5], [5,10]])
Comportement_0206 = np.array(["Pb_hauteur", "Pb_hauteur", "Nvdp_pas_dp", "Nvdp_pas_dp", 
                     "Pas_col_dp"])

## 3 Juin 2026 
Parametres_0306 = np.array([[None, None], [1,1], [5,1], [20,1], [None, None],
                            [None, None], [20,2], [20,3], [20,4], [None, None], 
                            [None, None], [20,5], [100,1], [80,1], [80,1], [80,1],
                            [80,2], [40,2], [40,2], [None, None], [None, None],
                            [20,10], [40,5], [80,3], [80,1], [5,5], [60,5], 
                            [80,1], [100,0.8], [90,1], [100,1], [50,2], [60,2]])
Comportement_0306 = np.array([None, "Pas_col_dp", "Pas_col_dp", "Pas_col_dp", None, None,
                     "Col_dp", "Nvdp_pas_dp", "Nvdp_pas_dp", None, None, "Nvdp_pas_dp",
                     "Nvdp_pas_dp", "Pb_hauteur", "Nvdp_pas_dp", "Nvdp_pas_dp",
                     "Nvdp_pas_dp", "Nvdp_pas_dp", "Nvdp_dp", None, None, "Nvdp_pas_dp", 
                     "Nvdp_pas_dp", "Nvdp_pas_dp", "Dev_dp", "Pas_col_dp", "Nvdp_pas_dp",
                     "Dev_dp", "Dev_dp", "Nvdp_dp", "Nvdp_dp", "Nvdp_dp"])
i_recul_injecteur = 19 # Expérience à partir de laquelle on a reculé l'injecteur

# Resultats pour l'injecteur reculé au max (au 3 juin)

plt.figure(figsize = (8,4))

L_Pas_col_dp = np.where(Comportement_0306[i_recul_injecteur:] == "Pas_col_dp")[0] + i_recul_injecteur
plt.scatter(Parametres_0306[L_Pas_col_dp][:,0], 
         Parametres_0306[L_Pas_col_dp][:,1], label = "Dipôles formés, pas de collision")

L_Dev_dp = np.where(Comportement_0306[i_recul_injecteur:] == "Dev_dp")[0] + i_recul_injecteur
plt.scatter(Parametres_0306[L_Dev_dp][:,0], 
         Parametres_0306[L_Dev_dp][:,1], label = "Dipôles formés et deviés")

L_Nvdp_dp = np.where(Comportement_0306[i_recul_injecteur:] == "Nvdp_dp")[0] + i_recul_injecteur
plt.scatter(Parametres_0306[L_Nvdp_dp][:,0], 
         Parametres_0306[L_Nvdp_dp][:,1], label = "Dipôles formés, collision et nouveaux dipôles")

L_Nvdp_pas_dp = np.where(Comportement_0306[i_recul_injecteur:] == "Nvdp_pas_dp")[0] + i_recul_injecteur
plt.scatter(Parametres_0306[L_Nvdp_pas_dp][:,0], 
         Parametres_0306[L_Nvdp_pas_dp][:,1], label = "Dipôles pas formés, collision et nouveaux dipôles")

plt.grid()
plt.xlabel(r'$Q$ (mL/min)', size = 13)
plt.ylabel(r'$\delta t$ (s)', size = 13)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize = 10)
plt.title("Résultats au 3 juin pour la seringue écartée au max")
plt.show()