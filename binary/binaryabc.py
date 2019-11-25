#Implementation of the real-value coded ABC algorithm
#Clanek https://www.sciencedirect.com/science/article/pii/S1568494615004639
#MDisABC

import random as rnd
import copy
import numpy as np

class SolutionABC:
    def __init__(self,D):
        self.D = D
        self.Solution = []
        self.Fitness = float('inf')
        self.generateSolution()

    def generateSolution(self):
        self.Solution = [1 if rnd.random() >= 0.75 else 0 for _ in range(self.D)]
        self.numActiveFeatures = sum([1 if i == 1 else 0 for i in self.Solution])
        '''self.Solution = [0 for i in range(18)]
        self.Solution[0] = 1
        self.Solution[1] = 1
        self.Solution[2] = 1
        self.Solution[5] = 1'''
        while self.numActiveFeatures < 1:
            self.Solution = [1 if rnd.random() >= 0.75 else 0 for _ in range(self.D)]
            self.numActiveFeatures = sum([1 if i == 1 else 0 for i in self.Solution])


    def resetSolution(self):
        self.Solution = [0 for _ in range(self.D)]
        
    def evaluate(self):
        self.Fitness = SolutionABC.FuncEval(self.Solution)
        self.numActiveFeatures = sum([1 if i == 1 else 0 for i in self.Solution])

    def toString(self):
        print ("# of feats={} Fitness={}").format(self.numActiveFeatures,self.Fitness),
        print(self.Solution)



class bMDisABC:
    def __init__(self,Np,D,MaxCycle):
        self.sigma_max = 0.9
        self.sigma_min = 0.5
        self.Np = Np
        self.D = D
        self.Limit = 50
        self.Trial = []
        self.MaxCycle = MaxCycle
        self.Foods = []
        self.Probs = []
        self.Cr = 0.25
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

    def CalculateProbs(self):
        #self.Probs = [1.0 / (self.Foods[i].Fitness+0.01) for i in range(self.Np)]
        #print([self.Foods[i].Fitness for i in range(self.Np)])
        minV = min([self.Foods[i].Fitness for i in range(self.Np)])
        t1 = [f.Fitness-minV for f in self.Foods]
        maxV = max(t1)
        t2 = [(maxV - f.Fitness) + 0.01 for f in self.Foods]

        s = sum(t2)
        
        self.Probs = [t / s for t in t2]
        

    def checkForBest(self,Solution):
        if Solution.Fitness < self.Best.Fitness:
            self.Best = copy.deepcopy(Solution)

    def getScalingFactor(self,iter):
        return self.sigma_max - (float(self.sigma_max-self.sigma_min)/self.MaxCycle)*iter

    def disimilarity(self,sol1,sol2):
        #print(sol1)
        #print(sol2)
        nx = np.array(sol1)
        ny = np.array(sol2)
        M11 = (nx&ny).tolist().count(1)
        M10 = (nx-ny).tolist().count(1)
        M01 = (nx-ny).tolist().count(-1)
        disimilarity = 1 - float(M11)/(M11+M10+M01)
        #print("M11={},M01={},M10={}, ret={}".format(M11,M01,M10,disimilarity))
        return disimilarity


    def getMValues(self,m1,m0,A):
        sol = (0,0,0)
        #print m1,m0
        minValue = A
        for i in range(m1+1):
            for j in range(m0+1):
                #M11,M01,M10 
                #print (i,m1-i,j)

                try:
                    obj = abs(1.0 - float(i)/(i+j+m1-i) - A)
                except:
                    print (i,m1-i,j)
                if obj < minValue:
                    minValue = obj
                    sol = (i,m1-i,j)
        return sol

    def generateTrialVector(self,sol,M):
        M11 = M[0]
        M01 = M[1]
        M10 = M[2]
        #print("M",M,)
        #print("Solution",sol)
        #print("Best    ",self.Best.Solution)
        S1 = [idx for idx,value in enumerate(sol) if value == 1]
        S0 = [idx for idx,value in enumerate(sol) if value == 0]
        #print("S1",S1)
        #print("S0",S0)
        
        bS11 = [idx for idx,value in enumerate(zip(sol,self.Best.Solution)) if value[0] == 1 and value[1] == 1]
        bS10 = [idx for idx,value in enumerate(zip(sol,self.Best.Solution)) if value[0] == 0 and value[1] == 1]

        #print bS11
        #print bS10
        nS = SolutionABC(self.D)
        nS.resetSolution()
        if rnd.random < 0.5:
            #print("Random selection")
            rM1 = rnd.sample(S1, M11)
            rM0 = rnd.sample(S0, M10)
            for j in rM1:
                nS.Solution[j] = 1
            for j in rM0:
                nS.Solution[j] = 1
        else:
            #print("Greedy selection")
            #change where 1 in both
            for pos in bS11:
                S1.remove(pos)
                nS.Solution[pos] = 1
            #print("Modified S1", S1)
            #nS.toString()
            if len(bS11) < M11:
                needChange = M11-len(bS11)
                rM1 = rnd.sample(S1, needChange)
                #print("rM1",rM1)
                for j in rM1:
                    nS.Solution[j] = 1
            
            for pos in bS10:
                S0.remove(pos)
                nS.Solution[pos] = 1
            #print("Modified S0", S0)
                
            if len(bS10) < M10:
                needChange = M10-len(bS10)
                rM0 = rnd.sample(S0, needChange)
                for j in rM0:
                    nS.Solution[j] = 1
                

        #nS.toString()

        return nS
        

    def greedySelection(self,trial,i):
        if trial.Fitness < self.Foods[i].Fitness:
            self.Foods[i] = trial
            self.Trial[i] = 0
        else:
            self.Trial[i] += 1

    def doCrossover(self,trial,i):
        for d in range(self.D):
            if rnd.random() > self.Cr:
                trial.Solution[d] = self.Foods[i].Solution[d]
        return trial


    def generateSolution(self,iter,i):
        r = rnd.sample(range(0, self.Np), 3)
        while i in r:
            r = rnd.sample(range(0, self.Np), 3)
        A = self.disimilarity(self.Foods[r[1]].Solution,self.Foods[r[2]].Solution)*self.getScalingFactor(iter)
        #print ("Solution in mind", self.Foods[r[0]].Solution, r[0])
        M = self.getMValues(self.Foods[r[0]].Solution.count(1),self.Foods[r[0]].Solution.count(0),A)
        trial = self.generateTrialVector(self.Foods[r[0]].Solution,M)
        trial = self.doCrossover(trial,i)
        trial.evaluate()
        #trial.toString()
        self.greedySelection(trial,i)

    def employed_bees(self,iter):
        for i in range(self.Np):
            self.generateSolution(iter,i)

    def onlooker_bees(self,iter):
        t = 0
        i = 0
        while t < self.Np:
        #for i in range(self.Np):
            if rnd.random() < self.Probs[i]:
                t += 1
                self.generateSolution(iter,i)
            i += 1
            if i == self.Np:
                i = 0
            

    def scout_bees(self):
        for i in range(self.Np):
            if self.Trial[i] >= self.Limit:
                self.Foods[i] = SolutionABC(self.D)
                self.Foods[i].evaluate()
                self.Trial[i] = 0
                #self.checkForBest(self.Foods[i])


    def run(self):
        self.init()
        convergenceRates = []
        for iter in range(self.MaxCycle):
            print("Gen {} => {}".format(iter+1,self.Best.Fitness))
            self.Best.toString()
            
            self.employed_bees(iter)
            self.CalculateProbs()
            self.onlooker_bees(iter)
            self.scout_bees()
            
            for i in range(self.Np):
                self.checkForBest(self.Foods[i])


            avgFitness = sum([s.Fitness for s in self.Foods])/self.Np
            avgFeatures = sum([s.numActiveFeatures for s in self.Foods])/self.Np
            convergenceRates.append([avgFitness,avgFeatures,self.Best.Fitness,self.Best.numActiveFeatures])
        return self.Best,convergenceRates