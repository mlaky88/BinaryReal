#!/usr/bin/env python
#http://www.sciencedirect.com/science/article/pii/S0957417414002164
#http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=4749258
#https://pdfs.semanticscholar.org/cf63/0dbd510c5203bddd4a40c51c0e3ec47b6cfa.pdf
#http://www.sciencedirect.com/science/article/pii/S0950705117300801
#http://www.tandfonline.com/doi/abs/10.1080/09540091.2012.737765
#http://ieeexplore.ieee.org/abstract/document/7471506/
#https://link.springer.com/article/10.1007/s00521-013-1368-0
import random as rnd
import copy



class SolutionDE:
    '''Defines particle for population'''

    def __init__(self, D):
        self.D = D
        self.LB = 0
        self.UB = 1
        
        self.Solution = []
        self.numActiveFeatures = 0

        self.F = 0.8
        self.Cr = 0.7

        self.Fitness = float('inf')

        self.generateSolution()

    def generateSolution(self):
        self.Solution = [self.LB + (self.UB - self.LB) * rnd.random() for i in range(self.D)]
        

    def evaluate(self):       
        self.Fitness = SolutionDE.FuncEval(self.Solution)
        self.numActiveFeatures = sum([1 if i >= 0.5 else 0 for i in self.Solution])
    
    def repair(self):
        for i in range(self.D):
            if (self.Solution[i] > self.UB):
                self.Solution[i] = self.UB
            if self.Solution[i] < self.LB:
                self.Solution[i] = self.LB              


    def toString(self):
        print ("# of feats={} Fitness={}").format(self.numActiveFeatures,self.Fitness),
        print([1 if i >= 0.5 else 0 for i in self.Solution])

    def __eq__(self,other):
        return self.Solution == other.Solution and self.Fitness == other.Fitness



class DE:

    def __init__(self, Np, D, MaxG):
        self.Np = Np
        self.D = D
        self.MaxG = MaxG
        self.Population = []
        self.bestSolution = SolutionDE(self.D)
        self.Tao = 0.12
        self.max_pop_size = Np
        self.Reduce = False
    
    def reset(self):
        self.__init__(self.Np,self.D,self.MaxG)

    def evalPopulation(self):
        for p in self.Population:
            p.evaluate()
            if p.Fitness < self.bestSolution.Fitness:
                self.bestSolution = copy.deepcopy(p)

    def initPopulation(self):
        for i in range(self.Np):
            self.Population.append(SolutionDE(self.D))          
    

    def generationStep(self,Population):
        
        newPopulation = []

        for i in range(self.Np):
            newSolution = SolutionDE(self.D)
            '''
            if rnd.random() < self.Tao:
                newSolution.Cr = rnd.random()
            else:
                newSolution.Cr = self.Population[i].Cr
            if rnd.random() < self.Tao:
                newSolution.F = rnd.random()
            else:
                newSolution.F = self.Population[i].F   
            '''      
            r = rnd.sample(range(0, self.Np), 3)
            while i in r:
                r = rnd.sample(range(0, self.Np), 3)  
            jrand = int(rnd.random()*self.Np)

            for j in range(self.D):
                if rnd.random() < newSolution.Cr or j == jrand:
                    newSolution.Solution[j] = Population[r[0]].Solution[j] + newSolution.F * (Population[r[1]].Solution[j]- Population[r[2]].Solution[j])
                else:
                    newSolution.Solution[j] = Population[i].Solution[j]
            newSolution.repair()
            newSolution.evaluate()
            
            if newSolution.Fitness < self.bestSolution.Fitness:
                self.bestSolution = copy.deepcopy(newSolution)
            if (newSolution.Fitness < self.Population[i].Fitness):
                newPopulation.append(newSolution)
            else:
                newPopulation.append(Population[i])
        return newPopulation
            
                
    def reducePopulation(self,Population, g):        

        if self.Reduce == True:
            min_pop_size = 4
            plan_pop_size = round((((min_pop_size - self.max_pop_size) / float(self.MaxG)) * g) + self.max_pop_size)
            #print("new pop size={}".format(plan_pop_size))
            if plan_pop_size < self.Np:
                numReductions = self.Np - plan_pop_size
                #print("numReductions={}".format(numReductions))
                if self.Np - numReductions < min_pop_size:
                    numReductions = self.Np - min_pop_size
                Population.sort(key = lambda  p: p.Fitness)
                Population = Population[1:]
                self.Np -= int(numReductions)
            #print("nPop size = {}".format(len(Population)))
            #print(self.Np)
        return Population

    def run(self):
        g = 1        
        self.initPopulation()
        self.evalPopulation()
        convergenceRates = []
        while g <= self.MaxG:        
            print("Generation {}".format(g)),
            nPopulation = self.generationStep(self.Population)
            self.Population = self.reducePopulation(nPopulation,g)
            self.bestSolution.toString()
            avgFitness = sum([s.Fitness for s in self.Population])/self.Np
            avgFeatures = sum([s.numActiveFeatures for s in self.Population])/self.Np
            convergenceRates.append([avgFitness,avgFeatures,self.bestSolution.Fitness,self.bestSolution.numActiveFeatures])
            g += 1
        return self.bestSolution, convergenceRates