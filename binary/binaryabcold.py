#Implementation of the real-value coded ABC algorithm
#implementacija po tem clanku http://sci-hub.cc/10.1016/j.cie.2014.08.016


import random as rnd
import copy
class SolutionABC:
    def __init__(self,D):
        self.D = D
        self.Solution = []
        self.Fitness = float('inf')
        self.generateSolution()

    def generateSolution(self):
        self.Solution = [rnd.randint(0,1) for i in range(self.D)]
    def evaluate(self):
        self.Fitness = SolutionABC.FuncEval(self.Solution)
        self.numActiveFeatures = sum([1 if i == 1 else 0 for i in self.Solution])

    def toString(self):
        print ("# of feats={} Fitness={}").format(self.numActiveFeatures,self.Fitness),
        print(self.Solution)



class bABC:
    def __init__(self,NP,D,MaxCycle):
        self.NP = NP
        self.D = D
        self.FoodNumber = self.NP/2
        self.Limit = 100
        self.Trial = []
        self.MaxCycle = MaxCycle
        self.Foods = []
        self.Probs = []
        self.r = 0.5
        self.Best = SolutionABC(self.D)

    def reset(self):
        self.__init__(self.NP,self.D,self.MaxCycle)

    def init(self):
        self.Probs = [0 for i in range(self.FoodNumber)]
        self.Trial = [0 for i in range(self.FoodNumber)]
        for i in range(self.FoodNumber):
            self.Foods.append(SolutionABC(self.D))
            self.Foods[i].evaluate()
            self.checkForBest(self.Foods[i])
            self.Foods[i].toString()

    def CalculateProbs(self):
        self.Probs = [1.0 / (self.Foods[i].Fitness+0.01) for i in range(self.FoodNumber)]
        s = sum(self.Probs)
        self.Probs = [self.Probs[i] / s for i in range(self.FoodNumber)]

    def checkForBest(self,Solution):
        if Solution.Fitness <= self.Best.Fitness:
            self.Best = copy.deepcopy(Solution)

    
    def run(self):
        self.init()
        convergenceRates = []
        for iter in range(self.MaxCycle):
            print("Gen {} => {}".format(iter+1,self.Best.Fitness) )
            self.Best.toString()
            for i in range(self.FoodNumber):
                newSolution = copy.deepcopy(self.Foods[i])
                param2change = int(rnd.random() * self.D)
                neighbor = int(self.FoodNumber * rnd.random())
                rn = 1 if rnd.random() < self.r else 0
                #newSolution.Solution[param2change] = self.Foods[i].Solution[param2change]+(-1 + 2 * rnd.random())*(self.Foods[i].Solution[param2change]-self.Foods[neighbor].Solution[param2change])
                newSolution.Solution[param2change] = int(bool(self.Foods[i].Solution[param2change]) ^ bool(rn & (self.Foods[i].Solution[param2change]|self.Foods[neighbor].Solution[param2change])))
                newSolution.evaluate()
                if newSolution.Fitness < self.Foods[i].Fitness:
                    self.checkForBest(newSolution)
                    self.Foods[i] = newSolution
                    self.Trial[i] = 0
                else:
                    self.Trial[i] += 1
            
            self.CalculateProbs()
            t,s = 0,0
            while t < self.FoodNumber:
                if rnd.random() < self.Probs[s]:
                    t+=1
                    Solution = copy.deepcopy(self.Foods[s])
                    param2change = int(rnd.random() * self.D)
                    neighbor = int(self.FoodNumber * rnd.random())
                    while neighbor == s:
                        neighbor = int(self.FoodNumber * rnd.random())
                    rn = 1 if rnd.random() < self.r else 0
                    #Solution.Solution[param2change] = self.Foods[s].Solution[param2change]+(-1 + 2 * rnd.random())*(self.Foods[s].Solution[param2change]-self.Foods[neighbor].Solution[param2change])
                    Solution.Solution[param2change] = int(bool(self.Foods[s].Solution[param2change]) ^ bool(rn & (self.Foods[s].Solution[param2change]|self.Foods[neighbor].Solution[param2change])))
                    
                    Solution.evaluate()
                    if Solution.Fitness < self.Foods[s].Fitness:
                        self.checkForBest(newSolution)
                        self.Foods[s] = Solution
                        self.Trial[s] = 0
                    else:
                        self.Trial[s] += 1
                s += 1
                if s == self.FoodNumber:
                    s = 0
            
            mi = self.Trial.index(max(self.Trial))
            if self.Trial[mi] >= self.Limit:
                self.Foods[mi] = SolutionABC(self.D)
                self.Foods[mi].evaluate()
                self.Trial[mi] = 0
            avgFitness = sum([s.Fitness for s in self.Foods])/self.NP
            avgFeatures = sum([s.numActiveFeatures for s in self.Foods])/self.NP
            convergenceRates.append([avgFitness,avgFeatures,self.Best.Fitness,self.Best.numActiveFeatures])
        return self.Best,convergenceRates