import matplotlib.pyplot as plt
import numpy

data = numpy.genfromtxt("data.txt", delimiter=',')
date = numpy.genfromtxt("date.txt", delimiter=',', dtype="|S5")
print(data)
print(date)
plt.plot(date,data)
plt.show()

