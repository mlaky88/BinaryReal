import random as rnd
import copy
import numpy as np

class Chromosome:
    def __init__(self, D):
        self.D = D
        self.LB = 0
        self.UB = 1
        
        self.Solution = []
        self.numActiveFeatures = 0

        self.Fitness = float('inf')

        self.generateSolution()

    def generateSolution(self):
        self.Solution = [self.LB + (self.UB - self.LB) * rnd.random() for i in range(self.D)]

    def evaluate(self):       
        self.Fitness = Chromosome.FuncEval(self.Solution)
        self.numActiveFeatures = sum([1 if i >= 0.5 else 0 for i in self.Solution])
    
    def toString(self):
        print ("# of feats={} Fitness={}").format(self.numActiveFeatures,self.Fitness),
        print([1 if i >= 0.5 else 0 for i in self.Solution])
        
    
    def repair(self):
        for i in range(self.D):
            if (self.Solution[i] > self.UB):
                self.Solution[i] = self.UB
            if self.Solution[i] < self.LB:
                self.Solution[i] = self.LB
    def __eq__(self,other):
        return self.Solution == other.Solution and self.Fitness == other.Fitness


class GA:
    def __init__(self,Np,D,MaxG):
        self.Np = Np
        self.D = D
        self.TournamentSize = 4
        self.Mr = 0.05
        self.Population = []
        self.Probabilities = []
        self.MaxG = MaxG
        self.Best = Chromosome(self.D)
        self.Elitism = 0.1
        self.p = int(self.Elitism*self.Np)
        self.Alpha = 0.5


    def reset(self):
        self.__init__(self.Np,self.D,self.MaxG)
        
    def checkForBest(self,pChromosome):
        if pChromosome.Fitness <= self.Best.Fitness:
            self.Best = copy.deepcopy(pChromosome)

    def TournamentSelection(self,Pop):
        comps = [Pop[i] for i in np.random.choice(len(Pop), self.TournamentSize, replace=False)]
        comps.sort(key=lambda x: x.Fitness)        
        return comps[0]

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

    def Mate(self,p1,p2):
        
        gamma = [-self.Alpha + (1+2*self.Alpha) * rnd.random() for i in range(self.D)]
        c1 = Chromosome(self.D)
        c2 = Chromosome(self.D)
        c1.Solution = [gamma[i]*p2.Solution[i] + (1-gamma[i]) * p1.Solution[i] for i in range(self.D)]
        c2.Solution = [gamma[i]*p1.Solution[i] + (1-gamma[i]) * p2.Solution[i] for i in range(self.D)]
        #print(c1.Solution)
        #print(c2.Solution)
        #exit(1)
        return c1,c2

    def Mutation(self,Pop):
        for i in range(self.p,self.Np):
            for j in range(self.D):
                if rnd.random() < self.Mr:
                    Pop[i].Solution[j] = rnd.random()
        return Pop


    def EvaluatePop(self):
        for c in self.Population:
            c.evaluate()
    
    def init(self):
        for i in range(self.Np):
            self.Population.append(Chromosome(self.D))
            self.Population[i].evaluate()
            self.checkForBest(self.Population[i])    
    
    def run(self):
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
        return self.Best,convergenceRates





                         