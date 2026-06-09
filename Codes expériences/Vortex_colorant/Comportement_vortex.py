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

#Liste des expériences faites

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
        - "Pas_nvdp_pas_dp" : signifie qu'on a une une collision d'un dipôle
        pas formé et que ce dernier ne forme pas de nouveau dipôle
        - "Col_jet" : signifie que on injecte encore du colorant quand la 
        structure que l'on envoie arrive sur le mur
'''

## 2 Juin 2026
Parametres_0206 = np.array([[10,5], [10,5], [20,1], [20,10], [50,5], [5,10]])
Comportement_0206 = np.array(["Pb_hauteur", "Pb_hauteur", "Pb_hauteur", "Nvdp_pas_dp", "Nvdp_pas_dp", 
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

## 4 Juin

Parametres_0406 = np.array([[None, None], [20,6], [20,8], [40,4], [40,4.5], 
                            [50,3], [50,4], [50,5], [50,4.5], [50, 4.3], [50,2.5],
                            [50,3.5], [60,3], [60,2], [60, 2.5], [60,1], [60, 1.5]])
Comportement_0406 = np.array([None, "Nvdp_dp", "Nvdp_dp", "Nvdp_dp", "Nvdp_dp",
                             "Nvdp_pas_dp", "Nvdp_pas_dp", "Nvdp_pas_dp", 
                             "Nvdp_pas_dp", "Nvdp_pas_dp", "Dev_dp", "Nvdp_pas_dp",
                             "Nvdp_pas_dp", "Nvdp_pas_dp", "Nvdp_pas_dp",
                             "Dev_dp", "Nvdp_dp"])

## 5 Juin

Parametres_0506 = np.array([[70,2], [70,1], [70,1.5], [70,3], [70,2], [80,2], 
                            [80,1.5], [90,2], [90,3], [5,10], [20,1], [20,2],
                            [20, 1.5],  [60,0.5], [80,0.4], [10,5], [80,0.625],
                            [100,0.625], [115,0.625], [115,0.3], [115,0.1],
                            [115,0.2], [11.5,2], [15,5], [5,15], [5,60], 
                            [5,150]])
Comportement_0506 = np.array(["Nvdp_dp", "Dev_dp", "Col_dp", "Nvdp_pas_dp", 
                              "Nvdp_pas_dp", "Nvdp_pas_dp", "Nvdp_pas_dp",
                              "Nvdp_dp", "Nvdp_pas_dp", "Pas_nvdp_pas_dp",
                              "Col_dp", "Pas_nvdp_pas_dp", "Pas_nvdp_pas_dp",
                              None, "Pas_nvdp_pas_dp", "Nvdp_pas_dp", 
                              "Nvdp_pas_dp", "Nvdp_pas_dp", "Nvdp_pas_dp",
                              "Col_dp", None, None, "Pas_nvdp_pas_dp", 
                              "Nvdp_pas_dp", "Col_jet", "Col_jet", "Col_jet"])
i_rotation_cuve = 9 # Expérience à partir de laquelle on a changé l'orientation de la cuve

# Résultats pour l'injecteur placé à la position initiale (2 juin et 3 juin matin)

plt.figure(figsize = (8,4))

## Résultats au 2 Juin

L_Pas_col_dp = np.where(Comportement_0206 == "Pas_col_dp")[0]
plt.scatter(Parametres_0206[L_Pas_col_dp][:,0], 
         Parametres_0206[L_Pas_col_dp][:,1], 
         label = "Dipôles formés, pas de collision", color = 'blue')

L_Dev_dp = np.where(Comportement_0206 == "Dev_dp")[0]
plt.scatter(Parametres_0206[L_Dev_dp][:,0], 
         Parametres_0206[L_Dev_dp][:,1], 
         label = "Dipôles formés et deviés", color = 'green')

L_Col_dp = np.where(Comportement_0206 == "Col_dp")[0]
plt.scatter(Parametres_0206[L_Col_dp][:,0], 
         Parametres_0206[L_Col_dp][:,1], 
         label = "Dipôles formés, collision seulement", color = 'tab:olive')

L_Nvdp_dp = np.where(Comportement_0206 == "Nvdp_dp")[0]
plt.scatter(Parametres_0206[L_Nvdp_dp][:,0], 
         Parametres_0206[L_Nvdp_dp][:,1], 
         label = "Dipôles formés, collision et nouveaux dipôles", color = 'orange')

L_Nvdp_pas_dp = np.where(Comportement_0206 == "Nvdp_pas_dp")[0]
plt.scatter(Parametres_0206[L_Nvdp_pas_dp][:,0], 
         Parametres_0206[L_Nvdp_pas_dp][:,1], 
         label = "Dipôles pas formés, collision et nouveaux dipôles", color = 'red')

## Résultats au 3 Juin

L_Pas_col_dp = np.where(Comportement_0306[:i_recul_injecteur] == "Pas_col_dp")[0]
plt.scatter(Parametres_0306[L_Pas_col_dp][:,0], 
         Parametres_0306[L_Pas_col_dp][:,1], 
         color = 'blue')

L_Dev_dp = np.where(Comportement_0306[:i_recul_injecteur] == "Dev_dp")[0]
plt.scatter(Parametres_0306[L_Dev_dp][:,0], 
         Parametres_0306[L_Dev_dp][:,1], 
         color = 'green')

L_Col_dp = np.where(Comportement_0306[:i_recul_injecteur] == "Col_dp")[0]
plt.scatter(Parametres_0306[L_Col_dp][:,0], 
         Parametres_0306[L_Col_dp][:,1], 
         color = 'tab:olive')

L_Nvdp_dp = np.where(Comportement_0306[:i_recul_injecteur] == "Nvdp_dp")[0]
plt.scatter(Parametres_0306[L_Nvdp_dp][:,0], 
         Parametres_0306[L_Nvdp_dp][:,1], 
         color = 'orange')

L_Nvdp_pas_dp = np.where(Comportement_0306[:i_recul_injecteur] == "Nvdp_pas_dp")[0]
plt.scatter(Parametres_0306[L_Nvdp_pas_dp][:,0], 
         Parametres_0306[L_Nvdp_pas_dp][:,1], 
         color = 'red')

## Plot

plt.grid()
plt.xlabel(r'$Q$ (mL/min)', size = 13)
plt.ylabel(r'$\delta t$ (s)', size = 13)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize = 10)
plt.title("Résultats pour la seringue en position intiale (2 et 3 juin)")
plt.show()

# Resultats pour l'injecteur reculé au max (au 3, 4 et 5 juin)

## Résultats au 3 Juin

plt.figure(figsize = (8,4))

L_Pas_col_dp = np.where(Comportement_0306[i_recul_injecteur:] == "Pas_col_dp")[0] + i_recul_injecteur
plt.scatter(Parametres_0306[L_Pas_col_dp][:,0], 
         Parametres_0306[L_Pas_col_dp][:,1], 
         label = "Dipôles formés, pas de collision", color = 'blue')

L_Dev_dp = np.where(Comportement_0306[i_recul_injecteur:] == "Dev_dp")[0] + i_recul_injecteur
plt.scatter(Parametres_0306[L_Dev_dp][:,0], 
         Parametres_0306[L_Dev_dp][:,1], 
         label = "Dipôles formés et deviés", color = 'green')

L_Col_dp = np.where(Comportement_0306[i_recul_injecteur:] == "Col_dp")[0] + i_recul_injecteur
plt.scatter(Parametres_0306[L_Col_dp][:,0], 
         Parametres_0306[L_Col_dp][:,1], 
         label = "Dipôles formés, collision seulement", color = 'tab:olive')

L_Nvdp_dp = np.where(Comportement_0306[i_recul_injecteur:] == "Nvdp_dp")[0] + i_recul_injecteur
plt.scatter(Parametres_0306[L_Nvdp_dp][:,0], 
         Parametres_0306[L_Nvdp_dp][:,1], 
         label = "Dipôles formés, collision et nouveaux dipôles", color = 'orange')

L_Nvdp_pas_dp = np.where(Comportement_0306[i_recul_injecteur:] == "Nvdp_pas_dp")[0] + i_recul_injecteur
plt.scatter(Parametres_0306[L_Nvdp_pas_dp][:,0], 
         Parametres_0306[L_Nvdp_pas_dp][:,1], 
         label = "Dipôles pas formés, collision et nouveaux dipôles", color = 'red')

## Résultats au 4 Juin

L_Pas_col_dp = np.where(Comportement_0406 == "Pas_col_dp")[0]
plt.scatter(Parametres_0406[L_Pas_col_dp][:,0], 
         Parametres_0406[L_Pas_col_dp][:,1], 
         color = 'blue')

L_Dev_dp = np.where(Comportement_0406 == "Dev_dp")[0]
plt.scatter(Parametres_0406[L_Dev_dp][:,0], 
         Parametres_0406[L_Dev_dp][:,1], 
         color = 'green')

L_Col_dp = np.where(Comportement_0406 == "Col_dp")[0]
plt.scatter(Parametres_0406[L_Col_dp][:,0], 
         Parametres_0406[L_Col_dp][:,1], 
         color = 'tab:olive')

L_Nvdp_dp = np.where(Comportement_0406 == "Nvdp_dp")[0]
plt.scatter(Parametres_0406[L_Nvdp_dp][:,0], 
         Parametres_0406[L_Nvdp_dp][:,1], 
         color = 'orange')

L_Nvdp_pas_dp = np.where(Comportement_0406 == "Nvdp_pas_dp")[0]
plt.scatter(Parametres_0406[L_Nvdp_pas_dp][:,0], 
         Parametres_0406[L_Nvdp_pas_dp][:,1], 
         color = 'red')

## Résultats au 5 Juin

L_Pas_col_dp = np.where(Comportement_0506[:i_rotation_cuve] == "Pas_col_dp")[0]
plt.scatter(Parametres_0506[L_Pas_col_dp][:,0], 
         Parametres_0506[L_Pas_col_dp][:,1], 
         color = 'blue')

L_Dev_dp = np.where(Comportement_0506[:i_rotation_cuve] == "Dev_dp")[0]
plt.scatter(Parametres_0506[L_Dev_dp][:,0], 
         Parametres_0506[L_Dev_dp][:,1], 
         color = 'green')

L_Col_dp = np.where(Comportement_0506[:i_rotation_cuve] == "Col_dp")[0]
plt.scatter(Parametres_0506[L_Col_dp][:,0], 
         Parametres_0506[L_Col_dp][:,1], 
         color = 'tab:olive')

L_Nvdp_dp = np.where(Comportement_0506[:i_rotation_cuve] == "Nvdp_dp")[0]
plt.scatter(Parametres_0506[L_Nvdp_dp][:,0], 
         Parametres_0506[L_Nvdp_dp][:,1], 
         color = 'orange')

L_Nvdp_pas_dp = np.where(Comportement_0506[:i_rotation_cuve]== "Nvdp_pas_dp")[0]
plt.scatter(Parametres_0506[L_Nvdp_pas_dp][:,0], 
         Parametres_0506[L_Nvdp_pas_dp][:,1], 
         color = 'red')

## Plot

plt.grid()
plt.xlabel(r'$Q$ (mL/min)', size = 13)
plt.ylabel(r'$\delta t$ (s)', size = 13)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize = 10)
plt.title("Résultats au 3, 4 et 5 juin pour la seringue écartée au max")
plt.show()

# Resultats pour la cuve tournée dans l'autre sens (5 juin)

plt.figure(figsize = (8,4))

L_Col_dp = np.where(Comportement_0506[i_rotation_cuve:] == "Col_dp")[0] + i_rotation_cuve
plt.scatter(Parametres_0506[L_Col_dp][:,0], 
         Parametres_0506[L_Col_dp][:,1], 
         label = "Dipôles formés, collision seulement", color = 'tab:olive')

L_Nvdp_pas_dp = np.where(Comportement_0506[i_rotation_cuve:]== "Nvdp_pas_dp")[0] + i_rotation_cuve
plt.scatter(Parametres_0506[L_Nvdp_pas_dp][:,0], 
         Parametres_0506[L_Nvdp_pas_dp][:,1], 
         label = "Dipôles pas formés, collision et nouveaux dipôles", color = 'red')

L_Pas_nvdp_pas_dp = np.where(Comportement_0506[i_rotation_cuve:]== "Pas_nvdp_pas_dp")[0] + i_rotation_cuve
plt.scatter(Parametres_0506[L_Pas_nvdp_pas_dp][:,0], 
         Parametres_0506[L_Pas_nvdp_pas_dp][:,1], 
         label = "Dipôles pas formés, collision et pas de nouveaux dipôles", color = 'magenta')

L_Col_jet = np.where(Comportement_0506[i_rotation_cuve:]== "Col_jet")[0] + i_rotation_cuve
plt.scatter(Parametres_0506[L_Col_jet][:-2,0], 
         Parametres_0506[L_Col_jet][:-2,1], 
         label = "Jet turbulent", color = 'purple')
## Plot

plt.grid()
plt.xlabel(r'$Q$ (mL/min)', size = 13)
plt.ylabel(r'$\delta t$ (s)', size = 13)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize = 10)
plt.title("Résultats au 5 juin pour la cuve tournée dans l'autre sens (problèmes de hauteur ?)")
plt.show()