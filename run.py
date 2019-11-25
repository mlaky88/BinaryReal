#!/usr/bin/env python
import sys
import math
import numpy
import json
import random as rnd

from Datapreproc.Datapreproc  import *

from sklearn import tree
from sklearn import svm
from sklearn import neighbors
from sklearn.model_selection import cross_val_score

#sys.path.append('libsvm/python/')
#from svmutil import *

classifier='knn'


def evaluateSolution(X,MatrixTrain,MatrixTest):
    trainSet = []
    testSet = []
    for i in range(len(X)):            
        if X[i] > 0.5:
            trainColumn = [[row[i]] for row in MatrixTrain]
            testColumn = [[row[i]] for row in MatrixTest]

            if len(trainSet) < 1:
                trainSet = numpy.array(trainColumn)
                testSet = numpy.array(testColumn)
            else:
                trainSet = numpy.hstack((trainSet,numpy.array(trainColumn)))
                testSet = numpy.hstack((testSet,numpy.array(testColumn)))

    if classifier == 'svm':
        clf = svm.SVC(kernel='linear',decision_function_shape='ovo',random_state=42)
    elif classifier == 'knn':
        clf = neighbors.KNeighborsClassifier(n_neighbors=5, weights='distance')
    elif classifier == 'dt':
        clf = tree.DecisionTreeClassifier(random_state=42)
    else:
        print("Unknown classifier selected")
        quit()
    

    trainLabels = [row[len(MatrixTrain[0])-1] for row in MatrixTrain]
    testLabels = [row[len(MatrixTest[0])-1] for row in MatrixTest]
    #trainSet =  [row.tolist() for row in trainSet] 
    #testSet =  [row.tolist() for row in testSet] 
    #svmProb = svm_problem(trainLabels,trainSet)
    #svmParam = svm_parameter("-s 0 -t 0 -b 0 -q")
    #svmModel = svm_train(svmProb,svmParam)
    #p_labs, p_acc, p_vals = svm_predict(testLabels, testSet, svmModel,'-b 0 -q')

    clf = clf.fit(trainSet, trainLabels)
    predLabels = clf.predict(testSet)
    #return p_acc[0]

    acc = [a-b for a,b in zip(testLabels,predLabels)]
    
    return float(acc.count(0))/len(acc)




def processResults(Archive):
    Archive.sort(key = lambda  p: p.numActiveFeatures)
    XX = dict()
    XY = dict()
    rA = []
    for p in Archive:
        p.toString()
        res = evaluateSolution(p.Solution,DataLearn,DataTest)
        if p.numActiveFeatures in XX:
            XX[p.numActiveFeatures]+=res
            XY[p.numActiveFeatures]+=1
        else:
            XX[p.numActiveFeatures]=res
            XY[p.numActiveFeatures]=1
        rA.append([res,p.numActiveFeatures])

    res = evaluateSolution([1 for i in range(Archive[0].D)],DataLearn,DataTest)
    XX[Archive[0].D]=res
    XY[Archive[0].D]=1
    print "---------Classification---------"
    for r in rA:
        print (r)
    print "+++++++++Overall+++++++++"
    for key in sorted(XX):
        print "Number of features {}({}) ".format(key,XY[key]),
        print XX[key]/XY[key]



def FilterFSNew(FeatureVector):
    relevance = 0
    redundancy = 0
    #print FeatureVector
    selectedFeaturesIdx = [i for i,v in enumerate(FeatureVector) if v >= 0.5]
    if len(selectedFeaturesIdx) < 1:
        return float('inf')#10**5 #Something really big
    
    #print selectedFeaturesIdx
    nRelevance = math.sqrt(sum([rel**2 for rel in FC]))
    nRedundancy = 0
    M = len(FeatureVector)
    for m in range(M-1):
	    for j in range(m+1,M):
		    nRedundancy += FF[m][j]**2

    nRedundancy = math.sqrt(nRedundancy)

    for i in range(len(selectedFeaturesIdx)):
        relevance += FC[selectedFeaturesIdx[i]]

    
    for k in range(len(selectedFeaturesIdx)):
        for l in range(len(selectedFeaturesIdx)):
            if k == l:
                continue
            else:
                redundancy += FF[selectedFeaturesIdx[k]][selectedFeaturesIdx[l]]

    beta = 1.0
    relevance /= nRelevance
    redundancy /= nRedundancy

    #print relevance,redundancy
    fit = relevance - beta * redundancy
    return -fit
    


def FilterFS(FeatureVector):
    Rel1 = 0
    Red1 = 0
    selectedFeatures = []
    #for i in range(18):
        #for j in range(18):
        #    print (FF[i][j]),
        #print

    '''FeatureVector = [0 for i in range(18)]
    FeatureVector[0] = 1
    FeatureVector[1] = 1
    FeatureVector[2] = 1
    FeatureVector[5] = 1'''
    
    for i in range(len(FeatureVector)):
        if FeatureVector[i] > 0.5: # Feature is selected
            selectedFeatures.append(i)
    #print FeatureVector,selectedFeatures
    
    for i in range(len(selectedFeatures)):
        Rel1 += FC[selectedFeatures[i]]
        for j in range(i+1,len(selectedFeatures)):
            #print(i,j,selectedFeatures[i],selectedFeatures[j])
            Red1 += FF[selectedFeatures[i]][selectedFeatures[j]]
    
    if len(selectedFeatures) == 0:
        return float('inf')
    print (-Rel1-Red1)
    #exit(1)
    #Maximize relevance, minimize redundancy
    #return (Red1)
    return -(Rel1-Red1)

def WrapperFS(FeatureVector):
    trainSet = []
    trainLabels = [row[len(DataLearn[0])-1] for row in DataLearn]
    
    selectedFeaturesIdx = [i for i,v in enumerate(FeatureVector) if v >= 0.5]
    if len(selectedFeaturesIdx) < 1:
        return float('inf')#10**5 #Something really big


    for i in range(len(FeatureVector)):
        if FeatureVector[i] >= 0.5:
            trainColumn = [[row[i]] for row in DataLearn]
            #print (trainColumn)
            if len(trainSet) < 1:
                trainSet = numpy.array(trainColumn)
            else:
                trainSet = numpy.hstack((trainSet,numpy.array(trainColumn)))


    assert len(trainLabels) == len(trainSet)
    if classifier == 'svm':
        clf = svm.SVC(kernel='linear',decision_function_shape='ovr',random_state=42)
    elif classifier == 'knn':
        clf = neighbors.KNeighborsClassifier(n_neighbors=10, weights='distance')
    elif classifier == 'dt':
        clf = tree.DecisionTreeClassifier(random_state=42)
    else:
        print("Unknown classifier selected")
        quit()
    scores = cross_val_score(clf, trainSet, trainLabels, cv=5,n_jobs=-1)
    #Return error of cross-validation
    return 100-(scores.mean()*100)
    
def dumpConvergenceToFile(data,fileName):
    fileHandle = open(fileName,'w') 
    fileHandle.write("Generation avgFitness avgFeatures minFitness minFeatures (of bestsolution)\n")
    for idx,data in enumerate(data):
        #print idx,data
        fileHandle.write(str(idx+1)+" "+' '.join(str(value) for value in data)+"\n")
    fileHandle.close()


def ReadCmdParameters(arg, argLen):
    cmd = {'np': '30', 'maxg': 500, 'algorithm': 'de', 'seed': 42, 'learn': '', 'test': '', 'coding': 'real', 'compute': False, 'classifier':'svm','evaltype':'wrapper','jsonfile':''}
    for i in range(1,argLen):
        if arg[i] == "-np":
            cmd['np'] = int(arg[i+1])
        if arg[i] == "-maxg":
            cmd['maxg'] = int(arg[i+1])
        if arg[i] == "-algorithm":
            cmd['algorithm'] = arg[i+1]
        if arg[i] == "-seed":
            cmd['seed'] = int(arg[i+1])
        if arg[i] == "-learn":
            cmd['learn'] = arg[i+1]
        if arg[i] == "-test":
            cmd['test'] = arg[i+1]
        if arg[i] == "-coding":
            cmd['coding'] = arg[i+1]
        if arg[i] == "-classifier":
            cmd['classifier'] = arg[i+1]   
        if arg[i] == "-compute":
            cmd['compute'] = True                           
        if arg[i] == "-evaltype":
            cmd['evaltype'] = arg[i+1]
        if arg[i] == "-jsonfile":
            cmd['jsonfile'] = arg[i+1]                    
    return cmd

cmd = ReadCmdParameters(sys.argv,len(sys.argv))
'''
NP = int(sys.argv[1])
MaxG = int(sys.argv[2])
algorithm = sys.argv[3]
seed = int(sys.argv[4])
databaseLearn = sys.argv[5]
databaseTest = sys.argv[6]
coding = sys.argv[7]
#jsonFile = sys.argv[8]
#classifier = sys.argv[9]
'''


'''print H
print H[0][1]
print H[0][2]
print H[0][3]
print len(H)
'''
#print DataLearn

#print evaluateSolution([1 for i in range(14)],DataLearn,DataTest)
#quit()

###################################
if cmd['compute'] == True:
    F,H,DataLearn,_ = ReadData([cmd['learn'],cmd['test']])
    #for j in DataTest:
    #    DataLearn.append(j)
    FC = FeatureToClassMI(F,DataLearn,H)
    FF = FeatureToFeatureMI(F,DataLearn,H)
    data = {}
    data['FF'] = FF
    data['FC'] = FC
    with open('data.json','w') as data_file:
        json.dump(data,data_file)
    quit()

###################################

F,H,DataLearn,DataTest = ReadData([cmd['learn'],cmd['test']])
EvalType = cmd['evaltype']
EvalFunction = []
FC = []
FF = []

if EvalType == "wrapper":
    EvalFunction = WrapperFS    
elif EvalType == "filter":
    EvalFunction = FilterFSNew
    data={}
    if cmd['compute'] == False:
        with open(cmd['jsonfile']) as data_file:
            data = json.load(data_file)
            FF = data['FF']
            FC = data['FC']
else:
    print ("Unknown feature selection method! Quiting!")
    quit()


D = len(DataLearn[0])-1
print D
rnd.seed(cmd['seed'])
coding = cmd['coding']
algorithm = cmd['algorithm']
NP = cmd['np']
MaxG = cmd['maxg']

alg = []

if coding.upper() == "BIN":
    from binary.binaryabc import *
    from binary.binaryde import *
    from binary.binarypso import *
    from binary.binaryga import *

    #from binary.binaryabcold import *
    #from binary.binarydeold import *
elif coding.upper() == "REAL":
    from real.realabc import *
    from real.realde import *
    from real.realpso import *
    from real.realga import *

if algorithm.upper() == "ABC":
    SolutionABC.FuncEval = staticmethod(EvalFunction)
    if coding.upper() == "BIN":
        alg = bMDisABC(NP,D,MaxG) #OK
    else:
        alg = ABC(NP,D,MaxG) #OK
elif algorithm.upper() == "DE":
    SolutionDE.FuncEval = staticmethod(EvalFunction)
    if coding.upper() == "BIN":
        alg = bDE(NP, D, MaxG) #OK
    else:
        alg = DE(NP, D, MaxG) #OK
elif algorithm.upper() == "PSO":
    Particle.FuncEval = staticmethod(EvalFunction)
    if coding.upper() == "BIN":
        alg = bPSO(NP, D, MaxG) #OK
    else:
        alg = PSO(NP, D, MaxG) #OK
elif algorithm.upper() == "GA":
    Chromosome.FuncEval = staticmethod(EvalFunction)
    if coding.upper() == "BIN":
        alg = bGA(NP,D,MaxG) #OK
    else:
        alg = GA(NP,D,MaxG) #OK

#binary DE https://www.sciencedirect.com/science/article/pii/S1568494615006778


#alg = bMDisABC(NP,D,MaxG)
    

restarts = 30
results = []
import time
for res in range(restarts):
   bestRes,convRes = alg.run()
   fileName = "converge/"+cmd['jsonfile'].replace("json/","")+"-"+cmd['algorithm']+"-"+cmd['coding']+"-"+str(cmd['seed'])+"-"+str(cmd['np'])+"-"+cmd['classifier']+"-"+cmd['evaltype']+"-"+str(res+1)+".conv"
   dumpConvergenceToFile(convRes,fileName)
   results.append(bestRes)
   alg.reset()
   time.sleep(0.1)
   rnd.seed(rnd.randint(0,10000))



print("#################################################")
processResults(results)


