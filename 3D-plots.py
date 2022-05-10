#Packages
import h5py
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import pi
from scipy.optimize import curve_fit as fit
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D



#Plot style:
plt.style.use('dark_background')
title = '.png'



#Data directory:
datadir = 'data/snaps/'



#Creating folders for the output image.
savedir = 'output/'

files = os.listdir(datadir+".")
files.sort()
for i,file in enumerate(files):    #Importing data (PartType0 - Gas, PartType1 - DM, PartType2 - baryons)
    f = h5py.File(datadir+file, "r")
    group = f["PartType0"]
    data = group["Coordinates"][()]
    vel = group["Velocities"][()]
    
    #Plotting the initial conditions of both galaxies:
    fig = plt.figure(figsize=(12,5),dpi=100)
    #fig.suptitle(title)
    plt.rcParams['grid.color'] = (0.65, 0.65, 0.65, 0.65)

    # 1st subplot
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    plot1 = ax.scatter3D(data[:,0],data[:,1],data[:,2],c=vel[:,0],cmap="viridis",s=0.2,alpha=0.6)
    ax.set_axisbelow(True)
    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    ax.set_zlim(-1,1)
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))

    # 2nd subplot
    ax = fig.add_subplot(1, 2, 2)
    ax.grid(alpha=0.6)
    plot = ax.scatter(data[:,0],data[:,1],s=1,c=vel[:,0],cmap="viridis",alpha=0.6)
    cbar = fig.colorbar(plot, ax = ax)
    cbar.set_label('$V_x$', rotation=0)
    ax.set_axisbelow(True)
    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    
    plt.savefig(savedir+str(i)+".png", bbox_inches = 'tight')
    #plt.show()



#ANIMATION:
im1 = Image.open(savedir+'0.png')
images = []

for k in range(1, 15):
    path = savedir + str(k) + '.png'
    images.append(Image.open(path))

im1.save('gif.mp4', save_all=True, append_images=images, duration=400, loop=2)
