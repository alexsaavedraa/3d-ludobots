import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import random

from simulation import SIMULATION
from snake import SNAKE
from world import WORLD
import constants as c



class SNAKE_SIMILATION(SIMULATION):
     def __init__(self, id):
          self.Create_World()

          p.connect(p.GUI)
          p.configureDebugVisualizer(p.COV_ENABLE_GUI,0) 
          
          p.setAdditionalSearchPath(pybullet_data.getDataPath())
          
          p.setGravity(c.gravity_x,c.gravity_y,c.gravity_z)
          
          self.world = WORLD()

          random.seed(id)
          num_parts = random.randint(25,25)
          
          num_sensors = random.randint(1, max(num_parts-1,1))
          
          self.robot = SNAKE(id, num_parts, num_sensors)
          
          self.directOrGUI = "GUI"

          pyrosim.Prepare_To_Simulate(self.robot.robotId)
          
          self.robot.Prepare_To_Sense()
          self.robot.Prepare_To_Act()
          


     
     def Create_World(self):
          pyrosim.Start_SDF("world.sdf")
          pyrosim.End()

