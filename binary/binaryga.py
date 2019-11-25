import random as rnd
import numpy as np
import math
import copy

class Chromosome:
    def __init__(self, D):
        self.D = D
        
        self.Solution = []
        self.numActiveFeatures = 0

        self.Fitness = float('inf')

        self.generateSolution()

    def generateSolution(self):
        self.Solution = [rnd.randint(0,1) for i in range(self.D)]

    def evaluate(self):       
        self.Fitness = Chromosome.FuncEval(self.Solution)
        self.numActiveFeatures = sum([1 if i == 1 else 0 for i in self.Solution])

    
    def toString(self):
        print ("# of feats={} Fitness={}").format(self.numActiveFeatures,self.Fitness),
        print(self.Solution)
    
    def __eq__(self,other):
        return self.Solution == other.Solution and self.Fitness == other.Fitness


class bGA:
    def __init__(self,Np,D,MaxG):
        self.Np = Np
        self.D = D
        self.TournamentSize = 4
        self.Mr = 0.05
        self.Elitism = 0.1
        self.Population = []
        self.MaxG = MaxG
        self.Best = Chromosome(self.D)
        self.p = int(math.floor(self.Elitism*self.Np))

    def reset(self):
        self.__init__(self.Np,self.D,self.MaxG)

        
    def checkForBest(self,pChromosome):
        if pChromosome.Fitness <= self.Best.Fitness:
            self.Best = copy.deepcopy(pChromosome)

    def TournamentSelection(self,Pop): 
        comps = [Pop[i] for i in np.random.choice(len(Pop), self.TournamentSize, replace=False)]
        comps.sort(key=lambda x: x.Fitness)        
        return comps[0]

    def Mate(self,p1,p2):
        #print("CS")
        OnePointCr = int(rnd.random()*self.D)
        #print(OnePointCr)
        c1 = Chromosome(self.D)
        c2 = Chromosome(self.D)
        #parent1.toString()
        #parent2.toString()
        c1.Solution = p1.Solution[0:OnePointCr] + p2.Solution[OnePointCr:]
        
        c2.Solution = p2.Solution[0:OnePointCr] + p1.Solution[OnePointCr:]
        #child1.toString()
        #child2.toString()
        
        return c1,c2

    def Mutate(self,child):
        for i in range(self.D):
            if rnd.random() < self.mr:
                if child.Solution[i] == 1:
                    child.Solution[i] = 0
                else:
                    child.Solution[i] = 1
    
    def init(self):
        for i in range(self.Np):
            self.Population.append(Chromosome(self.D))
            self.Population[i].evaluate()
            self.checkForBest(self.Population[i])

    def Selection(self):
        nPop = []
        self.Population.sort(key = lambda c: c.Fitness)
        nPop = self.Population[0:self.p]

        for i in range(self.Np-self.p):
            nPop.append(self.TournamentSelection(self.Population))
        return nPop

    def Crossover(self,Pop):
        
        cPop = Pop[0:self.p]
        for i in range(self.p,self.Np,2):
            if i+1 == self.Np:
                c1,c2 = self.Mate(Pop[i-1],Pop[i])    
            else:
                c1,c2 = self.Mate(Pop[i],Pop[i+1])
            cPop.extend([c1,c2])
        return cPop

    def Mutation(self,Pop):
        for i in range(self.p,self.Np):
            for j in range(self.D):
                if rnd.random() < self.Mr:
                    Pop[i].Solution[j] = abs(Pop[i].Solution[j]-1)
        return Pop

    def EvaluatePop(self):
        for c in self.Population:
            c.evaluate()
    
    def run(self):
        #rnd.seed(42)
        self.init()
        convergenceRates = []
        for iter in range(self.MaxG):
            print("Generation {}".format(iter+1)),
            self.Best.toString()
            nPop = self.Selection()
            cPop = self.Crossover(nPop)
            self.Population = self.Mutation(cPop)
            self.EvaluatePop()

            for i in range(self.Np):
                self.checkForBest(self.Population[i])

            avgFitness = sum([s.Fitness for s in self.Population])/self.Np
            avgFeatures = sum([s.numActiveFeatures for s in self.Population])/self.Np
            convergenceRates.append([avgFitness,avgFeatures,self.Best.Fitness,self.Best.numActiveFeatures])
        return self.Best, convergenceRates




                         