# -*- coding: utf-8 -*-
"""
This file plots the environments saved in the simulated annealing optimization
"""

import pickle
import matplotlib.pyplot as plt
from functions_collision_detection import plot_polygon, plot_lights

def plot_env(env, title = ''):
  for room in env.roomList:
      plot_polygon(room.polygon)
      
  for door in env.doorList:
          plot_polygon(door.polygon)
  
  for furniture in env.furnitureList:
      plot_polygon(furniture.polygon)
      
  for light in env.lightList:
      plot_lights(light.point)
  plt.title(title)
  plt.show()

## ----------------------------------------------------------------------------
##  ---------------------   USER INPUT ----------------------------------------
#-----------------------------------------------------------------------------
bestEnv_filepath = 'Results/bestEnv_bed_f_door_i_2021-06-19__13-51.pkl'
bestfallRisk_filepath = 'Results/bestFallRisk_bed_f_door_i_2021-06-19__13-51.pkl'

firstEnv_filepath = 'Results/firstEnv_bed_f_door_i_2021-06-19__13-51.pkl'
firstfallRisk_filepath = 'Results/firstFallRisk_bed_f_door_i_2021-06-19__13-51.pkl'


## ---------------------- LOADING THE FILES -------------------------------
## loading the variabe
with open(bestEnv_filepath, 'rb') as f:
   bestEnv = pickle.load(f)
   
with open(bestfallRisk_filepath, 'rb') as f:
   bestFallRisk = pickle.load(f)
      
with open(firstEnv_filepath, 'rb') as f:
   firstEnv = pickle.load(f)
   
with open(firstfallRisk_filepath, 'rb') as f:
   firstFallRisk = pickle.load(f)   
## ---------------------- PLOTTING -------------------------------   
plot_env(firstEnv[0], 'Initial room layout')
firstFallRisk[0].plotDistribution(bestFallRisk[0].scores, firstEnv[0], 'final', 'nearest')
plt.title('Risk of fall for the first layout')
plt.show()
plot_env(bestEnv[0], title = 'Best found room layout')   
bestFallRisk[0].plotDistribution(bestFallRisk[0].scores, bestEnv[0], 'final', 'nearest')
plt.title('Risk of fall for the best layout')



