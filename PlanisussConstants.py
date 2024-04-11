#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 18:55:36 2023

@author: alessandro_iva
"""

# social groups
NEIGHBORHOOD = 1     # radius of the region that a social group can evaluate to decide the movement
NEIGHBORHOOD_E = 1   # radius of the region that a herd can evaluate to decide the movement
NEIGHBORHOOD_C = 1   #  radius of the region that a pride


MAX_HERD = 1000 # maximum numerosity of a herd
MAX_PRIDE = 100 # maximum numerosity of a pride
# individuals
MAX_ENERGY = 100 # maximum value of Energy
MAX_ENERGY_E = 100 # maximum value of Energy for Erbast
MAX_ENERGY_C = 100 # maximum value of Energy for Carviz

MAX_LIFE = 10000 # maximum value of Lifetime
MAX_LIFE_E = 10000 # maximum value of Lifetime for Erbast
MAX_LIFE_C = 10000 # maximum value of Lifetime for Carviz


AGING = 1 # energy lost each month
AGING_E = 1 # energy lost each month for Erbast
AGING_C = 1 # energy lost each month for Carviz
GROWING = 1 # Vegetob density that grows per day.

n_neighbors = 8 # if we consider a 3x3 matrix of neighbors, excluding the point (x,y) Worlde have 8 neighbors
max_neigh_density = n_neighbors*MAX_ENERGY

year = 100
decade = 10 * year
century = 10 * decade
