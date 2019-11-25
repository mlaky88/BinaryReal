#Implementation of the real-value coded ABC algorithm
import random as rnd
import copy
import numpy as np
class SolutionABC:
    def __init__(self,D):
        self.D = D
        self.Solution = []
        self.Fitness = float('inf')
        self.LB = 0
        self.UB = 1
        self.generateSolution()

    def generateSolution(self):
        self.Solution = [self.LB + (self.UB - self.LB) * rnd.random() for i in range(self.D)]
        while sum([1 if i >= 0.5 else 0 for i in self.Solution]) < 1:
            self.Solution = [self.LB + (self.UB - self.LB) * rnd.random() for i in range(self.D)]

    def repair(self):
        for i in range(self.D):
            if (self.Solution[i] > self.UB):
                self.Solution[i] = self.UB
            if self.Solution[i] < self.LB:
                self.Solution[i] = self.LB

    def evaluate(self):
        self.Fitness = SolutionABC.FuncEval(self.Solution)
        self.numActiveFeatures = sum([1 if i >= 0.5 else 0 for i in self.Solution])

    def toString(self):
        print ("# of feats={} Fitness={}").format(self.numActiveFeatures,self.Fitness),
        print([1 if i >= 0.5 else 0 for i in self.Solution])



class ABC:
    def __init__(self,Np,D,MaxCycle):
        self.Np = Np
        self.D = D
        
        self.Limit = 100
        self.Trial = []
        self.MaxCycle = MaxCycle
        self.Foods = []
        self.Probs = []
        self.Best = SolutionABC(self.D)
    def reset(self):
        self.__init__(self.Np,self.D,self.MaxCycle)

    def init(self):
        self.Probs = [0 for i in range(self.Np)]
        self.Trial = [0 for i in range(self.Np)]
        for i in range(self.Np):
            self.Foods.append(SolutionABC(self.D))
            self.Foods[i].evaluate()
            self.checkForBest(self.Foods[i])
            #self.Foods[i].toString()
            #quit()

    def CalculateProbs(self):
        minV = min([self.Foods[i].Fitness for i in range(self.Np)])
        t1 = [f.Fitness-minV for f in self.Foods]
        maxV = max(t1)
        t2 = [maxV - f.Fitness for f in self.Foods]

        s = sum(t2)
        self.Probs = [t / s for t in t2]

    def checkForBest(self,Solution):
        if Solution.Fitness <= self.Best.Fitness:
            self.Best = copy.deepcopy(Solution)

    
    def generateFoodSource(self,i):
        #print "Before",
        #self.Foods[i].toString()
        newSolution = copy.deepcopy(self.Foods[i])
        k = int(rnd.random() * self.Np)
        while k == i:
            k = int(rnd.random() * self.Np)
            #print("Here")
        j = int(rnd.random() * self.D)
        r = rnd.uniform(-1, 1)

        newSolution.Solution[j] = self.Foods[i].Solution[j] + r * (self.Foods[i].Solution[j]-self.Foods[k].Solution[j])
        newSolution.repair()
        #print "Generated",
        #newSolution.toString()
        #print "Compared with",
        #self.Foods[i].toString()
        newSolution.evaluate()
        if newSolution.Fitness < self.Foods[i].Fitness:
            self.checkForBest(newSolution)
            self.Foods[i] = newSolution
            self.Trial[i] = 0
        else:
            self.Trial[i] += 1

    def employed_bees(self):
        for i in range(self.Np):
            self.generateFoodSource(i)

    def onlooker_bees(self):
            t,i = 0,0
            while t < self.Np:
                if rnd.random() < self.Probs[i]:
                    t += 1
                    self.generateFoodSource(i)
                i += 1
                if i == self.Np:
                    i = 0

    def scout_bees(self):
        for i in range(self.Np):
            if self.Trial[i] >= self.Limit:
                self.Foods[i] = SolutionABC(self.D)
                self.Foods[i].evaluate()
                self.Trial[i] = 0
                

    
    def run(self):
        self.init()
        convergenceRates = []
        for iter in range(self.MaxCycle):
            print("Gen {} => {}".format(iter+1,self.Best.Fitness))
            self.Best.toString()

            self.employed_bees()
            self.CalculateProbs()
            self.onlooker_bees()
            self.scout_bees()

            avgFitness = sum([s.Fitness for s in self.Foods])/self.Np
            avgFeatures = sum([s.numActiveFeatures for s in self.Foods])/self.Np
            convergenceRates.append([avgFitness,avgFeatures,self.Best.Fitness,self.Best.numActiveFeatures])
        return self.Best,convergenceRates
