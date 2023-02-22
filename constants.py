import numpy as np
import random as rand
factor = 10

if (1):
    gens = 3
    population = 2
    sensneuronNum = 6
    motorneuronNum = 10
    jointr = 0.5
    gravity_x = 0
    gravity_y = 0
    gravity_z = -9.8
    steps = 1000
    strenMax = 100
    sleep_time = 1/20000
    amplitude = np.pi/8
    frequency = 5
    phaseOffset = 0
    bl_amplitude = np.pi/8
    bl_frequency = 5
    bl_phaseOffset = 0
    fl_amplitude = np.pi/4
    fl_frequency = 10
    fl_phaseOffset = np.pi/4
else:
    gens = random.randint(1, factor)
    population = random.randint(1, factor)
    sensneuronNum = random.randint(1, factor)
    motorneuronNum = random.randint(1, factor)
    jointr = random.random()
    gravity_x = 0
    gravity_y = 0
    gravity_z = -9.8
    steps = 1000
    strenMax = random.randint(1, 10*factor)
    sleep_time = 1/2000
    amplitude = np.pi/8
    frequency = random.randint(1, factor)
    phaseOffset = 0
    bl_amplitude = np.pi/8
    bl_frequency = random.randint(1, factor)
    bl_phaseOffset = 0
    fl_amplitude = np.pi/4
    fl_frequency = random.randint(1, factor)
    fl_phaseOffset = np.pi/4


