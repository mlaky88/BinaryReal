#!/usr/bin/env python2
import random
import sys
import math
from readdata import *

weightRelevance = 0.5 # maximize
weightRedundancy = 0.5 # minimize


def findOccurence(j,f,c,Data):
	count = 0
	
	for i in range(len(Data)):
		if Data[i][j] == f and Data[i][-1] == c:
			count += 1
	#print "Count {0}".format(float(count)/len(Data))
	return float(count)/len(Data)

def findOccurenceFeats(feature1,feature2,f1,f2,Data):
	count = 0
	for i in range(len(Data)):
		if Data[i][feature1] == f1 and Data[i][feature2] == f2:
			count += 1
	#print "Count {0}".format(float(count)/len(Data))
	return float(count)/len(Data)

def FeatureToClassMI(F,Data,H):
	C = F.pop()
	fi = 0
	FMI = []
	
	for feature in F:
		#print "Doing feature {0}".format(fi+1)
		mi = 0
		for v in feature:
			
			for cLabel in C:
				#print v,
				#print cLabel
				probxy = findOccurence(fi,v,cLabel,Data)
				if probxy == 0: 
					continue
				postProbx = float(H[fi][v])/len(Data)
				postProby = float(H[-1][cLabel])/len(Data)
				#print postProbx,postProby
				mi += probxy*math.log(probxy/(postProbx*postProby),2)
		fi += 1
		FMI.append(mi)
		#print "mi={0}".format(mi)
		
	return FMI

def FeatureToFeatureMI(F,Data,H):
	FMI = [[0 for i in range(len(F))] for i in range(len(F))]

	fi = 0
	for feature1 in range(len(F)):
		for feature2 in range(feature1+1,len(F)):
			#print "Doing features {0} and {1}".format(feature1+1,feature2+1)
			mi = 0
			for f1 in F[feature1]:
				for f2 in F[feature2]:
					#print f1,
					#print f2
					probxy = findOccurenceFeats(feature1,feature2,f1,f2,Data)
					if probxy == 0:
						continue
					postProbx = float(H[feature1][f1])/len(Data)
					postProby = float(H[feature2][f2])/len(Data)
					#print postProbx,postProby
					mi+= probxy*math.log(probxy/(postProbx*postProby),2)
			#print "mi={0}".format(mi)
			FMI[feature1][feature2] = mi
			FMI[feature2][feature1] = mi
	return FMI
	
		





#discretizeTransform(database) #if database has any continous data
#quit()

#print F
#print Data


