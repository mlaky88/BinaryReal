#!/usr/bin/env python
import sys
import math
import numpy
import json

from binaryabc import *
from binaryde import *
from binarypso import *
from binaryga import *
sys.path.append('../Datapreproc')
from Datapreproc  import *

from sklearn import tree
from sklearn import svm
from sklearn.decomposition import PCA



def evaluateSolution(X,MatrixTrain,MatrixTest):
    trainSet = []
    testSet = []
    #print (len(MatrixTrain))
    #print (len(MatrixTrain[0]))
    for i in range(len(X)):            
        #print i    
        if X[i] == 1:
            trainColumn = [[row[i]] for row in MatrixTrain]
            testColumn = [[row[i]] for row in MatrixTest]

            if len(trainSet) < 1:
                trainSet = numpy.array(trainColumn)
                testSet = numpy.array(testColumn)
            else:
                trainSet = numpy.hstack((trainSet,numpy.array(trainColumn)))
                testSet = numpy.hstack((testSet,numpy.array(testColumn)))

    #clf = svm.SVC(kernel='linear',decision_function_shape='ovo')
    clf = tree.DecisionTreeClassifier(random_state=42)

    trainLabels = [row[len(MatrixTrain[0])-1] for row in MatrixTrain]
    testLabels = [row[len(MatrixTest[0])-1] for row in MatrixTest]
    clf = clf.fit(trainSet, trainLabels)
    predLabels = clf.predict(testSet)

    acc = [a-b for a,b in zip(testLabels,predLabels)]
    return float(acc.count(0))/len(acc)




def processResults(Archive):
    Archive.sort(key = lambda  p: p.numActiveFeatures)
    XX = dict()
    XY = dict()
    for p in Archive:
        p.toString()
        res = evaluateSolution(p.Solution,DataLearn,DataTest)
        if p.numActiveFeatures in XX:
            XX[p.numActiveFeatures]+=res
            XY[p.numActiveFeatures]+=1
        else:
            XX[p.numActiveFeatures]=res
            XY[p.numActiveFeatures]=1

        #print res,
        #p.toString()
    res = evaluateSolution([1 for i in range(Archive[0].D)],DataLearn,DataTest)
    XX[Archive[0].D]=res
    XY[Archive[0].D]=1
    #print XX
    for key in sorted(XX):
        print "Number of features {} ".format(key),
        print XX[key]/XY[key]



def FilterFS(ParticlePosition):
    R1 = 0
    D1 = 0
    selectedFeatures = []
    for i in range(len(ParticlePosition)):
        if ParticlePosition[i] == 1: # Feature is selected
            selectedFeatures.append(i)
            
    for i in range(len(selectedFeatures)):
        D1 += FC[selectedFeatures[i]]
        for j in range(i+1,len(selectedFeatures)):
            R1 += FF[selectedFeatures[i]][selectedFeatures[j]]
    return -1*(D1-R1)

def labs(x):
    x = [-1 if i == 0 else 1 for i in x]    
    N = len(x)
    #print N
    enrg = 0
    for i in range(N-1):
        ss=0
        for j in range(N-1-i):
            ss += x[j]*x[j+1+i]
        enrg += (ss*ss)
    return enrg



NP = int(sys.argv[1])
D = int(sys.argv[2])
MaxG = int(sys.argv[3])
algorithm = sys.argv[4]
seed = int(sys.argv[5])
databaseLearn = sys.argv[6]
databaseTest = sys.argv[7]

F,H,DataLearn,DataTest = ReadData([databaseLearn,databaseTest])
FC = FeatureToClassMI(F,DataLearn,H)
FF = FeatureToFeatureMI(F,DataLearn,H)


#quit()
'''
Data = {}
with open('data.json', 'w') as outfile:
	Data['FC'] = FC
	Data['FF'] = FF
	
	json.dump(Data, outfile)
'''    
#with open('data.json') as data_file:
#    data_loaded = json.load(data_file)
    
#print data_loaded



#quit()



D = len(FC)
rnd.seed(seed)
alg = []

if algorithm.upper() == "ABC":
    SolutionABC.FuncEval = staticmethod(FilterFS)
    alg = bABC(NP,D,MaxG)
elif algorithm.upper() == "DE":
    SolutionDE.FuncEval = staticmethod(FilterFS)
    alg = bDE(NP, D, MaxG)
elif algorithm.upper() == "PSO":
    Particle.FuncEval = staticmethod(FilterFS)
    alg = bPSO(NP, D, MaxG)
elif algorithm.upper() == "GA":
    Chromosome.FuncEval = staticmethod(FilterFS)
    alg = bGA(NP,D,MaxG)

restarts = 2
results = []
import time
for res in range(restarts):
   bestRes = alg.run()
   results.append(bestRes)
   alg.reset()
   time.sleep(2)



print("#################################################")
processResults(results)


