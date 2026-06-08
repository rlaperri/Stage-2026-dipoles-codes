#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 10:53:41 2026

@author: Robin Laperrière

Mesure de la stratification faite le 8 Juin 2026
avant de vidanger la cuve

BESOIN PEUT-ÊTRE DE RECALIBRER LA SONDE ?
"""

import numpy as np
import matplotlib.pyplot as plt
# Graduations notées sur le tube en PVC (en cm)
z_graduation = np.arange(25,0,-1) 
z_graduation = np.append(z_graduation, 0.4)

# Offset du l'écart cellules-bout de la sonde

z = z_graduation + 0.9

# Mesures de conductimétrie (mS/cm), incertitudes faibles

sigma_0207 = np.array([0.01, 2.93, 9.70, 11.61, 15.27, 18.16, 21.41, 24.89, 27.98,
                  30.88, 33.94, 36.69, 39.52, 41.99, 44.48, 46.80, 48.87, 51.06,
                  52.83, 54.47, 56.25, 57.85, 59.40, 60.83, 62.23, 63.02])


sigma_0807 = np.array([0.01, 19.18, 19.26, 20.06, 21.29, 23.40, 25.77, 
                  28.20, 30.69, 33.60, 36.30, 38.68, 41.14, 43.30, 
                  45.71, 47.96, 49.84, 51.71, 53.29, 54.96, 56.46, 
                  57.68, 58.59, 59.28, 59.72])

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

rho_0207  = calcul_rho(sigma_0207)
rho_0807 = calcul_rho(sigma_0807)


# Plot 
plt.figure(figsize = (8,4))

plt.scatter(rho_0207, z, marker = 'x', s = 60, label = '2/06/2026')
plt.scatter(rho_0807, z[1:], marker = 'x', s = 60, label = '8/06/2026')


plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.xlabel(r'$\rho \, (kg/m^3)$', size = 13)
plt.ylabel(r'$z \, (cm)$', size = 13)
plt.grid()

plt.legend(fontsize = 14)
plt.title(r"Stratification de la deuxième semaine", 
          size = 16)
plt.show()

