# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 16:08:00 2020
This file contains different functions for temperture scheduling of simulated
 annealing optimization function. alpha is a hyper parameter and k is the
 speeding variable
@author: Sarvenaz
"""
import numpy as np

def alpha2k_temp_change(T, alpha, k):
  return T*(alpha**k)

def logaritmic_temp_change(T, alpha, k):
  return (T)/(1+alpha*np.log(1+k))

def geometric_temp_change(T, alpha, k):
  return (T)/(1+alpha*k)

def standard_T_alpha_k(T):
  return (T)*0.7


alpha = 0.8
T = 10
for i in range(25):
  T = standard_T_alpha_k(T)
  print(T)