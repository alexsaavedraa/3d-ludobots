import pyrosim.pyrosim as pyrosim
import pybullet as p
import numpy as np
import random
import os
import constants as c
from sensor import SENSOR
from motor import MOTOR
from robot import ROBOT
from pyrosim.neuralNetwork import NEURAL_NETWORK
import rotateNmap as rNm


green = ['Green','     <color rgba="0.0 1.0 0.0 1.0"/>']
blue  = ['Blue','     <color rgba="0.0 0.5 1.0 1.0"/>']
vector_dict = {'x': [1, 0, 0], '-x': [-1, 0, 0], 'y': [0, 1, 0], '-y': [0, -1, 0], 'z': [0, 0, 1], '-z': [0, 0, -1]}
to_opposite = {'x': '-x', '-x':'x', 'y': '-y', '-y': 'y', 'z': '-z', '-z': 'z'}
face_centers = {
    'x': [1.0, 0.5, 0.5],    # positive x face
    '-x': [0.0, 0.5, 0.5],    # negative x face
    'y': [0.5, 1.0, 0.5],    # positive y face
    '-y': [0.5, 0.0, 0.5],    # negative y face
    'z': [0.5, 0.5, 1.0],    # positive z face
    '-z': [0.5, 0.5, 0.0]     # negative z face
}
def validLoc(lst, block):
     ret = False
     for other in lst:
          if block.id != other.id:
               if block.parentId == other.parentId and block.direction == other.direction:
                    
                    return False
                    #print(f"\n the speeds and feeds are {other.id, block.id, block.direction, other.direction, other.parentId, block.parentId}\n a snake accepted \n")
               else:
                    pass

               
     print("a block has been allowed")
     return True


class block():
     def __init__(self, id, parId, parAx, limbtype, orientation, color, direction = 'y'):
          self.direction = direction
          self.id = id
          self.parentId = parId
          self.parent = f'Part{self.parentId}'
          self.parAx = parAx
          self.Ax = [0,0,0]
          self.limbtype = limbtype
          self.posn = [0,0,0]
          self.child = 0
          self.rotaX = orientation #[left, right]
          self.findAx()
          self.minSide = 25
          self.lwh = [0,0,0]
          self.dims()
          if color:
               self.color = blue
          else:
               self.color = green

     def __str__(self):
          return f'\n\n the current block is {self.id}\n the sides are {self.lwh} \n the orientation is {self.jointAx}\n the color is {self.color}\n, the direction is {self.direction}\n'
     def findAx(self):
          if self.limbtype == "dorsal":
               self.Ax = self.parAx 
          
          chooseAx = vector_dict[self.direction]# random.choice([[1,0,0], [0,1,0], [0,0,1]])
          self.jointAx =  " ".join(str(coord) for coord in chooseAx) 
     
     def dims(self):
          length = 1#random.randint(self.minSide,100)/100
          width = 1#random.randint(self.minSide,100)/100
          height = 1#random.randint(self.minSide,100)/100
          self.lwh = [length,width,height]


     
class SNAKE(ROBOT): 
     def __init__(self, id, num_parts, num_sensors):
          self.myID = id
          self.numParts = num_parts
          self.partBoundries = np.zeros((num_parts, 6)) #x bb, x bb, ybb, -ybb, T bb, bottom BB
          self.partslist = np.zeros((num_parts, 7)) #length,width,height,axX, axY, axZ, depth
          
          self.numSensors = num_sensors
          random.seed(id)
          self.isSensor = np.full((1,num_parts), False)[0]
          self.isSensor[random.sample(range(num_parts), num_sensors)] = True
          self.weights = np.random.rand(num_sensors,num_parts-1)*2-1
          self.minSide = 25 
          self.listparts = []
          self.Create_Body()
          self.Create_Brain()

          ROBOT.__init__(self, id, False, False)
          



     

     def Create_Body(self):
          pyrosim.Start_URDF(f'body{self.myID}.urdf')

          if self.isSensor[0]:
               color = green
          else:
               color = blue
          random.seed(self.myID)
          
          listofBlocks = [block(0, -1,vector_dict['y'], "dorsal", [0,1,0], self.isSensor[0])]    
          pos  = np.array(vector_dict[listofBlocks[0].direction])*np.array(listofBlocks[0].lwh) * .5 
          print("the very first block is ", listofBlocks[0]) 
          pyrosim.Send_Cube(name="Part0", pos=[0,0,0] , size=listofBlocks[0].lwh, color=color)
      
       
          
     
          for i in range(1,self.numParts):
               parent = random.choice(list(range(0,len(listofBlocks))))
               dir = random.choice(['x','y','z'])#, '-x', '-y', '-z'])        
               currbox = block(i, parent, vector_dict[dir], "dorsal", None, self.isSensor[i], dir)
               while(not(validLoc(listofBlocks, currbox))):
                    parent = random.choice(list(range(0,len(listofBlocks))))
                    dir = random.choice(['x','y','z'])#, '-x', '-y', '-z'])     
                    currbox = block(i, parent, vector_dict[dir], "dorsal", None, self.isSensor[i], dir)

               listofBlocks.append(currbox)


               print(f"the name is '{currbox.parent}_Part{i}")
               jointdir = np.array([0,0,0])
               if currbox.parentId == 0:
                    prevdir = np.array(face_centers[listofBlocks[parent].direction])
                    currdir = np.array(face_centers[currbox.direction])
                    if prevdir.all() == currdir.all():
                         prevdir = np.array(face_centers[to_opposite[listofBlocks[parent].direction]])
                    jointdir = currdir-prevdir
                    jointdir = np.array(listofBlocks[parent].lwh) * .5
                    print("the thing that i want to see is", np.logical_not((np.array(vector_dict[listofBlocks[parent].direction])).astype(int)))
                    pos  = np.array(vector_dict[currbox.direction])*np.array(currbox.lwh) *.5
                    
               else:
              
                    prevdir = np.array(face_centers[listofBlocks[parent].direction])
                    currdir = np.array(face_centers[currbox.direction])
                    if prevdir.all() == currdir.all():
                         prevdir = np.array(face_centers[to_opposite[listofBlocks[parent].direction]])
                    jointdir = currdir-prevdir
                    jointdir = jointdir *  currbox.lwh
                    pos  = np.array(vector_dict[currbox.direction])*np.array(currbox.lwh) * .5


               print(pos)
               pyrosim.Send_Joint(name = f'{currbox.parent}_Part{i}' , parent= currbox.parent , child = f'Part{i}' , type = "revolute", position = (jointdir), jointAxis = currbox.jointAx)
               pyrosim.Send_Cube(name=f'Part{i}', pos= pos , size= currbox.lwh, color=currbox.color) 
               #previous = [f'Part{i}', currbox.jointAx, width]
               print(currbox)
               print("\n the joint location is ", jointdir)

               

     
          
          self.listparts = listofBlocks
          pyrosim.End()

          

          #print(self.partBoundries)
     
     def gen_parts(self, part):
          pass# return posn, jointaxis, size, color


     
     def Create_Brain(self):
          pyrosim.Start_NeuralNetwork(f'brain{self.myID}.nndf')
          i = 0
          j = self.numSensors
          for part in range(self.numParts):
               #Sensor Neurons
               is_sensor = self.isSensor[part]
               if is_sensor:
                    pyrosim.Send_Sensor_Neuron(name = i , linkName = f'Part{part}')
                    i += 1
                    
               #Motor Neurons
               if part != self.numParts-1 and part != 0:
                    pyrosim.Send_Motor_Neuron( name = j , jointName = f'Part{self.listparts[part].parentId}_Part{self.listparts[part].id}')
                    j += 1

          for sensor in range(self.numSensors):
               for motor in range(self.numParts-1): #should be right
                    pyrosim.Send_Synapse( sourceNeuronName = sensor, targetNeuronName = motor+self.numSensors , weight = self.weights[sensor][motor] )
          pyrosim.End()
     
     def Act(self, i):
          for neuronName in self.nn.Get_Neuron_Names():
               if self.nn.Is_Motor_Neuron(neuronName):
                    jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                    desiredAngle = self.nn.Get_Value_Of(neuronName) * c.jointr
                    self.motors[jointName].Set_Value(self.robotId, desiredAngle)



     



