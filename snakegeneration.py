import pyrosim.pyrosim as pyrosim
import pybullet_data
import constants as c
import pybullet as p
import time
import os
from world import WORLD
from snake import SNAKE
from snakeSimulation import SNAKE_SIMILATION

class RANDOM_GEN:
     def __init__(self, id):
          self.myID = id


     def Generate_And_Run(self):
          sim = SNAKE_SIMILATION(self.myID) #Generate
          sim.Run()                     #Run/Simulate
               
          os.system("del body*.urdf")
          os.system("del brain*.urdf")
          

          
