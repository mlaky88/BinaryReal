#!/usr/bin/env python

import random as rnd
import copy

from sklearn import tree
from sklearn import svm


class Particle:
    '''Defines particle for population'''

    def __init__(self, D):
        self.D = D
        self.LB = 0
        self.UB = 1
        self.vmax = 6
        self.Solution = []
        self.Velocity = []
        self.numActiveFeatures = 0
        
        self.pBestPosition = []  
        self.bestFitness = float('inf')   

        self.Fitness = float('inf') 
        self.generateParticle()

    def generateParticle(self):
        self.Solution = [self.LB + (self.UB - self.LB) * rnd.random() for i in range(self.D)]
        self.Velocity = [-self.vmax + 2*rnd.random()*self.vmax for i in range(self.D)]

        self.pBestSolution =  [0 for i in range(self.D)]
        self.bestFitness = float('inf') 

    def evaluate(self):
       
        self.Fitness = Particle.FuncEval(self.Solution)
        self.numActiveFeatures = sum([1 if i >= 0.5 else 0 for i in self.Solution])
        self.checkPersonalBest()
    

    def checkPersonalBest(self):
        if self.Fitness < self.bestFitness:
            self.pBestSolution = self.Solution
            self.bestFitness = self.Fitness

    def simpleBound(self):
        for i in range(len(self.Solution)):
            if self.Solution[i] < self.LB:
                self.Solution[i] = self.LB
            if self.Solution[i] > self.UB:
                self.Solution[i] = self.UB

            if self.Velocity[i] > self.vmax or self.Velocity[i] < -self.vmax:
                self.Velocity[i] = -self.vmax + 2*rnd.random()*self.vmax


    def toString(self):
        print ("# of feats={} Fitness={}").format(self.numActiveFeatures,self.Fitness),
        print([1 if i >= 0.5 else 0 for i in self.Solution])

    def __eq__(self,other):
        return self.Solution == other.Solution and self.Fitness == other.Fitness



class PSO:

    def __init__(self, Np, D, MaxG):
        '''Constructor'''
        self.Np = Np
        self.D = D
        self.MaxG = MaxG
        self.Swarm = []
        self.C1 = 2
        self.C2 = 2
        #self.vmax = 0.9
        #self.vmin = 0.2
        
        self.gBest = Particle(D)

    def reset(self):
        self.__init__(self.Np,self.D,self.MaxG)

    def evalSwarm(self):
        for p in self.Swarm:
            p.evaluate()
            #p.toString()
            if p.Fitness < self.gBest.Fitness:
                self.gBest = copy.deepcopy(p)
            
        

    def initSwarm(self):
        for i in range(self.Np):
            self.Swarm.append(Particle(self.D))
       
        
    
    def moveSwarm(self, Swarm):
        MovedSwarm = []
        for p in Swarm: 
            part1 = ([(a-b)* rnd.random() * self.C1 for a,b in zip(p.pBestSolution,p.Solution)])
            part2 = ([(a-b)* rnd.random() * self.C2 for a,b in zip(self.gBest.Solution,p.Solution)])
        
            p.Velocity = ([self.W*a+b+c for a,b,c in zip(p.Velocity,part1,part2)])            
            p.Solution = ([a+b for a,b in zip(p.Solution,p.Velocity)])
            p.simpleBound()
            
            p.evaluate()
            if p.Fitness < self.gBest.Fitness:
                self.gBest = copy.deepcopy(p)
        
            MovedSwarm.append(p)
        return MovedSwarm


    def run(self):
        g = 1        
        self.initSwarm()
        self.evalSwarm()
        self.W = 0.9
        convergenceRates = []
        while g <= self.MaxG:
            #self.W=self.vmax-(g-1)*((self.vmax-self.vmin)/self.MaxG)
            print("Generation {}").format(g)
            self.gBest.toString()
            MovedSwarm = self.moveSwarm(self.Swarm)
            self.Swarm = MovedSwarm
            avgFitness = sum([s.bestFitness for s in self.Swarm])/self.Np
            avgFeatures = sum([s.numActiveFeatures for s in self.Swarm])/self.Np
            convergenceRates.append([avgFitness,avgFeatures,self.gBest.Fitness,self.gBest.numActiveFeatures])
            g += 1
        return self.gBest, convergenceRates
    