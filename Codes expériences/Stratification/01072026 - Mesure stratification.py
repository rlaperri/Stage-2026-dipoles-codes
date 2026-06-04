#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Jun  1 16:47:12 2026

@author: Robin Laperrière 

Mesure de la stratification faite le 1 Juin 2026
après avoir rempli la cuve

MESURES FAUSSES, VIDANGE DE TORICELLI
"""

import numpy as np
import matplotlib.pyplot as plt

# Graduations notées sur le tube en PVC (en cm)
z_graduation = np.arange(25,0,-1) 
z_graduation = np.append(z_graduation, 0.4)

# Offset du l'écart cellules-bout de la sonde

z = z_graduation + 0.9

# Mesures de conductimétrie (mS/cm), incertitudes faibles

sigma = np.array([9.16, 13.25, 16.95, 19.94, 23.71, 26.71, 29.47, 32.53,
                  35.32, 38.12, 40.81, 43.22, 45.56, 47.72, 49.86, 51.91, 
                  53.73, 55.51, 57.24, 58.69, 60.16, 61.55, 62.87, 63.93, 
                  64.64, 64.88])

# Conversion en densité

rho  = 998 + 0.62*sigma + 0.012*np.square(sigma)

# Calcul de la fréquence de Brunt-Väisälä

a1,a0 = np.polyfit(z*1e-2, rho, deg = 1)
N = np.sqrt(-(a1*9.81)/998)

# Plot 

plt.figure(figsize = (8,4))

plt.scatter(rho, z, color = 'indigo', marker = 'x', s = 60, label = 'mesures')


plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.xlabel(r'$\rho \, (kg/m^3)$', size = 13)
plt.ylabel(r'$z \, (cm)$', size = 13)
plt.grid()

plt.title(r"Stratification du 1 Juin 2026 (mesures fausses), $N \approx {:.2f}$ rad/s".format(N), 
          size = 16)
plt.show()