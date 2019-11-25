import sys
import numpy as np
import csv


def processAttribute(token):
    unqValuesAttr = list()
    print("Processing attribute {}".format(token[1]))
    attrValues = token[2]
    tokenizedAttrs = token[2].split(",")
    for aV in tokenizedAttrs:
        a = aV.replace("{","").replace("}","").replace("\n","")
        unqValuesAttr.append(a)
    #print(unqValuesAttr)
    return unqValuesAttr

def getAttributes(fileHandle):
    attrList = list()
    for line in fileHandle:
        #print ("Line:", line)
        token = line.split(" ")
        #print(token)
        #print("Token", token[0])
        if token[0] == "@attribute":
            attrList.append(processAttribute(token))            
        elif token[0] == "@data\n":
            #print("Position at :" , fileHandle.tell())
            break
    return attrList

def getData(fileHandle):
    #print("Getting data",fileHandle.tell())
    data = list()
    #fileHandle.seek(0)
    for line in fileHandle:
        data.append(line.split(","))
    return data

def parse(FileName):
    fileHandle = open(FileName, 'r')		
    attr = getAttributes(fileHandle)
    #print(attr)
    data = getData(fileHandle)
    fileHandle.close()
    DataMatrix = [[0 for i in range(len(data[0]))] for j in range(len(data))]
    print(len(DataMatrix),len(DataMatrix[0]))
    for idx,obs in enumerate(data):
        #print ("Doing observation ", obs)
        for i in range(len(obs)):
            #print ("attr",attr[i])
            #print ("obs",obs[i])
            val = attr[i].index(obs[i].replace("\n",""))
            DataMatrix[idx][i] = val
    return DataMatrix
    
def separate(data,proc=0.7):
    y = [row[-1] for row in data]
    allClasses = list(set(y))
    np.random.seed(42)
    train = list()
    test = list()
    for c in allClasses:
        print("Separating for class {}".format(c))
        oneClass = [idx for idx,val in enumerate(y) if val == c]
        print(len(oneClass))
        selectedTrainForClass = np.random.choice(oneClass,int(proc*len(oneClass)),replace=False).tolist()
        selectedTestForClass = list(oneClass.copy())
        print(len(selectedTrainForClass))
        for val in selectedTrainForClass:
            selectedTestForClass.remove(val)
            train.append(data[val])

        for val in selectedTestForClass:
            test.append(data[val])
    assert len(train)+len(test) == len(data)
    return train,test

def writeToFile(data,FileName,typedata):
    FileName = FileName.replace(".arff","-"+typedata+"-processed.arff")
    fileHandle = open(FileName, 'w')
    wr = csv.writer(fileHandle,delimiter=",")

    for datarow in data:
        wr.writerow(datarow)
    fileHandle.close()

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Error! Supply discretized .arff file to process")
    DataMatrix = parse(sys.argv[1])
    train,test = separate(DataMatrix)
    writeToFile(train,sys.argv[1],"train")
    writeToFile(test,sys.argv[1],"test")


    
    	

