#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 13:45:07 2026

@author: robinou
"""

# Librairies

import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Données

## conductivité

'''
Mesurée par la sonde (voir cahier de labo). Une première incertitude
est estimée sur chaque mesure avec les fluctuation observées. 

L'appareil a une precision jusqu'au µS/cm, donc l'incertitude 
appareil peut être négligée ici.
'''

sigma = np.array([95.45, 92.92, 90.8, 86.5, 81.6, 77.2, 73.5, 69.55, 
                  67.4, 61.6, 53.6, 48.3, 42.9, 31.05, 25.23, 20.49,
                  11.28, 7.88, 1.47, 0.2, 0]) #mS/cm
u_sigma_exp = np.array([0.1, 0, 0.05, 1, 0.2, 0.2, 0.2, 0.05, 0.2, 
                        0.2, 0.1, 0.1, 0, 0.1, 0.1, 0.1, 0.1, 0.1, 
                        0.1,0.5, 0]) #mS/cm


## Densité

'''
Mesurée par le densimètre (voir cahier de labo)
'''

rho = np.array([1.1740, 1.1609, 1.1517, 1.1365, 1.1233, 1.1114, 1.1036, 
                1.0948, 1.0905, 1.0799, 1.0647, 1.0572, 1.0492, 1.0322, 
                1.0251, 1.0185, 1.0095, 1.0041, 0.9994, 0.9983, 0.998]) #g/cm3
u_rho_appareil = 0.001  #g/cm3, sur la notice

# Fit avec un polynome d'ordre 2

def polynome_deg2(sigma,a,b):
    return a*np.square(sigma) + b*sigma + 0.998

popt, pcov = curve_fit(polynome_deg2, xdata= sigma, ydata = rho, sigma = u_rho_appareil, 
                       p0 = [1e-5, 1e-4])
a,b = popt

# Graphique

plt.figure(figsize = (8,4))
plt.errorbar(x = sigma, y = rho, xerr = u_sigma_exp, yerr = u_rho_appareil, 
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
