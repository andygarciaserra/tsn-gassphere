#Packages
import h5py
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi
from scipy.optimize import curve_fit as fit
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D

datadir = 'data/snaps/'

files = os.listdir(datadir+".")
files.sort()

f = h5py.File(datadir+files[0], "r")
group = f["PartType0"]
data = group["Coordinates"][()]
vel = group["Velocities"][()]   

"""
plot = plt.figure()
plt.grid(alpha=0.6)
plt.scatter(data[:,0],data[:,1],s=1,alpha=0.6)
plt.xlim(-1,1)
plt.ylim(-1,1)
plt.savefig('initial.png')
plt.show()
"""

fig = plt.figure(figsize=(5,5),dpi=150)
plt.rcParams['grid.color'] = (0.65, 0.65, 0.65, 0.65)
ax = fig.add_subplot()
ax.grid(alpha=0.6)
plot = ax.scatter(data[:,0],data[:,1],s=1,cmap="viridis",alpha=0.6)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_axisbelow(True)
ax.set_xlim(-1,1)
ax.set_ylim(-1,1)

plt.savefig("init.png", bbox_inches = 'tight')
plt.show()

