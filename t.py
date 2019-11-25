import numpy as np
import matplotlib.pyplot as plt

vector = np.random.rand(10,1)
#vector = np.random.uniform(low = 10, high = 1000, size = 10)
povp = sum(vector)/10
sd = np.sqrt(sum((vector - povp)**2)/10)
plt.plot(vector, color = "black")
plt.xlabel("Vzorec")
plt.ylabel("Amplituda")
plt.axhline(y=povp, color='r')
plt.axhline(y=povp + sd, color='b')
plt.axhline(y=povp - sd, color='b')
plt.show()