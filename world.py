import pybullet as p

class WORLD:
     def __init__(self):
          self.planeId = p.loadURDF("groundplane.urdf")
          
          p.loadSDF("world.sdf")