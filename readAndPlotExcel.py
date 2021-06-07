# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 21:38:27 2020

@author: sarve
"""
import statistics as stat
import numpy as np
import pandas as pd
import scipy as sp
import scipy.interpolate
import matplotlib.pyplot as plt
from scipy import signal

'''------------------------------------------------------------------------------
#                             INBOARD DATA
#------------------------------------------------------------------------------'''

#-----------------------------  CHOSEN FITNESS -------------------------------
'''Chosen Fitness'''
in5Chosen = pd.read_excel(r'Results\Inboard\Result_2020-09-07__04-00.xlsx', sheet_name='ChosenFitness', index = False); in5Chosen = in5Chosen.iloc[1:]
in4Chosen = pd.read_excel(r'Results\Inboard\Result_2020-09-06__20-25.xlsx', sheet_name='ChosenFitness', index = False); in4Chosen = in4Chosen.iloc[1:]
in3Chosen = pd.read_excel(r'Results\Inboard\Result_2020-09-05__20-58.xlsx', sheet_name='ChosenFitness', index = False); in3Chosen = in3Chosen.iloc[1:]
in2Chosen = pd.read_excel(r'Results\Inboard\Result_2020-09-06__04-32.xlsx', sheet_name='ChosenFitness', index = False); in2Chosen = in2Chosen.iloc[1:]
in1Chosen = pd.read_excel(r'Results\Inboard\Result_2020-09-06__12-09.xlsx', sheet_name='ChosenFitness', index = False); in1Chosen = in1Chosen.iloc[1:]
#print('len(in1):',len(in1Chosen), 'len(in2):',len(in2Chosen),'len(in3):',len(in3Chosen),'len(in4):',len(in4Chosen),'len(in5):',len(in5Chosen))

nSample = max(len(in1Chosen), len(in2Chosen),len(in3Chosen),len(in4Chosen),len(in5Chosen))

newAxis = np.linspace(1, nSample, nSample)
in1Chosen = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(in1Chosen)), in1Chosen.squeeze(), kind='linear')(newAxis)
in2Chosen = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(in2Chosen)), in2Chosen.squeeze(), kind='linear')(newAxis)
in3Chosen = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(in3Chosen)), in3Chosen.squeeze(), kind='linear')(newAxis)
in4Chosen = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(in4Chosen)), in4Chosen.squeeze(), kind='linear')(newAxis)
in5Chosen = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(in5Chosen)), in5Chosen.squeeze(), kind='linear')(newAxis)

plt.plot(in1Chosen)
plt.plot(in2Chosen);
plt.plot(in3Chosen);
plt.plot(in4Chosen);
plt.plot(in5Chosen);
plt.title(' The Accepted Fitness Value for Inboard Room');plt.ylabel('Accepted Fitness Value'); plt.xlabel('Resampled Data Point');
plt.show()

# Calculating the mean value
multipleList = [in1Chosen, in2Chosen, in3Chosen, in4Chosen, in5Chosen]
arrays = [np.array(x) for x in multipleList]
meanResult = np.array([np.mean(k) for k in zip(*arrays)])
stdevResult = np.array([np.std(k) for k in zip(*arrays)])

# Plot

plt.fill_between(range(len(meanResult)), meanResult-stdevResult, meanResult+stdevResult, alpha =0.3, facecolor='blue' )
plt.plot(meanResult, color = 'blue')
plt.title(' The Accepted Fitness Value for Inboard Room'); plt.ylabel('Accepted Fitness Value'); plt.xlabel('Resampled Data Point');
plt.show()


#-----------------------------  BEST FITNESS -------------------------------
'''Best Fitness'''
in5Best = pd.read_excel(r'Results\Inboard\Result_2020-09-07__04-00.xlsx', sheet_name='BestValue', index = False); in5Best = in5Best.iloc[1:]
in4Best = pd.read_excel(r'Results\Inboard\Result_2020-09-06__20-25.xlsx', sheet_name='BestValue', index = False); in4Best = in4Best.iloc[1:]
in3Best = pd.read_excel(r'Results\Inboard\Result_2020-09-05__20-58.xlsx', sheet_name='BestValue', index = False); in3Best = in3Best.iloc[1:]
in2Best = pd.read_excel(r'Results\Inboard\Result_2020-09-06__04-32.xlsx', sheet_name='BestValue', index = False); in2Best = in2Best.iloc[1:]
in1Best = pd.read_excel(r'Results\Inboard\Result_2020-09-06__12-09.xlsx', sheet_name='BestValue', index = False); in1Best = in1Best.iloc[1:]
#print('len(in1):',len(in1Best), 'len(in2):',len(in2Best),'len(in3):',len(in3Best),'len(in4):',len(in4Best),'len(in5):',len(in5Best))

nSample = min(len(in1Best), len(in2Best),len(in3Best),len(in4Best),len(in5Best))
newAxis = np.linspace(1, nSample, nSample)
in1Best = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(in1Best)), in1Best.squeeze(), kind='linear')(newAxis)
in2Best = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(in2Best)), in2Best.squeeze(), kind='linear')(newAxis)
in3Best = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(in3Best)), in3Best.squeeze(), kind='linear')(newAxis)
in4Best = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(in4Best)), in4Best.squeeze(), kind='linear')(newAxis)
in5Best = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(in5Best)), in5Best.squeeze(), kind='linear')(newAxis)

plt.plot(in1Best)
plt.plot(in2Best);
plt.plot(in3Best);
plt.plot(in4Best);
plt.plot(in5Best);
plt.title(' The Best Found Fitness Value for Inboard Room'); plt.ylabel('Accepted Fitness Value'); plt.xlabel('Resampled Data Point');
plt.show()

# Calculating the mean value
multipleList = [in1Best, in2Best, in3Best, in4Best, in5Best]
arrays = [np.array(x) for x in multipleList]
meanResult = np.array([np.mean(k) for k in zip(*arrays)])
stdevResult = np.array([np.std(k) for k in zip(*arrays)])

# Plot
plt.fill_between(range(len(meanResult)), meanResult-stdevResult, meanResult+stdevResult, alpha =0.3, facecolor='blue' )
plt.plot(meanResult, color = 'blue')
plt.title(' The Best Found Fitness Value for Inboard Room'); plt.ylabel('Accepted Fitness Value'); plt.xlabel('Resampled Data Point');
plt.show()


'''------------------------------------------------------------------------------
#                             OUTBOARD DATA
#------------------------------------------------------------------------------'''

#-----------------------------  CHOSEN FITNESS -------------------------------
'''Chosen Fitness'''
out5Chosen = pd.read_excel(r'Results\Outboard\Result_2020-09-02__07-09.xlsx', sheet_name='ChosenFitness', index = False); out5Chosen = out5Chosen.iloc[1:]
out4Chosen = pd.read_excel(r'Results\Outboard\Result_2020-09-02__16-26.xlsx', sheet_name='ChosenFitness', index = False); out4Chosen = out4Chosen.iloc[1:]
out3Chosen = pd.read_excel(r'Results\Outboard\Result_2020-09-03__00-55.xlsx', sheet_name='ChosenFitness', index = False); out3Chosen = out3Chosen.iloc[1:]
out2Chosen = pd.read_excel(r'Results\Outboard\Result_2020-09-03__08-27.xlsx', sheet_name='ChosenFitness', index = False); out2Chosen = out2Chosen.iloc[1:]
out1Chosen = pd.read_excel(r'Results\Outboard\Result_2020-09-03__15-21.xlsx', sheet_name='ChosenFitness', index = False); out1Chosen = out1Chosen.iloc[1:]
#print('len(out1):',len(out1Chosen), 'len(out2):',len(out2Chosen),'len(out3):',len(out3Chosen),'len(out4):',len(out4Chosen),'len(out5):',len(out5Chosen))

nSample = max(len(out1Chosen), len(out2Chosen),len(out3Chosen),len(out4Chosen),len(out5Chosen))

newAxis = np.linspace(1, nSample, nSample)
out1Chosen = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(out1Chosen)), out1Chosen.squeeze(), kind='linear')(newAxis)
out2Chosen = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(out2Chosen)), out2Chosen.squeeze(), kind='linear')(newAxis)
out3Chosen = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(out3Chosen)), out3Chosen.squeeze(), kind='linear')(newAxis)
out4Chosen = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(out4Chosen)), out4Chosen.squeeze(), kind='linear')(newAxis)
out5Chosen = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(out5Chosen)), out5Chosen.squeeze(), kind='linear')(newAxis)

plt.plot(out1Chosen)
plt.plot(out2Chosen);
plt.plot(out3Chosen);
plt.plot(out4Chosen);
plt.plot(out5Chosen);
plt.title(' The Accepted Fitness Value for outboard Room');plt.ylabel('Accepted Fitness Value'); plt.xlabel('Resampled Data Point');
plt.show()

# Calculating the mean value
multipleList = [out1Chosen, out2Chosen, out3Chosen, out4Chosen, out5Chosen]
arrays = [np.array(x) for x in multipleList]
meanResult = np.array([np.mean(k) for k in zip(*arrays)])
stdevResult = np.array([np.std(k) for k in zip(*arrays)])

# Plot

plt.fill_between(range(len(meanResult)), meanResult-stdevResult, meanResult+stdevResult, alpha =0.3, facecolor='blue' )
plt.plot(meanResult, color = 'blue')
plt.title(' The Accepted Fitness Value for outboard Room'); plt.ylabel('Accepted Fitness Value'); plt.xlabel('Resampled Data Point');
plt.show()


#-----------------------------  BEST FITNESS -------------------------------
'''Best Fitness'''
out5Best = pd.read_excel(r'Results\Outboard\Result_2020-09-02__07-09.xlsx', sheet_name='BestValue', index = False); out5Best = out5Best.iloc[1:]
out4Best = pd.read_excel(r'Results\Outboard\Result_2020-09-02__16-26.xlsx', sheet_name='BestValue', index = False); out4Best = out4Best.iloc[1:]
out3Best = pd.read_excel(r'Results\Outboard\Result_2020-09-03__00-55.xlsx', sheet_name='BestValue', index = False); out3Best = out3Best.iloc[1:]
out2Best = pd.read_excel(r'Results\Outboard\Result_2020-09-03__08-27.xlsx', sheet_name='BestValue', index = False); out2Best = out2Best.iloc[1:]
out1Best = pd.read_excel(r'Results\Outboard\Result_2020-09-03__15-21.xlsx', sheet_name='BestValue', index = False); out1Best = out1Best.iloc[1:]
#print('len(out1):',len(out1Best), 'len(out2):',len(out2Best),'len(out3):',len(out3Best),'len(out4):',len(out4Best),'len(out5):',len(out5Best))

nSample = max(len(out1Best), len(out2Best),len(out3Best),len(out4Best),len(out5Best))

newAxis = np.linspace(1, nSample, nSample)
out1Best = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(out1Best)), out1Best.squeeze(), kind='linear')(newAxis)
out2Best = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(out2Best)), out2Best.squeeze(), kind='linear')(newAxis)
out3Best = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(out3Best)), out3Best.squeeze(), kind='linear')(newAxis)
out4Best = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(out4Best)), out4Best.squeeze(), kind='linear')(newAxis)
out5Best = sp.interpolate.interp1d(np.linspace(1, max(newAxis), len(out5Best)), out5Best.squeeze(), kind='linear')(newAxis)


#
plt.plot(out1Best)
plt.plot(out2Best);
plt.plot(out3Best);
plt.plot(out4Best);
plt.plot(out5Best);
plt.title(' The Best Found Fitness Value for outboard Room'); plt.ylabel('Accepted Fitness Value'); plt.xlabel('Resampled Data Point');
plt.show()

# Calculating the mean value
multipleList = [out1Best, out2Best, out3Best, out4Best, out5Best]
arrays = [np.array(x) for x in multipleList]
meanResult = np.array([np.mean(k) for k in zip(*arrays)])
stdevResult = np.array([np.std(k) for k in zip(*arrays)])

# Plot
plt.fill_between(range(len(meanResult)), meanResult-stdevResult, meanResult+stdevResult, alpha =0.3, facecolor='blue' )
plt.plot(meanResult, color = 'blue')
plt.title(' The Best Found Fitness Value for outboard Room'); plt.ylabel('Accepted Fitness Value'); plt.xlabel('Resampled Data Point');
plt.show()


