#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 16:45:06 2026

@author: Robin LAPERRIÈRE

Stratification du 10/06/2026
"""

import numpy as np
import matplotlib.pyplot as plt
# Graduations notées sur le tube en PVC (en cm)
z_graduation = np.arange(25,0,-1) 
z_graduation = np.append(z_graduation, 0.4)

# Offset du l'écart cellules-bout de la sonde

z = z_graduation + 0.9

# Mesures de conductimétrie (mS/cm), incertitudes faibles

sigma = np.array([4.40, 7.68, 11.28, 15.51, 18.18, 20.74, 23.42, 26.23, 28.79,
                  31.33, 33.71, 36.12, 38.64, 40.88, 43.19, 45.26, 47.51, 49.55,
                  51.58, 53.36, 55.33, 57.08, 58.96, 60.48, 61.66, 62.23])

# Conversion en densité

def calcul_rho(sigma):
    '''
    Convertit la conductivité (mS/cm) en densité (kg/m3) 
    à partir des mesures du 2 Juin 2026. VÉRIFIER AU PRÉALABLE
    L'ACCCORD AVEC CETTE LOI
    
    Arguments : 
    ----
    sigma : conductivité en mS/cm, nombre, liste ou np.array
    
    Renvoie :
    ----
    rho : densité en kg/m3, nombre, liste ou np.array
    '''
    
    return 998 + 0.47205116002752073*sigma + 0.014261625172364541*np.square(sigma)

rho  = calcul_rho(sigma)

# Calcul de la fréquence de Brunt-Väisälä

[a1,a0], cov = np.polyfit(z[2:-1]*1e-2, rho[2:-1], deg = 1, cov = True) 
u_a1 = cov[1,1]

'''
On exclut les quatre premiers et trois derniers points : 
    - Effets de la couche de mélange en surface
    - Effets du remplissage en profondeur
'''

N = np.sqrt(-(a1*9.81)/998)
u_N = np.sqrt((u_a1*9.81)/998)


# Plot 
b1, b0 = np.polyfit(rho[2:-2], z[2:-2], deg = 1) 

plt.figure(figsize = (8,4))

plt.scatter(rho, z, color = 'indigo', marker = 'x', s = 60, label = 'mesures')
plt.plot(rho, rho*b1 + b0, color = 'red', linestyle = 'dashed',
         label = 'Régression linéaire' , alpha = 0.6)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.xlabel(r'$\rho \, (kg/m^3)$', size = 13)
plt.ylabel(r'$z \, (cm)$', size = 13)
plt.grid()

plt.legend(fontsize = 14)
plt.title(r"Stratification du 10 Juin 2026, $N \approx {:.2f} \pm {:.2f} $ rad/s".format(N, u_N), 
          size = 16)
plt.show()

