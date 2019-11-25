
import sys

data = sys.argv[1]

with open(data,'rb') as f:
    content = f.readlines()

#print(content)

names = [row.split(' ')[0] for row in content]
#print (names)

ranks = [float(row.split(' ')[1].strip('\n')) for row in content]
#print (ranks)

fixedRanks=[max(ranks) - i + min(ranks) for i in ranks]
#print (fixedRanks)
for a,b in zip(names,fixedRanks):
    print a,b