import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import h5py


Um =  0.05
R = 1
boxSide = R * 2
M = 1
n = 20
Ntotal = n**3
offset = boxSide / n


currentXCoord = 0
currentYCoord = 0
currentZCoord = 0
partXCoord = np.array([])
partYCoord = np.array([])
partZCoord = np.array([])

for i in range(0, n):
    for j in range(0, n):
        for z in range(0, n):
            partXCoord = np.append(partXCoord, i*offset)
            partYCoord = np.append(partYCoord, j*offset)
            partZCoord = np.append(partZCoord, z*offset)

partXCoord = partXCoord - np.median(partXCoord)
partYCoord = partYCoord - np.median(partYCoord)
partZCoord = partZCoord - np.median(partZCoord)

# Generation of the desired density profile
newXCoord = np.array([])
newYCoord = np.array([])
newZCoord = np.array([])

oldRadius = np.sqrt(partXCoord**2 + partYCoord**2 + partZCoord**2)
newRadius = oldRadius * np.sqrt(oldRadius)

for i in range(len(oldRadius)):
    if (oldRadius[i] <= 1.):
        newXCoord = np.append(newXCoord, partXCoord[i] * np.sqrt(oldRadius[i]))
        newYCoord = np.append(newYCoord, partYCoord[i] * np.sqrt(oldRadius[i]))
        newZCoord = np.append(newZCoord, partZCoord[i] * np.sqrt(oldRadius[i]))

Ntotal = len(newXCoord)
newXCoord.shape = (Ntotal, 1)
newYCoord.shape = (Ntotal, 1)
newZCoord.shape = (Ntotal, 1)
Coordinates = np.concatenate((newXCoord, newYCoord, newZCoord), axis = 1)
ID = np.linspace(1, Ntotal, Ntotal, dtype = int)
Velocities = np.zeros_like(Coordinates)

m = M / Ntotal
internalEnergyPart = m * Um 
partEnergies = np.zeros(Ntotal)
partEnergies += internalEnergyPart

# Create hdf5
filename = "ICs.hdf5"
hf = h5py.File(filename, 'w')

header = hf.create_group("Header")

massvec = np.zeros(1)
massvec[0] = M / Ntotal 

numberOfPart = np.zeros(1)
numberOfPart[0] = Ntotal

header.attrs['NumPart_ThisFile']    = numberOfPart
header.attrs['MassTable']           = massvec
header.attrs['Time']                = 0
header.attrs['Redshift']            = 0
header.attrs['NumPart_Total']       = numberOfPart
header.attrs['NumFilesPerSnapshot'] = 1
header.attrs['BoxSize']             = 1.0
header.attrs['Omega0']              = 1.0
header.attrs['OmegaLambdda']        = 0.
header.attrs['HubbleParam']         = 0.7
header.attrs['Flag_Entropy_ICs']    = 0
header.attrs['NumPart_Total_HighWord'] = np.zeros(1)

PartType0 = hf.create_group("PartType0")
PartType0.create_dataset("Coordinates", data = Coordinates)
PartType0.create_dataset("ParticleIDs", data = ID)
PartType0.create_dataset("Velocities", data = Velocities)
PartType0.create_dataset("InternalEnergy", data = partEnergies)

hf.close()
