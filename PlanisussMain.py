import random
import copy
import time
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors

from PlanisussConstants import *
from PlanisussClasses import *
from PlanisussFunctions import *


        

from matplotlib.animation import FuncAnimation



def main():
    ncol = 30 # x world
    nrow = 25 # y world
    initialspawn = [0.4,0.6] # probabilities of spawn | Position 0 for Erbasts, Position 1 for Carvizs
    period = {'centuries':0,'decades':0,'years':0,'days':1} # period of time of the world
    
   
    periodtime = days(period)
    simulationWorld = World(ncol,nrow,initialspawn)
    matrix = simulationWorld.viewMatrix()
    
    img, ax = plt.subplots()
    
    ax.imshow(matrix)
    

    # Create a colormap for the colors
    colors = ['blue', 'green']
    cmap = mcolors.ListedColormap(colors)
    # Plot the matrix with colors
    ax.imshow(matrix, cmap=cmap)
    
    # Set the grid
    #ax.set_xticks(np.arange(-0.5, ncol-1, 1))
    #ax.set_yticks(np.arange(-0.5, nrow-1, 1))
    #plt.grid()
    
    for i in range (periodtime):
        update(simulationWorld) 
                    
    plt.show()
    

    
        
    
    # animations:
    # use animation.FuncAnimation library function
    # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.animation.FuncAnimation.html
    # or use plt.pause() to pause the execution of the program for a given amount of time
    # non cambia essenzialmente nulla ma il primo e piu' elegante
    

    # each iter is a frame of the animation
    # richiesta ottimizazzione codice: troppo lento 

    





    


    

if __name__ == "__main__":
    main()




