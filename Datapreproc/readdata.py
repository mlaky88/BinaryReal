import collections

def performRead(Matrix):
	X = [[0 for i in range(len(Matrix))] for i in range(len(Matrix[0]))]

	i = 0
	for row in Matrix:
		j = 0
		for col in row:
			X[j][i] = col
			j+=1
		i+=1

	H = [collections.Counter(x) for x in X]
	X = [list(set(x)) for x in X]	
	return X,H

def ReadData(FileName):
	DataMatrix = []
	arrayLength = []
	for i in range(2):
		FileHandle = open(FileName[i], 'r')		
		try:
			for line in FileHandle:
				temp = []
				for val in line.split(","):
					temp.append(val.split("\n")[0])
					
				DataMatrix.append(temp)
			arrayLength.append(len(DataMatrix))
		except:
			raise 
	
	n = arrayLength[0]
	'''for i in range(len(DataMatrix)):
		print DataMatrix[i]
		if i+1 == n:
			print "--------------"
	'''
	unique = []
	#print DataMatrix[0]
	#quit()
	for feature in range(len(DataMatrix[0])):
		#print feature
		#print(set([row[feature] for row in DataMatrix]))
		#print([row[feature] for row in DataMatrix])
		unique.append(list(set([row[feature] for row in DataMatrix])))
		unique[feature].sort()
		#print unique
		#exit(1)

	j = 0
	for feature in unique:
		#print "Doing feature", feature
		for featureValue in feature:
			for row in range(len(DataMatrix)):
				#print row,j
				#print feature.index(featureValue)
				if DataMatrix[row][j] == featureValue:
					DataMatrix[row][j] = feature.index(featureValue)
		j += 1
	

	'''for i in range(len(DataMatrix)):
		print DataMatrix[i]
		if i+1 == n:
			print "--------------"
	'''
	DataMatrixLearn = DataMatrix[0:n]
	DataMatrixTest = DataMatrix[n:]
	#print DataMatrixLearn
	#print DataMatrixTest
	X,H = performRead(DataMatrixLearn)
	#print "DataMatrixLearn",DataMatrixLearn
	#print "X",X
	#print "H",H
	return X,H,DataMatrixLearn,DataMatrixTest