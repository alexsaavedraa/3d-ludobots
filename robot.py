import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
from sensor import SENSOR
from motor import MOTOR
import constants as c
import math




class ROBOT:
     def __init__(self, solutionID, test, evolved):
          self.sensors = {}
          self.motors = {}
          self.robotId = p.loadURDF(f'body{solutionID}.urdf') 

          if test:
               if evolved:
                    self.nn = NEURAL_NETWORK(f'results/evolved/brain{solutionID}.nndf')
               else:
                    self.nn = NEURAL_NETWORK(f'results/random/brain{solutionID}.nndf')
          else:
               self.nn = NEURAL_NETWORK(f'brain{solutionID}.nndf')

          if not test:
               os.system(f'del brain{solutionID}.nndf')
               
          self.solutionID = solutionID
          self.totalStandReward = 0
          self.lastSpot = 0
          self.lastYUp = 0
     
     def Prepare_To_Sense(self):
          
          for linkName in pyrosim.linkNamesToIndices:
               self.sensors[linkName] = SENSOR(linkName)
     
     def Sense(self, i):
          for linkName in self.sensors:
               self.sensors[linkName].Get_Value(i)
     
     def Prepare_To_Act(self):
          for jointName in pyrosim.jointNamesToIndices:
               self.motors[jointName.decode('utf-8')] = MOTOR(jointName)
     
     def Act(self, i):
          for neuronName in self.nn.Get_Neuron_Names():
               if self.nn.Is_Motor_Neuron(neuronName):
                    jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                    if jointName in ["Torso_UpperRightLeg", "Torso_UpperLeftLeg"]:
                         desiredAngle = self.nn.Get_Value_Of(neuronName) * 1
                    elif jointName in ["UpperRightLeg_LowerRightLeg", "UpperLeftLeg_LowerLeftLeg"]:
                         desiredAngle = self.nn.Get_Value_Of(neuronName) * 0.5
                    elif jointName in ["LowerRightLeg_RightFoot", "LowerLeftLeg_LeftFoot"]:
                         desiredAngle = self.nn.Get_Value_Of(neuronName) * 0.2
                    else:
                         desiredAngle = self.nn.Get_Value_Of(neuronName) * 0.4
                    self.motors[jointName]
                    self.motors[jointName].Set_Value(self.robotId, desiredAngle)
          
          
          xPosition = p.getBasePositionAndOrientation(self.robotId)[0][0]
          yPosition = p.getBasePositionAndOrientation(self.robotId)[0][1]
          zPosition = p.getBasePositionAndOrientation(self.robotId)[0][2]

          if zPosition >= 2:
               self.totalStandReward += 10
               self.lastYUp = yPosition
          else:
               self.totalStandReward -= 5

     
     def Think(self):
          self.nn.Update()

     
     def Get_Fitness(self):
          basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
          basePosition = basePositionAndOrientation[0]
          xPosition = basePosition[0]
          yPosition = basePosition[1]
          zPosition = basePosition[2]
          

          fitness = 0

          yReward = self.lastYUp * 50
          fitness += yReward

         
          fitness += self.totalStandReward*.3/len(self.sensors)
      
        

          f = open(f'tmp{self.solutionID}.txt', "w")
          f.write(str(fitness))
          f.close()
          os.system(f'mv tmp{self.solutionID}.txt fitness{self.solutionID}.txt')

  
          






