# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 17:05:35 2020
http://apmonitor.com/me575/index.php/Main/SimulatedAnnealing
@author: local_ergo
"""
import math
import statistics as stats
import numpy as np
import os
import random
import time
import matplotlib.pyplot as plt
from class_EnvironmentGenerated_annealing import Environment_Generated
from class_FallRiskAssesment import FallRiskAssesment
from Trajectory_generation import generate_trajectory, define_obstacles
from functions_collision_detection import plot_polygon, plot_lights
from functions_temperture_sceduling import*
from functions_fitness import fitness_distance_between_furn

#------------------------------------------------------------------------------                
#                           CLASSES
#------------------------------------------------------------------------------    

class Dual_Annealing():
    '''
    numCyc: number of cycles
    numTrial: number of trials at each cycle
    nSol: number of accepted solutions
    pInit: probability of accepting the worse solution at the begining
    pEnd: probability of accepting the worse solution at the end
    tInit: initial temperture
    tEnd: final temperture
    '''
    def __init__(self, numCyc, numTrial, pInit, pEnd, tInit, tEnd, mainRoom, bathRoom, intention_set, maxNumTraj, bedPlacement = 0):
      
        self.cycleTime = [] # keeps track of the time of each cycle
        
        # -------------------------- ROOM GENERATION PARAMETERS -----------------------------
        furnMainStat = []; furnBathStat= []
        lightMainStat = []; lightBathStat = []
        doorMainStat = []; doorBathStat = []

        self.std = np.identity(3)        
        self.numOfRows = 22 # Number of grids in the room in Y direction.
        self.numOfCols = 29 # Number of grids in the room in X direction.
        self.env = [] # Initializing the environment
        self.env.append(Environment_Generated(mainRoom, bathRoom, furnMainStat, furnBathStat, lightMainStat, lightBathStat, doorMainStat, doorBathStat, self.numOfRows, self.numOfCols, bedPlacement))
        self.firstEnv = self.env[-1]
        
        '''PLOTTING THE ROOM'''
        for room in self.env[-1].roomList:
            plot_polygon(room.polygon, fignum = 0, title = 'Initial Placement of the Room')
            
        for door in self.env[-1].doorList:
                plot_polygon(door.polygon, fignum = 0, title = 'Initial Placement of the Room')
        
        for furniture in self.env[-1].furnitureList:
            plot_polygon(furniture.polygon, fignum = 0, title = 'Initial Placement of the Room')
            
        for light in self.env[-1].lightList:
            plot_lights(light.point, fignum = 0, title = 'Initial Placement of the Room')
        plt.show()
        
        
        self.chosenEnv = self.env[0]  # initializng the solution


        # -------------------------- FALL MODEL PARAMETERS -----------------------------
        pdf_filenames = []
        png_filenames = []
        traj_png_filenames = []
        traj_pdf_filenames = []
        path = os.path.join(os.getcwd()) # The object library file address.
        design_name = "Room-3-Inboard-Headwall"
        day_night = "day"
        plots = True

        
        '''Setup parameters used for motion prediction and evaluation'''
    #    v = [1.2, 0.3] # maximum linear velocity = [mu, sigma]
        v = [0.5, 0.3] # maximum linear velocity = [mu, sigma]
#        v = [0.3, 0.2] # maximum linear velocity = [mu, sigma]
        w = [1, 0.3] # maximum angular velocity = [mu, sigma]
#        w = [0.5, 0.3] # maximum angular velocity = [mu, sigma]
        num_points = 500
    
        # Setup scenarios within the room
        num_trials = 36
        
        library_file = "{0}/Object_Library.csv".format(path) # Put the object library file address here.
        background_filename = "{0}/Room_Designs/{1}_objects_rotated.png".format(path, design_name)
        
        for counter in range(num_trials):
            traj_pdf_filenames.append("{0}/results/{1}/{2}/Trajectories/{1}_{2}_traj_{3}.pdf".format(path, design_name, day_night, counter+1))
            traj_png_filenames.append("{0}/results/{1}/{2}/Trajectories/{1}_{2}_traj_{3}.png".format(path, design_name, day_night, counter+1))
        for factor in ["light", "floor", "door", "support", "baseline"]:
            pdf_filenames.append("{0}/results/{1}/{2}/{1}_{2}_{3}.pdf".format(path, design_name, day_night, factor))
            png_filenames.append("{0}/results/{1}/{2}/{1}_{2}_{3}.png".format(path, design_name, day_night, factor))
            png_filenames.append("{0}/results/{1}/{2}/{1}_{2}_{3}.png".format(path, design_name, day_night, factor))
            
        # -------------------------- SA OPTIMIZATION PARAMETERS -----------------------------
        self.bestFitness = [] # This variable saves the best fitness value found over time
        self.fitness = [] # fitness is basically the energy function in the concept of annealing
        self.chosenFitness = []
        self.fitness.append(1000) # initializing the current energy to a very big number
        self.chosenFitness.append(1000)
        self.bestFitness.append(1000)
        self.acceptanceRate = []  # The acceptance rate is defined as: (# of accepted solutions)/(total solutions) for each trial 
        self.pBoltz = []; self.pBoltztemp = [] # pBoltztemp is created to check how pBoltz changes with other parameters to tune the temperaure for
        # Initializing the mean value and standard deviation of the solution

        fallRisk = []
        fallRisk.append(FallRiskAssesment(self.env[0]))  # Initializing the fall risk
        self.t = []; self.t.append(tInit) # initializing the temperture
        self.t1 = []; self.t2 = []
        self.dE = []; #self.dE.append(0); # initializng the energy
#        self.dEAve = [];# self.dEAve.append(0)
        
        self.na = 1; # number of accepted answers
        accept = False
#        frac = (tEnd/tInit)**(1.0/(numCyc-1.0)) # Fractional reduction every cycle       
        initFreq = list(intention_set['frequency'])
        alpha = tEnd/tInit; k = 5/numCyc # Temperture scheduling hyper parameter and speeding factor for t = t*alpha**k
        #-------------------------------------------------------------------------------------------------------
        for cycle in range(1,numCyc):
            print('___________________________________________________________________');
            print('                        CYCLE', cycle)
            print('___________________________________________________________________')
            start_time = time.time()
            # ADJUSTING NUMBER OF TRAJECTORIES BASED ON THE CYCLE 
#            tempFreq = []
#            numOfTraj = int(math.ceil((cycle*maxNumTraj)/(numCyc))); #print('- Number of trajectories:', numOfTraj)
#            tempFreq = initFreq
#            for i in range(len(tempFreq)):
#              tempFreq[i] = tempFreq[i]*numOfTraj
#            initFreq = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] # this is so weired that I still have to have this here! For some reason initFreq changes with 
#            intention_set['frequency'] = tempFreq

            ''' choosing temperture scheduling method'''
#            self.t.append(alpha2k_temp_change(self.t[cycle-1], alpha, k)) # new temperture
#            self.t.append(logaritmic_temp_change(self.t[cycle-1], alpha, k))
#            self.t.append(geometric_temp_change(self.t[cycle-1], alpha, k))
#            self.t.append(self.t[-1]*frac)
            self.t.append(standard_T_alpha_k(self.t[cycle-1]))
            
            print('Cycle: ' + str(cycle) + ' with Temperature: ' + str(self.t[cycle]))

#            for trial in range(1,numTrial):
            trial = 1
            nAccepted = 0 # number of accepted solutions
            while trial < numTrial :
              print('------------------------------------------------------')
              #-------------------------------------------------------------------------------
              #                               ROOM GENERATION 
              #-------------------------------------------------------------------------------

              print('Generating room',trial, 'in cycle:', cycle , '...')    
              self.env.append(Environment_Generated(mainRoom, bathRoom, furnMainStat, furnBathStat, lightMainStat, lightBathStat, doorMainStat, doorBathStat, self.numOfRows, self.numOfCols, bedPlacement))
              '''PLOTTING THE ROOM'''
              plt.show()
              for room in self.env[-1].roomList:
                  plot_polygon(room.polygon, fignum = cycle, title = 'Final Placement, room '+str(trial)+' in cycle '+str(cycle))
                  
              for door in self.env[-1].doorList:
                      plot_polygon(door.polygon, fignum = cycle, title = 'Final Placement, room '+str(trial)+' in cycle '+str(cycle))
              
              for furniture in self.env[-1].furnitureList:
                  plot_polygon(furniture.polygon, fignum = cycle, title = 'Final Placement, room '+str(trial)+' in cycle '+str(cycle))
                  
              for light in self.env[-1].lightList:
                  plot_lights(light.point, fignum = cycle, title = 'Final Placement, room '+str(trial)+' in cycle '+str(cycle))
              plt.show()
              #-------------------------------------------------------------------------------
              #                                FALL MODELL 
              #-------------------------------------------------------------------------------
              print('Baseline evaluating room', trial,' with the fall model...')
              fallRisk.append(FallRiskAssesment(self.env[-1])) # Initial FallRiskAssesment class
              fallRisk[-1].update(png_filenames, pdf_filenames, assistive_device = False, plot = plots) # # no assistive devices, Find scores for each baseline factor and baseline evaluation

              print('Motion Evaluation room', trial, ' with the fall model...')
              # Initialization
              TrajectoryPoints = []
              cc = 0
            
              for intention in range(len(intention_set['start'])):
                statCC = 0 # this varibale keeps track of trials for finding trajectories for each intention/scenarios
                for intenTrial in range(intention_set['frequency'][intention]):
                      # Generating a trajectory for each scenario each intenTrial
                      print("Trajectory prediction for scenario {0}, trial {1}: ".format(intention+1, intenTrial+1))
                      obstacles = define_obstacles(self.env[-1]) # Defines obstacles including furniture and walls
                      traj, trajStatus = generate_trajectory(intention_set['start'][intention], intention_set['end'][intention], self.env[-1], obstacles, random.gauss(v[0], v[1]), random.gauss(w[0], w[1]), num_points)
                      print('Trajectory status:', trajStatus)
                      if trajStatus != 2:
                        statCC += 1 
                        print('Trajectory was not found in trial',intenTrial, 'and statCC is:', statCC, 'and this trajectory frequency is:',intention_set['frequency'][intention])
                        if statCC == intention_set['frequency'][intention]:

                          print('No trajectories were found for', intention_set['start'][intention],'to',intention_set['end'][intention]  , 'RESETTING room number ', trial, '...')
                          del self.env[-1]
                          del fallRisk[-1]
                          break
                        
                      if statCC == intention_set['frequency'][intention]:
                        break
                      cc += 1
                      # Evaluating the generated trajectory
                      TrajectoryPoints.append(fallRisk[-1].getDistibutionForTrajectory(traj, cc, background_filename, traj_png_filenames, traj_pdf_filenames, plot=plots, assistive_device = False, baselinefig = fallRisk[-1].baselinefig, baselineAx = fallRisk[-1].baselineAx))

                if statCC == intention_set['frequency'][intention]:
                  break
              if statCC == intention_set['frequency'][intention]:             
                continue
                
              print("Final Scores Calculation of room ",trial,'in cycle',cycle,' ...')
              num = np.ones([self.env[-1].numOfRows,self.env[-1].numOfCols]) # Initializing number of points in each grid cell as one

              for traj in TrajectoryPoints:
                  for point in traj:
                      [m,n] = fallRisk[-1].meter2grid(point[0][0]) # Finding the grid cell for each point in trajectories
#                      print('Before:', fallRisk[-1].scores[m,n])
                      fallRisk[-1].scores[m,n] += point[1] # Add the score of that point to the associated grid cell
#                      print('After:', fallRisk[-1].scores[m,n])
#                      fallRisk[-1].scores[m,n] += (point[1]*(maxNumTraj-numOfTraj)/maxNumTraj) # Add the score of that point to the associated grid cell and normalize it
                      num[m,n] += 1 # Add 1 to number of points inside that grid cell
              for r in range(self.env[-1].numOfRows):
                  for c in range(self.env[-1].numOfCols):
                      fallRisk[-1].scores[r,c] = fallRisk[-1].scores[r,c]/num[r,c] # Take the avarage score for each grid cell
#                      
#              print("Final evaluation plot...")
#              fallRisk[-1].plotDistribution(fallRisk[-1].scores, self.env[-1], 'final', 'hamming')
#              fallRisk[-1].plotDistribution(fallRisk[-1].scores, self.env[-1], 'final', 'nearest')
              ''' Saving the first environment and score for comparison'''
              if cycle == 1 and trial == 1:
                self.firstEnv = self.env[-1]
                self.firstFallRisk = fallRisk[-1]
                
              self.fitness.append(fitness_Distribution(fallRisk[-1])) 
#              self.fitness.append(fitness_distance_between_furn(self.env[-1].furnitureList)) # Test fitness function
#                print(' scores are: \n', fallRisk[i].scores, '\n and the mean value is: ', fallRisk[i].scores.mean())
              print('The score for room  ',trial,' is: ', self.fitness[-1])               
              if self.fitness[-1] < self.bestFitness[-1]:
                self.bestFitness.append(self.fitness[-1])
                self.bestEnv = self.env[-1]
                self.bestFallRisk = fallRisk[-1]
              else:
                self.bestFitness.append(self.bestFitness[-1]) # save the current data
              #-------------------------------------------------------------------------------
              #                                OPTIMIZATOION
              #-------------------------------------------------------------------------------
              print('Optimization...')
#              print('self.fitness[-1] is: ', self.fitness[-1], 'and self.fitness[-2] is:', self.fitness[-2])
              self.dE.append(self.fitness[-1] - self.chosenFitness[-1]) # delta energy
              
              if cycle == 1 and trial == 1: 
                self.dE[-1] = self.fitness[-1]
              
              if self.fitness[-1] < self.chosenFitness[-1]: # if current configuration has lower energy than the previous cycle
                print('New solution is better than the previous one with dE of: ', self.dE[-1],'. Accepting the new one!')
                accept = True
  
              else:
                print('New solution is worse than the previous one, dE is :', self.dE[-1],', checking Boltzman condition ...  ')
                self.pBoltz.append(math.exp(-1*(self.dE[-1]/self.t[cycle])))
#                self.pBoltz.append(math.exp(-1*(self.dE[-1]/(self.dEAve[-1]*self.t[cycle]))))
                ran = random.uniform(0,1); # Generating a random number

                #********************************    FOR TEST   *************************************************
#                if self.pBoltz[-1] > (numCyc-cycle)/numCyc:
#                  self.pBoltz[-1] = (numCyc-cycle)/numCyc
#                  print('numCyc-cycle)/numCyc is:', (numCyc-cycle)/numCyc, 'pBOLTZ CHANGED')
                #**********************************************************************************************
                print('Boltzman probability is: ',self.pBoltz[-1],' and the generated random number is: ', ran)
                if (self.pBoltz[-1] > ran):
                  print('Boltzman condition is satisfied! Worse solution is ACCEPTED.')
                  accept = True
                else:
                  print('Boltzman condition is not satisfied, new solution is DISREGARDED.')
                  accept = False
                  
              if accept == True:
#                print('ACCEPT')
                self.chosenEnv = self.env[-1]
                self.chosenFallRisk = fallRisk[-1]
                self.chosenFitness.append(self.fitness[-1])
                furnMainStat, furnBathStat = furn_mu_and_sigma(self.chosenEnv)
                lightMainStat, lightBathStat = light_mu_and_sigma(self.chosenEnv)
#                doorMainStat, doorbathStat = door_mu_and_sigma(self.chosenEnv)
                self.na +=1
                nAccepted += 1
              else:
                self.chosenFitness.append(self.chosenFitness[-1])
                
              self.pBoltztemp.append(math.exp(-1*(abs(self.dE[-1])/self.t[cycle])))
#                self.dEAve.append((self.dEAve[-1]*(self.na-1)+abs(self.dE[-1]))/self.na) # updating the average delta_E
#                print('dEAve:', self.dEAve[-1], 'na:', self.na, 'dE =', self.dE[-1])           
              self.acceptanceRate.append(nAccepted/trial)
              trial += 1
              
            self.cycleTime.append(time.time() - start_time)
#------------------------------------------------------------------------------                
#                           FUNCTIONS
#------------------------------------------------------------------------------                
                
def furn_mu_and_sigma(env):
  ''' This function saves the characteristics of the lights of the
  chosen environment for the next round of optimization. The size of the 
  mu (mean) and sigma (std) differs if the object is against a wall or not'''
  # The env passed to this function is the acctpted environemt. The statistical parameters for the nxt solution is defined based on this solution
  mainMu = []; mainStd = [] # mean value and standard deviation for sampling the new generation
  bathMu = []; bathStd = [] # mean value and standard deviation for sampling the new generation
  for furn in env.furnitureList:
    if furn.room == 'main_room':
      if furn.wallPoint == []:
        mainMu.append(furn.conf)
        mainStd.append([1, 1, 30]) # standard deviation of orientation is always constant    
      else: # if against a wall
        mainMu.append(furn.wallPoint)
        mainStd.append([5])
    else: # if bathroom furniture
      if furn.wallPoint == []:
        bathMu.append(furn.conf)
        bathStd.append([1, 1, 30]) # standard deviation of orientation is always constant    
      else: # if against a wall
        bathMu.append(furn.wallPoint)
        bathStd.append([1])
        
  return [mainMu, mainStd], [bathMu, bathStd]

def light_mu_and_sigma(env):
  ''' This function saves the characteristics of the lights of the
  chosen environment for the next round of optimization'''
  mainMu = []; mainStd = [] # mean value and standard deviation for sampling the new generation
  bathMu = []; bathStd = [] # mean value and standard deviation for sampling the new generation
  for light in env.lightList:
    if light.room == 'main_room':
      mainMu.append(light.pos)
      mainStd.append([1, 1]) # standard deviation of orientation is always constant    
    else:
      bathMu.append(light.pos)
      bathStd.append([1, 1]) # standard deviation of orientation is always constant    
  return  [mainMu, mainStd], [bathMu, bathStd]

def door_mu_and_sigma(env):
  ''' This function saves the characteristics of the doors of the 
  chosen environment for the next round of optimization'''
  bathMu = []; bathStd = [] # Bathroom variables
  mainMu = []; mainStd = [] # Mainroom variables
  for door in env.doorList:
    if door.room == 'main_room':
      mainMu.append(door.wallPoint)
      mainStd.append(4) # standard deviation of 10 centimeters
    else:
      bathMu.append(door.wallPoint)
      bathStd.append(2) # standard deviation of 10 centimeters
    return [mainMu, mainStd], [bathMu, bathStd]
 
def fitness_Distribution (fallRisk):

     fitnessMean = np.mean(fallRisk.scores)
     fitnessMedian = np.median(fallRisk.scores)
     fitnessStd = np.std(fallRisk.scores)
     fitnessMax = np.amax(fallRisk.scores)
     alpha = 0.95*fitnessMax # the threshold that we define for the area under the curve, under the right tail of the distribution
     
     fitness = fitnessMedian + fitnessMax + ((alpha - fitnessMean)/fitnessStd)
     
     return fitness
    
    
    
                               