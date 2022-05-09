# PACKAGES
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import h5py
import csv





# DATA IMPORTING
filename = 'data/energy.txt'
data = np.loadtxt(filename)
t = data[:,0]
intengy = data[:,1]
potengy = data[:,2]
kinengy = data[:,3]
totengy = intengy + potengy + kinengy 
totfrac = ((totengy - totengy[0])/ np.abs(totengy[0]))*100



# PLOTTING
fig,axs = plt.subplots(2,1,sharex=True,gridspec_kw={'height_ratios': [3, 1]})
fig.subplots_adjust(hspace=0)
axs[0].set_xlim([0,3])
axs[0].plot(t,intengy,color='b',ls='-.')
axs[0].plot(t,potengy,color='r',ls='-.')
axs[0].plot(t,kinengy,color='g',ls='-.')
axs[0].plot(t,totengy,color='k',ls='-.')
axs[1].plot(t,totfrac,color='k',ls='-.')
plt.show()

print(totengy[0])



