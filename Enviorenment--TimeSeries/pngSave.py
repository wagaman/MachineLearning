import matplotlib.pyplot as plt
import math
import os
print(os.getcwd())

x_list = range(1,20)
y_list = range(1,20)

# draw
plt.figure(figsize=(13, 7))
plt.plot(x_list, y_list, color="red", linewidth=3)
plt.xlabel("")
plt.ylabel("R")
plt.title(u"x x")
plt.legend((u"图例",))

plt.ylim(0, 30)
plt.legend()
plt.savefig("D:/Programma/Environmentaltest/test.png")
#plt.show()
