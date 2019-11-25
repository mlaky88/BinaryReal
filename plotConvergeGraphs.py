import sys
import matplotlib.pyplot as plt

data = sys.argv[1]
typeData = sys.argv[2]
dataset = sys.argv[3]
coding = sys.argv[4]
typeFS = sys.argv[5]


with open(data,'rb') as f:
    content = f.readlines()


data = [row.split(',') for row in content]
data = [[float(v.strip('\n')) for v in row] for row in data]
columns = len(data[0])
plotStyle = ['b', 'r', 'k', 'g','b--','r--','k--','g--']

for i in range(columns):
    d = [row[i] for row in data]
    plt.plot(d,plotStyle[i])


if dataset == "all":
    plotTitle = "All datasets"
else:
    plotTitle = chr(ord(dataset[0])-32)+dataset[1:]

plt.title(plotTitle)
plt.xlabel('Generation')
if typeData == "obj":
    plt.ylabel('Objective value')
elif typeData == "feats":
    plt.ylabel('Number of features')


if columns == 8:
    plt.legend(('rDE', 'rPSO', 'rABC', 'rGA','bDE', 'bPSO', 'bABC', 'bGA'),loc='upper right')
else:
    plt.legend(('DE', 'PSO', 'ABC', 'GA'),loc='upper right')



if coding == "dummy":
    if typeData == "obj":
        plt.savefig("drawings/converge-obj-"+dataset+"-BR-"+typeFS+".png")
    elif typeData == "feats":
        plt.savefig("drawings/converge-feats-"+dataset+"-BR-"+typeFS+".png")
else:
    if typeData == "obj":
        plt.savefig("drawings/converge-obj-"+dataset+"-"+coding+"-"+typeFS+".png")
    elif typeData == "feats":
        plt.savefig("drawings/converge-feats-"+dataset+"-"+coding+"-"+typeFS+".png")


