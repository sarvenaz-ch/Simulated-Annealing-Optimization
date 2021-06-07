# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 11:26:40 2020

@author: sarve
"""
import math
import numpy as np
import statistics as stats

#def environment_mean()


def fitness_Distribution (fallRisk):

     fitnessMean = np.mean(fallRisk.scores)
     fitnessMedian = np.median(fallRisk.scores)
     fitnessStd = np.std(fallRisk.scores)
     fitnessMax = np.amax(fallRisk.scores)
     alpha = 0.95*fitnessMax # the threshold that we define for the area under the curve, under the right tail of the distribution
     
     fitness = fitnessMedian + fitnessMax + ((alpha - fitnessMean)/fitnessStd)
     
     return fitness
   
def fitness_distance_between_furn(furnitureList):
  posX = []
  posY = []
  dist = 0
  for furn in furnitureList:
    posX.append(furn.conf[0])
    posY.append(furn.conf[1])
    
  for i in range(len(posX)-1):
    print('distance between', furnitureList[i].name, 'and', furnitureList[i+1].name, '...')
    dist = dist + math.sqrt((posX[i]-posX[i+1])**2 + (posY[i]-posY[i+1])**2)
    
  return dist
    