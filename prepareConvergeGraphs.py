
import sys
import matplotlib.pyplot as plt

data = sys.argv[1]
#typeData = sys.argv[2]

with open(data,'rb') as f:
    content = f.readlines()

#print(content[0])


#print(content[0].split(','))
#print (names)

data = [row.split(',') for row in content]
nData = []
for row in data:
    nRow = []
    numInf = 0
    for v in row:
        val = float(v.strip('\n'))
        if val == float('inf'):
            numInf += 1
            val = 0
        nRow.append(val)
    nData.append(sum(nRow)/(len(nRow)-numInf))

'''plt.plot(nData)
plt.xlabel('Generation')
if typeData == "obj":
    plt.ylabel('Objective value')
elif typeData == "feats":
    plt.ylabel('Number of features')
plt.show()
'''
for v in nData:
    print v


