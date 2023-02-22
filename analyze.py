import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load('data/backLegSensorValues.npy')

#np.save('data/frontLegSensorValues.npy', frontLegSensorValues)
#frontLegSensorValues = np.load('data/frontLegSensorValues.npy')

plt.plot(backLegSensorValues, label='Back Leg', linewidth=1.5)
plt.plot(frontLegSensorValues, label='Front Leg')
plt.legend(loc='upper right')
plt.show()
