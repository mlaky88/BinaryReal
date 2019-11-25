#!/usr/bin/env python
#https://www.sciencedirect.com/science/article/pii/S0925231214009229#bib20
#https://www.sciencedirect.com/science/article/pii/S1568494613001361
import random as rnd
import copy
import math


class Particle:
    def __init__(self, D):
        self.D = D
        self.vmax = 6
        self.Solution = []
        self.Velocity = []
        self.numActiveFeatures = 0
        
        self.pBestSolution = []  
        self.pBestFitness = float('inf') 

        self.Fitness = float('inf')
        self.generateParticle()

    def generateParticle(self):
        self.Solution = [0 if rnd.random() < 0.5 else 1 for i in range(self.D)]
        self.Velocity = [-self.vmax + 2*rnd.random()*self.vmax for i in range(self.D)]
        self.pBestSolution =  [0 for i in range(self.D)]

    def evaluate(self):       
        self.Fitness = Particle.FuncEval(self.Solution)
        self.numActiveFeatures = sum([1 if i == 1 else 0 for i in self.Solution])
        self.checkPersonalBest()    

    def checkPersonalBest(self):
        if self.Fitness < self.pBestFitness:
            self.pBestSolution = self.Solution
            self.pBestFitness = self.Fitness

    def simpleBound(self):
        for i in range(len(self.Velocity)):
            if self.Velocity[i] > self.vmax or self.Velocity[i] < -self.vmax:
                self.Velocity[i] = -self.vmax + 2*rnd.random()*self.vmax


    def toString(self):
        print ("# of feats={} Fitness={}").format(self.numActiveFeatures,self.Fitness),
        print (self.Solution)

    def __eq__(self,other):
        return self.Solution == other.Solution and self.Fitness == other.Fitness


class bPSO:

    def __init__(self, Np, D, MaxG):
        self.Np = Np
        self.D = D
        self.MaxG = MaxG
        self.Swarm = []
        self.C1 = 2.0
        self.C2 = 2.0
        #self.vmax = 0.9
        #self.vmin = 0.2
        
        self.gBest = Particle(D)

    def reset(self):
        self.__init__(self.Np,self.D,self.MaxG)

    def evalSwarm(self):
        for p in self.Swarm:
            p.evaluate()
            p.toString()
            if p.Fitness < self.gBest.Fitness:
                self.gBest = copy.deepcopy(p)            
        
    def initSwarm(self):
        for i in range(self.Np):
            self.Swarm.append(Particle(self.D))       
        
    
    def logisticFun(self,v):
        return 1.0 / (1 + math.exp(-v))
    
    def moveSwarm(self, Swarm):
        MovedSwarm = []
        for p in Swarm:
            part1 = ([(a-b) * rnd.random() * self.C1 for a,b in zip(p.pBestSolution,p.Solution)])
            part2 = ([(a-b) * rnd.random() * self.C2 for a,b in zip(self.gBest.Solution,p.Solution)])
        
            p.Velocity = ([self.W*a+b+c for a,b,c in zip(p.Velocity,part1,part2)])
            
            #p.simpleBound()

            for i,v in enumerate(p.Velocity):
                if rnd.random() < self.logisticFun(v):
                    p.Solution[i] = 1
                else:
                    p.Solution[i] = 0

            #for i,v in enumerate(p.Solution):
            #    if rnd.random() <= 1.0 / self.D:
            #        p.Solution[i] = abs(p.Solution[i]-1)

            #print(p.Solution)
            #print(p.Velocity)
            #print()
            
            
            p.evaluate()
            if p.Fitness < self.gBest.Fitness:
                self.gBest = copy.deepcopy(p)
        
            MovedSwarm.append(p)
        return MovedSwarm


    def run(self):
        g = 1        
        self.initSwarm()
        self.evalSwarm()
        print("Best")
        self.gBest.toString()
        self.W = 0.9
        convergenceRates = []
        while g <= self.MaxG:
            #self.W=self.vmax-(g-1)*((self.vmax-self.vmin)/self.MaxG)
            print("Generation {}").format(g)
            self.gBest.toString()
            MovedSwarm = self.moveSwarm(self.Swarm)
            self.Swarm = MovedSwarm
            avgFitness = sum([s.pBestFitness for s in self.Swarm])/self.Np
            avgFeatures = sum([s.numActiveFeatures for s in self.Swarm])/self.Np
            convergenceRates.append([avgFitness,avgFeatures,self.gBest.Fitness,self.gBest.numActiveFeatures])
            
            g += 1
        return self.gBest,convergenceRates
    