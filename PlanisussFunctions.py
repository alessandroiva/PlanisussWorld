import random
import copy
import time
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from PlanisussConstants import *
from PlanisussClasses import *

def update(w : World):
    #print("Updating...")
    # presentDay stores the current state of the world
    # use it to make computations and evaluate the next state of the world
    presentDay = w
    nextDay = w
    # store here the next state of the world (and so next state of each cell)
    

    # growing
    nextDay.Growing()
                
    # movement phase
    #check the most suitable neighbor cell, the rules will be different from erbast and carviz
    #herd: vegetob density (more is better), population of other cell (less carviz is better) (more Erbast is better), remember to not come back on the previous cell 
    #pride: population of erbast (more is better),less carviz is better, remember to not come back on the previous cell 
    #herd/pride decision:
        
        
    # Here we create two for loops in order that herds and pride decide before the movement of other animals. These are two separate events.
    nextDay.Decisions()
                
    #An Erbast will not move if he needs to increment its energy, but if there is not vegetob it will move with herd regardeless on its social attitude.
    nextDay.Movements()
                                
    # grazeRoutine(world)
    
    nextDay.GrazeRoutine()  
    
    # struggle phase                           
    
    nextDay.Struggle() 
 
    # fight phase - last blood match --> an entire pride will be eliminated 
    # victory is not deterministic, the probability depends on their energy
      
    nextDay.Fight()                
    #Hunt
    # prey: stronger Erbast in the cell --> bigger energy            
    nextDay.Hunt()
            
    #spawning
    nextDay.Spawning()
                    
    return nextDay


def days(periodtime : dict):
    year = 100
    decade = 10 * year
    century = 10 * decade
    result = 0
    result = result + periodtime['centuries']*century
    result = result + periodtime['decades']*decade
    result = result + periodtime['years']*year
    result = result + periodtime['days']
    return result