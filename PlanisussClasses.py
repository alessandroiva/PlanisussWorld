import random
import copy
import time
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from PlanisussConstants import *

class Animal: #since Carviz and Erbast have same properties
    def __init__(self,location): 
        self.energy = random.randint(80, 100)
        self.lifetime = MAX_LIFE
        self.age = random.randint(0, MAX_LIFE)
        self.s_attitude = random.random()
        self.memory = 0 # when it's born, no memory
        self.location = location
    def getLocation(self):
        return self.location
    
    def setLocation (self,location):
        self.location = location
    
    def getEnergy(self):
        return self.energy
    def spawning(self):
        if isinstance(self, Erbast):
            born1 = Erbast(self.location)
            born2 = Erbast(self.location)
        elif isinstance(self, Carviz):
            born1 = Carviz(self.location)
            born2 = Carviz(self.location)
        en = self.energy / 2 
        born1.s_attitude = en
        born2.s_attitude = en
        born1.s_attitude = self.s_attitude
        born2.s_attitude = self.s_attitude
   
        return born1,born2

        
class Carviz (Animal):
    pass

class Erbast (Animal):
    def graze(self,cell):
        self.energy += 1
        cell.decreaseVegetob()
        
        
class Pride:
    def __init__(self,pop_pride : list):
        self.pop_pride = pop_pride
        self.memory = []
        for i in self.pop_pride:
            i = i.memory
            if i not in self.memory:
                self.memory.append(i)
    def getLocation(self):
        location = self.pop_pride[0].location
        return location
    
    def deletemember (self,i):
        self.pop_pride.remove(i)
    
    def addmember(self,i):
        self.pop_pride.append(i)
        i.setLocation(self.getLocation())
    
    def addPopulationPride (self,population : list):
        self.pop_pride.extend(population)
    
    def getaverageEnergy(self):
        energies = [c.energy for c in self.pop_pride]  
        return sum(energies)/len(self.pop_pride)
    
    def getaverageSocialAttitude(self):
        socialattitudes = [c.s_attitude for c in self.pop_pride]
        sumsocialattitudes = sum(socialattitudes)
        averageSocialAttitude = sumsocialattitudes / len(socialattitudes)
        return averageSocialAttitude
    
    def joinPrides(self,pride2):
        self.pop_pride.extend(pride2.pop_pride)
        
    
    def getvalue_mostenergycarviz (self):
        return max(self.pop_pride, key=lambda i: i.energy).energy 
    
    def get_mostenergycarviz (self):
        return max(self.pop_pride, key=lambda i: i.energy) 
    
    def eliminate_mostenergycarviz (self):
        i = Pride.get_mostenergycarviz (self)
        self.pop_pride.remove(i)
    
    def spread_energy (self,energyleft):
        def take_energy(carv):
            return carv.energy
        sorted_pop = sorted(self.pop_pride, key=take_energy)
        for x in sorted_pop: # from the least energetic carviz to the highest
            if energyleft == 0: # for loop breaks
                break 
            if x.energy+energyleft <= 100: # assignment successed, loop breaks
                x.energy = x.energy + energyleft 
                break
            else:
                give = 100-x.energy
                x.energy = x.energy + give
                energyleft = energyleft - give
            
                
    

class cell:
    def __init__(self, x, y, habitable, population : list, vegetobDensity = 20):
        self.x = x
        self.y = y
        self.habitable = habitable
        self.population = population
        self.vegetobDensity = vegetobDensity

    def getCoodinates(self):
        return (self.x, self.y)

    def addLiving(self, living):
        if not isinstance(living, Pride):
            living.memory = living.location
            living.setLocation(self.getCoodinates())
        else:
            for i in living.pop_pride:
                i.memory = i.location
                i.setLocation(self.getCoodinates())
        self.population.append(living)    
        
    def addPopulation(self,population : list ):
        for living in population:
            if not isinstance(living, Pride):
                living.memory = living.location
                living.setLocation(self.getCoodinates())
            else:
                for i in living.pop_pride:
                    i.memory = i.location
                    i.setLocation(self.getCoodinates())
        self.population.extend(population)
        
    def isHabitable(self):
        return self.habitable

    def getVegetobDensity(self):
        return self.vegetobDensity

    def growVegetob(self):
        if self.vegetobDensity < 100:
            self.vegetobDensity += 1
    def decreaseVegetob(self):
        if self.vegetobDensity > 0:
            self.vegetobDensity -= 1
    
    def removeLiving(self, living):
        self.population.remove(living)
    
    def removeLivingfromPride (self,living):
        for i in self.population:
            if type(i) == list or living in i:
                pass

    def getPopulations(self):
        cellpopulation = {}
        erbasts = []
        carvizs = [[]]
        
        for living in self.population:
            if isinstance(living, Erbast):
                erbasts.append(living)
            elif isinstance(living, Carviz):
                carvizs[0].append(living)
            elif isinstance(living, Pride):
                carvizs.append(living.pop_pride)
        cellpopulation['Erbasts'] = erbasts
        carvizs = [i for i in carvizs if i !=[]]
        cellpopulation['Carvizs'] = carvizs
        return cellpopulation

        
    def nPopulations (self):
        populations = cell.getPopulations(self)
        nPopulations = {}
        nerbasts = 0
        ncarvizs = 0
        for l in populations:
                if l == 'Erbasts':     
                    nerbasts = len (populations[l])
                if l == 'Carvizs':
                    for n in populations[l]:
                        if isinstance(n, Carviz):    
                            ncarvizs = ncarvizs + 1
                        elif isinstance(n, Pride):
                            ncarvizs = ncarvizs + len (n.pop_pride)
        nPopulations['Erbasts'] = nerbasts
        nPopulations['Carvizs'] = ncarvizs
        return nPopulations
    
    def getstrongestErbast(self):
        erbasts = cell.getPopulations(self)['Erbasts']
        maxenergy = max([i.energy for i in erbasts])
        for i in erbasts:
            if i.energy == maxenergy:
                return i
    def death(self):
        for animal in self.population:
            if type(animal) != Pride:
                if animal.energy <= 0:
                    self.removeLiving(animal)
            elif type(animal) == Pride:
                for a in animal.pop_pride:
                    if a.energy <= 0 :
                        animal.deletemember(a)
                
        

            
class World:
    def __init__(self,ncol,nrow,p): # p: list with probabilities to spawn in a cell 0th element = Erbast 1th Element 0 Carviz
        self.state = []
        if not isinstance(p, list):
            raise TypeError(" 'p' must be a list.")
        if ((p[0] + p[1] != 1) and (p[0]>0 or p[0]<1) and (p[1]>0 or p[1]<1)) or (nrow<1 or ncol<1):
            raise TypeError("Values not valid.")
        self.nrow = nrow
        self.ncol = ncol
        self.p1 = p[0]
        self.p2 = p[1]
        
        
        for y in range(0, self.nrow):
            self.state.append([])
            for x in range(0, self.ncol):
                if x==0 or y==0 or x==self.ncol-1 or y == self.nrow-1:
                    self.state[y].append(cell(x,y , False, []))
                else:
                    options = [True, False]
                    weights = [0.75, 0.25]  # 75% probability of Ground, 25% probability of Water
                    self.state[y].append(cell(x, y, random.choices(options, weights, k=1)[0], []))
                    if self.state[y][x].isHabitable() == True:
                        probs = [self.p1,self.p2]
                        for animals in range (1,random.randint(5,15)):
                            animal_types = [Erbast(self.state[y][x].getCoodinates()), Carviz(self.state[y][x].getCoodinates())]
                            a = random.choices(animal_types, probs, k=1)[0]
                            self.state[y][x].addLiving(a)
    
        self.habitableworld = []
        for y in self.state:
            for cell_i in y:
                if cell_i.isHabitable():
                    self.habitableworld.append(cell_i)
    
    def viewMatrix(self):
        matrix = np.zeros((self.nrow, self.ncol))
        for row in self.state:
            for cell in row:
                if cell.isHabitable() == True:
                    matrix[cell.y][cell.x] = 1
        return matrix
    
        
    
    def getPos(self, x, y):
        if x < 0 or y < 0 or x >= self.nrow or y >= self.ncol:
            return None
        return self.state[y][x]
    
    def getneighborhood_cell (self,cell_i):
        submatrix = []
        x = cell_i.getCoodinates()[0]
        y = cell_i.getCoodinates()[1]
        for i in range(y-1, y+2):
            row_list = []
            for j in range(x-1, x+2):
                if self.state[y][x]!=self.state[i][j] and self.state[y][x].isHabitable():
                    row_list.append(self.state[i][j])
                    submatrix.append(row_list)
        return submatrix
    
    
    # 3.1 GROWING
    
    def Growing (self):
        for cell_i in self.habitableworld:
            cell_i.growVegetob()
        for cell_i in self.habitableworld:
            n = self.getneighborhood_cell(cell_i)
            count = 0
            for i in n:
                for j in i:
                        count = count + j.vegetobDensity
            if count == max_neigh_density:
                cell_i.population = [] # All animals in the cell are dead
    
    #3.2 MOVEMENT 
    # Movements are happening at the same time,as for the decision for them
    #3.2.1 DECISIONS
    def Decisions(self):
        for cell_i in self.habitableworld:
                        n = self.getneighborhood_cell(cell_i)
                        candidates_h = [0,0,0]
                        # position 0 = candidate most density cell
                        # position 1 = candidate less carvizs population's cell
                        # position 2 = candidate most erbast population's cell
                    
                        candidates_p = [0,0]
                        # position 0 = candidate less carvizs population's cell
                        # position 1 = candidate more erbasts population's cell
                        
                        vdensity = 0
                        pcarviz_h = 0
                        perbast_h = 0
                        
                        pcarviz_p = 0
                        perbast_p = 0
                    
                    
                        for i in n:
                            for j in i:
                                    if vdensity == 0 or vdensity <= j.getVegetobDensity():
                                        vdensity = j.getVegetobDensity()
                                        candidates_h[0] = j.getCoodinates()
                                    if pcarviz_h == 0 or pcarviz_h >= j.nPopulations()['Carvizs']:
                                        pcarviz_h = j.nPopulations()['Carvizs']
                                        candidates_h[1] = j.getCoodinates()
                                    if perbast_h == 0 or perbast_h <= j.nPopulations()['Erbasts']:
                                        perbast_h = j.nPopulations()['Erbasts']
                                        candidates_h[2] = j.getCoodinates()
                                    
                                    if pcarviz_p == 0 or pcarviz_p >= j.nPopulations()['Carvizs']:
                                        pcarviz_p = j.nPopulations()['Carvizs']
                                        candidates_p[0] = j.getCoodinates()
                                    if perbast_p == 0 or perbast_p <= j.nPopulations()['Erbasts']:
                                        candidates_p[1] = j.getCoodinates()
                        cell_i.herddecision = random.choice(candidates_h)
                        cell_i.pridedecision = random.choice(candidates_p)
                        
    #3.2.2 MOVEMENTS
    def Movements(self):
            for cell_i in self.habitableworld:                          
                          erb_p = cell_i.getPopulations()['Erbasts']
                          car_p = cell_i.getPopulations()['Carvizs']
                          
                          # if herd will move:
                          if type(cell_i.herddecision)!=0: 
                              p_celldestination = self.state[cell_i.herddecision[1]][cell_i.herddecision[0]] 
                              for erbast in erb_p:
                                        if erbast.s_attitude > 0.50 and cell_i.herddecision != erbast.memory and erbast.energy > 40:
                                            cell_i.removeLiving(erbast)
                                            erbast.energy = erbast.energy-1
                                            p_celldestination.addLiving(erbast)
                                        
                                        else:
                                            erbast.memory = 0 # Consider if delete this line, notice that the animals will be move less 
                          # if a pride will move:
                          if type(cell_i.pridedecision)!=0: 
                              pride_i = []
                              pride_i = Pride(pride_i)    
                              for p in car_p:
                                    for c in p:
                                            if c.s_attitude > 0.4 and c.energy > 40:
                                                c.energy = c.energy - 1 
                                                pride_i.addmember(c)
                                            else:
                                                c.memory = 0 # Consider if delete this line,  notice that the animals will be move less 
                              if pride_i.pop_pride != []:
                                  h_celldestination = self.state[cell_i.pridedecision[1]][cell_i.pridedecision[0]]
                                  h_celldestination.addLiving(pride_i)
                                  for i in pride_i.pop_pride:
                                      for k in cell_i.population:
                                          if isinstance(k, Carviz) and k == i:
                                              cell_i.removeLiving(i)
                                              i.setLocation(h_celldestination.getCoodinates())
                                          elif isinstance(k, Pride) and i in k.pop_pride:
                                              newk = [x for x in k.pop_pride if i != x]
                                              cell_i.removeLiving(k)
                                              cell_i.addPopulation(newk)                                      
                                     
            for cell_i in self.habitableworld:     
                          cell_i.death()
    # 3.3  GRAZING               
    def GrazeRoutine(self):
            for cell_i in self.habitableworld:
                    if cell_i.getPopulations()['Erbasts'] != []:
                        for erb in cell_i.getPopulations()['Erbasts']:
                            check = [i.energy for i in cell_i.getPopulations()['Erbasts']]
                            min_value = min(check)    
                            min_elements = [x for x in check if x == min_value]
                            if erb.memory == 0:
                                    if cell_i.nPopulations()['Erbasts'] < cell_i.getVegetobDensity():
                                        erb.graze(cell_i)
                                    else: # if cell_i.nPopulations()['Erbasts'] >= cell_i.getVegetobDensity()
                                        if erb.energy in min_elements:
                                            erb.graze(cell_i)
    # 3.4 STRUGGLE
    def Struggle (self):
            for cell_i in self.habitableworld:
                    cell_i.fights = []
                    if cell_i.nPopulations()['Carvizs'] != 0:
                        for i in cell_i.getPopulations()['Carvizs']: # for every pride
                            for j in cell_i.getPopulations()['Carvizs']: # for every pride
                                if i != j:
                                    if i.getaverageSocialAttitude() > 0.5 and j.getaverageSocialAttitude() > 0.5: # joinPrides
                                        i.joinPrides(j)
                                    if i.getaverageSocialAttitude() <= 0.5 and j.getaverageSocialAttitude() > 0.5:
                                        choice = random.choice(['Fight', 'joinPrides'])
                                        if choice == 'Fight' and ((i,j) not in cell_i.fights or (j,i) not in cell_i.fights):
                                            cell_i.fights.append((i,j))
                                        elif choice == 'joinPrides':
                                            i.joinPrides(j)
                                    if i.getaverageSocialAttitude() <= 0.5 and j.getaverageSocialAttitude() <= 0.5: # fight
                                        if (i,j) not in cell_i.fights or (j,i) not in cell_i.fights:
                                            cell_i.fights.append((i,j))
    
    #3.5 FIGHT 
    def Fight(self):
        for cell_i in self.habitableworld:
                    if cell_i.fights != []:
                        for x in cell_i.fights:
                                    while True:
                                        if x[0].pop_pride == []:
                                            break
                                        if x[1].pop_pride == []:
                                            break            
                                        en_weights = [x[0].getvalue_mostenergycarviz(),x[1].getvalue_mostenergycarviz()]
                                        n = random.choices(x, en_weights, k=1)[0] #winner
                                        if x[0] != n:
                                            x[0].eliminate_mostenergycarviz()
                                        else:
                                            x[1].eliminate_mostenergycarviz()
    
    #3.6 HUNT
    def Hunt(self):
            def nocombat (cell_i,hunter,target):
                #hunt success
                size = target.energy / cell_i.nPopulations()['Carvizs']
                for i in cell_i.getPopulations()['Carvizs'][0]:
                    if i.energy + size <= 100:
                        i.energy = i.energy + size
                    else:
                        spareenergy = 100 - (i.energy + size)
                        hunter.spread_energy(spareenergy)
                cell_i.removeLiving(target)
                
            def singleassault (cell_i,hunter,target):
                chance = random.random()*100 # %chance of hunt fail
                energypride = hunter.getaverageEnergy()
                if energypride > chance and energypride > target.energy:
                    #hunt success
                    nocombat(cell_i, hunter, target)
            
            def lastblood(cell_i,hunter,target):
                chance = random.random()*100 # %chance of hunt fail
                energypride = hunter.getaverageEnergy()
                if energypride > chance and energypride > target.energy:
                    #hunt success
                    nocombat(cell_i, hunter, target)
                else:
                    #hunt fail
                    random.choice(hunter.pop_pride).energy -= 1
                    while True:
                        singleassault (cell_i,hunter,target)
                        if target not in cell_i.population:
                            break
                        if energypride <= chance and energypride <= target.energy:
                            #hunt fail
                            random.choice(hunter.pop_pride).energy -= 1            
            
            
            for cell_i in self.habitableworld:
                    if cell_i.getPopulations()['Erbasts'] != [] and cell_i.getPopulations()['Carvizs'] != []:
                        objective = cell_i.getstrongestErbast()
                        hunterpride = Pride(cell_i.getPopulations()['Carvizs'][0])
                        # weights: relative value of the cumulative Energy of the pride and the Energy of the prey
                        # it's relative to the pride_i
                        # choices: 
                        actions = ['NoCombat','SingleAssault','LastBlood'] 
                        action = random.choices(actions, weights=[0.3,0.4,0.3], k=1) # different probabilities for the different choices

                        if action == 'NoCombat':
                            nocombat (cell_i,hunterpride,objective)
                        if action =='SingleAssault':
                            singleassault (cell_i,hunterpride,objective)
                        if action =='LastBlood':
                            lastblood(cell_i,hunterpride,objective)
            
    #3.7 SPAWNING
    def Spawning(self):
         for cell_i in self.habitableworld:
                            newborns = []
                            deaths = []
                            for i in cell_i.population:
                                if type(i) != Pride:
                                    i.age += 1
                                    if i.age % 100 == 0:
                                        i.energy -= 1 
                                    if i.age == i.lifetime:
                                        born1, born2 = i.spawning()
                                        deaths.append(i)  
                                        newborns.append(born1)
                                        newborns.append(born2)
                                elif type(i) == Pride:
                                    newborns_pride = []
                                    dead_members = []
                                    for j in i.pop_pride:  
                                        j.age += 1
                                        if j.age % 100 == 0:
                                            j.energy -= 1 
                                        if j.age == j.lifetime:
                                            born1, born2 = j.spawning()
                                            newborns_pride.append(born1)
                                            newborns_pride.append(born2)
                                            dead_members.append(j)
                                    if newborns_pride != []:
                                        i.addPopulationPride(newborns_pride)
                                        i.pop_pride = [j for j in i.pop_pride if j not in dead_members]
                            if newborns != []:
                                cell_i.addPopulation(newborns)
                                cell_i.population = [i for i in cell_i.population if i not in deaths]
                        
    