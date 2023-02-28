import os
import os
import matplotlib.pyplot as plt
import random
import time
times =  time.localtime()



folder_path = 'C:\\Users\\Alex\\Downloads\\snakes'  # Replace with the path to your folder

for root, dirs, files in os.walk(folder_path):
     for file in files:
          if 'body' in file:  # Only process files that contain "body" in their filename
               file_path = os.path.join(root, file)
               os.remove(file_path)



     
from parallelHillCilmber import PARALLEL_HILL_CLIMBER
evolutions = []
for i in range(5):
    
    phc = PARALLEL_HILL_CLIMBER() 
    phc.Evolve()

    phc.save_best(times)
    evolutions.append(phc.bestOfGens)



for root, dirs, files in os.walk(folder_path):
     for file in files:
          if 'body' in file:  # Only process files that contain "body" in their filename
               file_path = os.path.join(root, file)
               os.remove(file_path)
