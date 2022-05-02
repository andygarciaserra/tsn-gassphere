import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import h5py


internalEPerMass =  0.05
sphereRadius = 1
boxSide = sphereRadius * 2
totalMass = 1
sideParticleNumber = 20
totalParticleNumber = sideParticleNumber**3
offset = boxSide / sideParticleNumber


currentXCoord = 0
currentYCoord = 0
currentZCoord = 0
partXCoord = np.array([])
partYCoord = np.array([])
partZCoord = np.array([])

for i in range(0, sideParticleNumber):
    for j in range(0, sideParticleNumber):
        for z in range(0, sideParticleNumber):
            partXCoord = np.append(partXCoord, i*offset)
            partYCoord = np.append(partYCoord, j*offset)
            partZCoord = np.append(partZCoord, z*offset)

partXCoord = partXCoord - np.median(partXCoord)
partYCoord = partYCoord - np.median(partYCoord)
partZCoord = partZCoord - np.median(partZCoord)

#fig = plt.figure()
#ax = plt.axes(projection='3d')
#ax.scatter(partXCoord, partYCoord, partZCoord, color="black", s=0.25)
#plt.show()

# Generation of the desired density profile
newXCoord = np.array([])
newYCoord = np.array([])
newZCoord = np.array([])

oldRadius = np.sqrt(partXCoord**2 + partYCoord**2 + partZCoord**2)
newRadius = oldRadius * np.sqrt(oldRadius)

for i in range(len(oldRadius)):
    if (oldRadius[i] <= 1.):
        #if (oldRadius[i] < 0.0001):
        #    continue
        #phi = newRadius[i] / oldRadius[i]
        #newXCoord = np.append(newXCoord, partXCoord[i] * phi)
        newXCoord = np.append(newXCoord, partXCoord[i] * np.sqrt(oldRadius[i]))
        newYCoord = np.append(newYCoord, partYCoord[i] * np.sqrt(oldRadius[i]))
        newZCoord = np.append(newZCoord, partZCoord[i] * np.sqrt(oldRadius[i]))

totalParticleNumber = len(newXCoord)
newXCoord.shape = (totalParticleNumber, 1)
newYCoord.shape = (totalParticleNumber, 1)
newZCoord.shape = (totalParticleNumber, 1)
Coordinates = np.concatenate((newXCoord, newYCoord, newZCoord), axis = 1)
ID = np.linspace(1, totalParticleNumber, totalParticleNumber, dtype = int)
Velocities = np.zeros_like(Coordinates)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(newXCoord, newYCoord, newZCoord, color="black", s=0.25)
plt.show()

# Density profile

distances = np.sqrt(newXCoord**2 + newYCoord**2 + newZCoord**2)

particleMass = totalMass / len(distances)
shellNumber = 15
shellWidth = np.mean(distances) / shellNumber  
shellDensity = np.array([])
shellRadius = np.array([])

for i in range(shellNumber):
    numberOfParticles = 0
    for j in range(len(distances)):
        if ((distances[j] >= (i * shellWidth)) and (distances[j] <= ((i+1) * shellWidth))):
            numberOfParticles = numberOfParticles + 1
    shellRadius = np.append(shellRadius, (shellWidth*i + (shellWidth)/2))
    massOfParticles = numberOfParticles * particleMass
    shellDensity = np.append(shellDensity, (massOfParticles) / ((4/3)*np.pi*(((i+1)*shellWidth)**3 - (i*shellWidth)**3)))


fig, ax = plt.subplots(figsize=(20,15))
ax.plot(shellRadius[1:], shellDensity[1:], 'r.')
ax.plot(shellRadius[1:], 1/(2*np.pi*shellRadius[1:]), color="g")
#plt.gca().set_xscale("log")
plt.gca().set_yscale("log")
plt.show()

internalEnergyUnitMass = 0.05
particleMass = totalMass / totalParticleNumber
internalEnergyPart = particleMass * internalEnergyUnitMass
partEnergies = np.zeros(totalParticleNumber)
partEnergies += internalEnergyPart

# Create hdf5
filename = "evrardInitialConditions.hdf5"
hf = h5py.File(filename, 'w')

header = hf.create_group("Header")

massvec = np.zeros(1)
massvec[0] = totalMass / totalParticleNumber

numberOfPart = np.zeros(1)
numberOfPart[0] = totalParticleNumber

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
