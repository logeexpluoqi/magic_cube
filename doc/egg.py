from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure()
ax = fig.add_subplot(projection = '3d')
[x, t] = np.meshgrid(np.array(range(25)) / 24.0,
                     np.arange(0, 575.5, 0.5) / 575 * 20 * np.pi + 4*np.pi)
p = (np.pi / 2) * np.exp(-t / (8 * np.pi))
change = np.sin(15*t)/1500
u = 1 - (1 - np.mod(3.3 * t, 2 * np.pi) / np.pi) ** 4 / 2 + change
y = 2 * (x ** 2 - x) ** 2 * np.sin(p)
r = u * (x * np.sin(p) + y * np.cos(p))
h = u * (x * np.cos(p) - y * np.sin(p))
c = cm.get_cmap('Reds')
plt.axis('off')
surf = ax.plot_surface(r * np.cos(t), r * np.sin(t), h, rstride=1, cstride=1,
                       cmap=c, linewidth=0, antialiased=True)
plt.show()
