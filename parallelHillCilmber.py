from snakegeneration import RANDOM_GEN
import constants as c
import copy
import os

class PARALLEL_HILL_CLIMBER:
     def __init__(self):
          
          os.system("del brain*.nndf")
          os.system("del fitness*.txt")
          self.nextAvailableID = 0
          self.parents = {}
          
          for i in range(c.population):
               self.parents[i] = RANDOM_GEN(self.nextAvailableID)
               self.nextAvailableID += 1
         

     def Evolve(self):
          
          self.Evaluate(self.parents)
          for currentGeneration in range(c.gens):
               self.Evolve_For_One_Generation()
     
     def Evolve_For_One_Generation(self):

          self.Spawn()
          print("spawned a beast")
          self.Mutate()
          self.Evaluate(self.children)
          self.Print()
          self.Select()
      

     
     def Spawn(self):
          self.children = {}
          for i in self.parents:
               self.children[i] = copy.deepcopy(self.parents[i])
               self.children[i].Set_ID(self.nextAvailableID)
               self.nextAvailableID += 1


     def Mutate(self):
          for i in self.children:
               self.children[i].Mutate()

     def Select(self):
          for i in self.parents:
               if self.children[i].fitness > self.parents[i].fitness:
                    self.parents[i] = self.children[i]
     
     def Show_Best(self):
          best_fitness = -float('inf')
          best = self.parents[0]
          for i in self.parents:
               if self.parents[i].fitness > best_fitness:
                    best = self.parents[i]
                    best_fitness = self.parents[i].fitness
          print(best_fitness)
          best.Start_Simulation("GUI")
          os.system(f'cp brain{best.myID}.nndf results/outputs/brain{best.myID}.nndf')
     
     def Evaluate(self, solutions):
          for p in range(c.population):
               solutions[p].Generate_And_Run() 
          for p in range(c.population):
               solutions[p].Wait_For_Simulation_To_End()
     
     def Print(self):
          print()
          for p in self.parents:
               print(self.parents[p].fitness, self.children[p].fitness)
          print()
