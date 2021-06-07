import time
import pandas
import pickle
import matplotlib.pyplot as plt
from pandas import DataFrame

from class_DualAnnealing import Dual_Annealing
#from class_FallRiskAssesment import FallRiskAssesment
#from class_EnvironmentGenerated_base import Environment_Generated
#from functions_collision_detection import plot_polygon, plot_lights

start_time = time.time()
''' ______________________ ROOM GENERATOR ___________________________'''

''' WHICH FURNITURE, DOOR AND LIGHTS ARE USED '''
mainFurnitureCodeArray = [8, 14, 16, 19, 30]
#mainFurnitureCodeArray = [23,24, 28, 30, 16]
#mainFurnitureCodeArray = [14]
#mainFurnitureCodeArray = []
mainDoorsCodeArray = [10] #*** MAIN DOORS ONLY TAKES IN THE DOORS THAT ARE NOT THE DOOR BETWEEN MAIN ROOM AND BATHROOM ****
#mainDoorsCodeArray = []
mainLightCodeArray = [2, 30]
#mainLightCodeArray = []

bathFurnitureCodeArray = [5,9]
#bathFurnitureCodeArray = []
bathDoorsCodeArray = [11] # *** BATHROOMDOORS ARE ONLY THE DOOR THAT IS BETWEEN THE MAIN ROOM AND THE BATHROOM
#bathDoorsCodeArray = []
bathLightCodeArray = [2]
#bathLightCodeArray = []

mainRoom = [mainFurnitureCodeArray, mainDoorsCodeArray, mainLightCodeArray, 'main_room']
bathRoom = [bathFurnitureCodeArray, bathDoorsCodeArray, bathLightCodeArray, 'bath_room']

''' ______________________ OPTIMIZATION PARAMETER ___________________________'''
for i in range(5): # number of runs
  numCyc = 3; numTrial = 3;# numCyc = 25, numTrial = 30
  pInit = 1; pEnd = 0;    # probabilities of accepting the solution at the begining and end
  tInit = 10; tEnd = 0.05;
  
  maxNumTraj = 10 # maximum number of trajectories between two objects
  # FALL MODEL
  # intention_set = {'start': ['Bed', 'Main Door', 'Bed', 'Toilet', 'Sink-Bath', 'Chair-Patient', 'Toilet', 'Bed', 'Chair-Patient', 'Bed', 'Chair-Visitor'], 'end': ['Main Door', 'Bed', 'Toilet', 'Sink-Bath', 'Bed', 'Toilet', 'Chair-Patient', 'Chair-Patient', 'Bed', 'Chair-Visitor', 'Bed'], 'frequency': [3, 3, 6, 6, 6, 3, 3, 2, 2, 1, 1]} # for P22 & Room-4 & Room-2 designs
  #    intention_set = {'start': ['Bed', 'Main Door', 'Bed', 'Toilet', 'Sink-Bath', 'Chair-Patient', 'Toilet', 'Bed', 'Chair-Patient', 'Bed', 'Sofa'], 'end': ['Main Door', 'Bed', 'Toilet', 'Sink-Bath', 'Bed', 'Toilet', 'Chair-Patient', 'Chair-Patient', 'Bed', 'Sofa', 'Bed'], 'frequency': [3, 3, 6, 6, 6, 3, 3, 2, 2, 1, 1]} # for A-K & S-B & J-M & J-C & J-G & B-L & B-JH & Room-1 & Room-3 designs
  #intention_set = {'start': ['Bed', 'Bed'], 'end': ['Sofa', 'Chair-Patient'], 'frequency': [20, 20, 1, 1, 1, 1, 1, 1, 1, 1, 1]} # for test
  #intention_set = {'start': ['Bed', 'Sofa'], 'end': ['Sofa', 'Bed'], 'frequency': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]} # for test
  intention_set = {'start': ['Bed', 'Bed', 'Bed'], 'end': ['Toilet', 'Chair-Patient', 'Main Door'], 'frequency': [5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1]} # FOR ICORES
  #intention_set = {'start': ['Bed'], 'end': ['Main Door'], 'frequency': [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]} 
#  intention_set = {'start': ['Sofa', 'Sofa'], 'end': ['Cabinet', 'Chair-Patient'], 'frequency': [2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]} # for test
  
  
  annealingOptimization = Dual_Annealing(numCyc, numTrial, pInit, pEnd, tInit, tEnd, mainRoom, bathRoom, intention_set, maxNumTraj)
  
  #-----------------------------------------------------------------------------
  #                                 PLOTS
  #-----------------------------------------------------------------------------
  
  plt.show()
  #print('annealingOptimization.furnMu: ',annealingOptimization.furnMu)
  plt.plot(annealingOptimization.chosenFitness[1:])
  plt.ylabel('Accepted fitness value'); plt.xlabel('# of iterations'); plt.show()
            
  plt.plot(annealingOptimization.pBoltztemp)
  plt.ylabel('Boltzman values'); plt.xlabel('# of iterations'); plt.show()
  plt.plot(annealingOptimization.t)
  #plt.ylabel('Temperature'); plt.xlabel('# of iterations'); plt.show()    
            
  elapsedTime = time.time() - start_time # Total elapsed time for the program
  
  #-----------------------------------------------------------------------------
  #                             SAVING TO FILE
  #-----------------------------------------------------------------------------
  timestr = time.strftime("%Y-%m-%d__%H-%M") # for adding to the excel file name
  #---------------------------- Saving in pickle file ---------------------------
  ''' dumping the variable'''
  # CHOSEN BY OPTIMIZATION 
  
  with open('Results/newInboard/chosenEnv_'+timestr+'.pkl', 'wb') as f:
    pickle.dump([annealingOptimization.chosenEnv], f)
  with open('Results/newInboard/chosenFallRisk_'+timestr+'.pkl', 'wb') as f:
    pickle.dump([annealingOptimization.chosenFallRisk], f)
  # INITIAL SOLUTION
  with open('Results/newInboard/firstEnv_'+timestr+'.pkl', 'wb') as f:
    pickle.dump([annealingOptimization.env[0]], f)
  with open('Results/newInboard/firstFallRisk_'+timestr+'.pkl', 'wb') as f:
    pickle.dump([annealingOptimization.firstFallRisk], f)
  # BEST FOUND BY THE OPTIMIZATION
  with open('Results/newInboard/bestEnv_'+timestr+'.pkl', 'wb') as f:
    pickle.dump([annealingOptimization.bestEnv], f)
  with open('Results/newInboard/bestFallRisk_'+timestr+'.pkl', 'wb') as f:
    pickle.dump([annealingOptimization.bestFallRisk], f)
  #
  ##loading the variabe
  ##with open('chosenEnv_'+timestr+'.pkl', 'rb') as f:
  ##  newEnv = pickle.load(f)
  #
  #
  ##---------------------------- Saving in an excel file -------------------------
  
  dfCycle = DataFrame({'Cycle Time':annealingOptimization.cycleTime})
  #dfElapsed = DataFrame({'Overall Elapsed Time':elapsedTime})
  dfBestValue = DataFrame({'Best Found value':annealingOptimization.bestFitness})
  dfChosenValue = DataFrame({'Chosen Fitness value':annealingOptimization.chosenFitness})
  dfTemperature = DataFrame({'Temperature':annealingOptimization.t})
  dfRun = DataFrame({'# of cycles':numCyc, 'numTrial':numTrial,'Overall Elapsed Time':elapsedTime }, index=[0])
  dfAcceptance = DataFrame({'Acceptance Rate':annealingOptimization.acceptanceRate})
  
  writer = pandas.ExcelWriter('Results/newInboard/Result_'+timestr+'.xlsx', engine = 'xlsxwriter')
  
  dfRun.to_excel(writer, sheet_name='RUN', index = False, startcol=0)
  dfCycle.to_excel(writer, sheet_name='Cycle time', index=False, startcol=0)
  dfBestValue.to_excel(writer, sheet_name='BestValue', index=False, startcol=0)
  dfChosenValue.to_excel(writer, sheet_name='ChosenFitness', index=False, startcol=0)
  dfTemperature.to_excel(writer, sheet_name='Temperature', index=False, startcol=0)
  dfAcceptance.to_excel(writer, sheet_name='Acceptance Rate', index=False, startcol=0)
  
  writer.save()
  writer.close()