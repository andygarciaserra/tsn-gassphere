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
fig,axs = plt.subplots(2,1,sharex=True,figsize=(12,15),gridspec_kw={'height_ratios': [3, 1]})
fig.subplots_adjust(hspace=0)
axs[0].set_xlim([0,3])
axs[0].set_ylabel('Energy', fontsize=25)
axs[0].plot(t,intengy,linewidth=3,color='b',label='Internal',ls='-.')
axs[0].plot(t,potengy,linewidth=3,color='r',label='Potential',ls='-.')
axs[0].plot(t,kinengy,linewidth=3,color='g',label='Kinetic',ls='-.')
axs[0].plot(t,totengy,linewidth=3,color='k',label='Total',ls='-.')
axs[0].legend(prop={'size': 25})
axs[0].tick_params(axis='both', which='major', labelsize=25)
axs[1].plot(t,totfrac,linewidth=3,color='k',label='MFV',ls='-.')
axs[1].set_xlabel('t (Gyrs)', fontsize=25)
axs[1].set_ylabel(r'$\left( \Delta E_{tot} \ \  / \ \  \vert E_{tot,0} \vert \right) \  (\%)$', fontsize=25)
axs[1].legend(prop={'size': 25})
axs[1].tick_params(axis='both', which='major', labelsize=25)
plt.tight_layout()
plt.savefig('energiess.png',dpi=100)
plt.show()

