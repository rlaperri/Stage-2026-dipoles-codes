#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 12:36:20 2026

@author: Robin Laperrière
Calibration de la sonde conductimétrique du 2 Juin 2026
"""

# Librairies

import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Données

## conductivité

'''
Mesurée par la sonde (voir cahier de labo). 

L'appareil a une precision jusqu'au µS/cm, donc l'incertitude 
appareil peut être négligée ici.
'''

sigma = np.array([96.86, 95.80, 94.55, 92.83, 90.53, 88.24, 86.00, 82.98,
                  79.58, 74.73, 69.28, 65.72, 57.57, 52.57, 46.20, 40.57, 
                  27.50, 20.22, 14.51, 11.02, 6.29, 1.95, 0.28]) #mS/cm



## Densité

'''
Mesurée par le densimètre (voir cahier de labo)
'''

rho = np.array([1.1941, 1.1820, 1.1734, 1.1642, 1.1546, 1.1456, 1.1375, 1.1277,
                1.1186, 1.1063, 1.0950, 1.0877, 1.0724, 1.0640, 1.0539, 1.0455,
                1.0278, 1.0188, 1.0122, 1.009, 1.0040, 0.9995, 0.9977]) #g/cm3
u_rho_appareil = 0.001  #g/cm3, sur la notice

# Fit avec un polynome d'ordre 2

def polynome_deg2(sigma,a,b):
    return a*np.square(sigma) + b*sigma + 0.998

popt, pcov = curve_fit(polynome_deg2, xdata= sigma, ydata = rho, sigma = u_rho_appareil, 
                       p0 = [1e-5, 1e-4])
a,b = popt

# Graphique

plt.figure(figsize = (8,4))
plt.errorbar(x = sigma, y = rho, yerr = u_rho_appareil, 
             linestyle = '', marker = 'x', color = 'indigo', markersize = 8,
             label = 'Données expérimentales')

plt.plot(sigma, polynome_deg2(sigma, a,b), label = 'Régression', color = 'blue', 
         linestyle = 'dashed')

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel(r'$\sigma$ $(mS/cm)$', size = 13)
plt.ylabel(r'$\rho$ $(g/cm^3)$', size = 13)

plt.legend(fontsize = 14)
plt.grid()
plt.show()

print("Coeff d'ordre 2")
print(a*1000)
print("Coeff d'ordre 1")
print(b*1000)
