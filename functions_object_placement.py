# -*- coding: utf-8 -*-
"""
This code contains functions for randomly placing objects in a room
*************************
This one does not care about the room walls, although it is being checked!
*************************
"""
import numpy as np
import math
import random
from random import sample
from scipy.stats import truncnorm
from math import cos, sin, radians, atan2, degrees

from functions_collision_detection import collision_detection, rectangle_vertices
from shapely.geometry import Polygon, LineString, MultiLineString

def object_configuration(object_code, room_x, room_y, orientation, mu, sigma):
    """ 
    
    This function randomly assigns position [x,y] and orientation [theta[degree]] 
    to the object that is passed to it as an object_code. It finds the object 
    specification from the object_library and uses the assigned length and width
    to place the object in the room. When theta = 0, length is along x-axis and 
    width is along y-axis. Theta is in [0, 360]
    :param object_code: The object code as specified in the object_library.csv
    :param object_library: the object_library.csv (data frame)
    :param room_x: length of the room along x direction (array)
    :param room_y: length of the room along y direction (array)
    : param orientation: array of the allowed orientation angles, in degrees (array)
    """
    if np.all(mu == []):
#        print(' First round')
        obj_x = np.random.normal(loc = room_x.mean(), scale = abs(room_x.max()-room_x.min())/4)# sample an x for the center of the object in the room
        obj_y = np.random.normal(loc =room_y.mean(), scale = abs(room_y.max()-room_y.min())/4)# sample an y for the center of the object in the room
        obj_theta = np.random.normal(loc =orientation.mean(), scale = abs(orientation.max()-orientation.min())/4)# sample an angle for the orientation of the object in the room
        obj_conf = [obj_x, obj_y, obj_theta] # Object configuration
    else:
        obj_conf = np.random.normal(loc = mu, scale = sigma)# sample an y for the center of the object in the room
    '''Keeping the angle [0,360]'''
    if obj_conf[2]>360 :
      obj_conf[2] = obj_conf[2]%360
    elif obj_conf[2] < 0:
      obj_conf[2] = (obj_conf[2]%(-360))+360
#        print('With new mu and sigma, mu is \n', mu)
#        print('obj conf from fucntions_obj_placement: ', obj_conf)
    return(obj_conf)

def door_configuration(room, otherRoom, muDoor, sigmaDoor):
    '''
    THIS FUNCTION FINDS THE WALLS THAT THE DOOR GOES ON (BATHROOM WALLS FOR THE
    BATHROOM DOOR AND THE REST OF THE MAIN ROOM WALLS FOR THE MAIN WALL), UNWRAP
    THE WALLS, SAMPLE A POINT ON THEM, WRAP THEM BACK AND SPITS OUT THE CONFIGURATION
    IN THE ROOM SPACE AS WELL AS THE CHOSEN POINT ON THE WALL
    '''
    l1 = room.polygon.boundary # lineString of the polygon of the room that the door belongs to
    l2 = otherRoom.polygon.boundary # lineString of the polygon of the room that the door does not belong to
    
    # finding the string of walls the door goes on
    if room.name == 'main_room':
#      print('It is the main door')
      wallString = l1.difference(l2)
    else:
#      print('It is the bathroom door')
      wallString = l1.intersection(l2)
      
    unwrapLen = wallString.length # total length of the walls suitable for sampling
#    print('unwrapLen:', unwrapLen,'Mu door:', muDoor)
    
    #------------------------- FOR GENERAL PURPOSES---------------
    general = True
    sampledPoint = unwrap_sampling(unwrapLen, muDoor, sigmaDoor) # sample a point on the wall
    if muDoor != []:
      sampledPoint = sampledPoint[0]
#    print('GENERAL sampled point:', sampledPoint)
    wallSum = []
#      print('lenwallString.geoms:', len(wallString.geoms))
    for i in range(len(wallString.geoms)):
      if i == 0:
        wallSum.append(wallString.geoms[0].length) # the first wall
      else:
        wallSum.append(wallString.geoms[i].length+wallSum[i-1])
    
    #------------------------- FOR OUTBOARD ROOM ---------------
#    outboard = False
#    if room.name == 'main_room': 
#      outboard = True # if you dont want to have an inboard room, change this to false
#    if outboard == True: 
#      samplingRange = np.linspace(0.5, 10, 20) # possible sampling numbers for placing an object
#      wallString = MultiLineString([((0, 0), (4.27,0)), ((4.27,0), (4.27, 5.79))])
#      if muDoor ==[]:
#        sampledPoint = random.choice(samplingRange)
#      else:
#  #      print('mu:',muDoor, 'sigma:', sigmaDoor)
#        sampledPoint = truncnorm((0.5 - muDoor[0]) / sigmaDoor[0], (10 - muDoor[0]) / sigmaDoor[0], loc=muDoor[0], scale=sigmaDoor[0])
#        sampledPoint = sampledPoint.rvs()
#  #      sampledPoint = sampledPoint[0]      
#  #    sampledPoint = 2
#      
#      wallSum = []
#      lineSum = 0
#      for line in wallString:
#        lineSum = lineSum+line.length
#        wallSum.append(lineSum) # the first wall
  #    print('INBOARD sampled point:', sampledPoint)
    #------------------------- FOR INBOARD ROOM ---------------
    inboard = False
    if room.name == 'main_room':
      inboard = True
    if inboard == True:
      samplingRange = np.linspace(0.5, 6, 15) # possible sampling numbers for placing an object
      wallString = MultiLineString([((4.27, 5.79), (1.93, 5.79)), ((0,3.7), (0,0))])
      if muDoor ==[]:
        sampledPoint = random.choice(samplingRange)
      else:
        sampledPoint = truncnorm((0.5 - muDoor[0]) / sigmaDoor[0], (6 - muDoor[0]) / sigmaDoor[0], loc=muDoor[0], scale=sigmaDoor[0])
        sampledPoint = sampledPoint.rvs()
        
      wallSum = []
      lineSum = 0
      for line in wallString:
        lineSum = lineSum+line.length
        wallSum.append(lineSum) # the first wall
      
#    
    #----------------------------------------
    ''' Find on which wall the point goes on'''
    for i in range(len(wallSum)):
#      print('i:', i, 'wallSum[i]', wallSum[i])
      if sampledPoint < wallSum[i] and i == 0:
        wallIndex = 0
        break
      elif sampledPoint < wallSum[i] and sampledPoint > wallSum[i-1]:
       wallIndex = i
       break
      else:
       wallIndex = len(wallSum)-1
#    print('wallIndex:', wallIndex)
    ''' Find the configuration of the door in the room coordinate'''
    chosenWall = wallString.geoms[wallIndex].coords
#    print('chosenWall:', chosenWall[0], chosenWall[1])
    wall_x1 = chosenWall[0][0]; wall_y1 = chosenWall[0][1];
    wall_x2 = chosenWall[1][0]; wall_y2 = chosenWall[1][1];
    chosenWallLen = wallString.geoms[wallIndex].length;# print('Length of the chosen wall:', chosenWallLen)
    
    if wallIndex == 0:
      pointLen = sampledPoint
    else:
      pointLen = sampledPoint- wallSum[wallIndex-1]
    
    conf_x = (pointLen*wall_x2+(chosenWallLen-pointLen)*wall_x1)/(chosenWallLen)
    conf_y = (pointLen*wall_y2+(chosenWallLen-pointLen)*wall_y1)/(chosenWallLen)
    
    Y = wall_y2 - wall_y1
    X = wall_x2 - wall_x1
    theta = round(degrees(atan2(Y, X)))
    
    return sampledPoint, [conf_x, conf_y, theta]

def light_position(room, lightMu, lightSigma):

    if np.all(lightMu == []):
#        print('first round...')
        lightX = np.random.normal(loc = room.x.mean(), scale = abs(room.x.max()-room.x.min())/4)# sample an x for the center of the object in the room
        lightY = np.random.normal(loc =room.y.mean(), scale = abs(room.y.max()-room.y.min())/4)# sample an y for the center of the object in the room
        lightPos = [lightX, lightY]
    else:
#        print('Second round with mu:', lightMu, 'and sigma:', lightSigma)
        lightPos = np.random.normal(loc = lightMu, scale = lightSigma)      
#        lightX = np.random.normal(loc = 0.0, scale = 0.5)# sample an x for the center of the object in the room
#        lightY = np.random.normal(loc = 0.0, scale = 0.5)# sample an y for the center of the object in the room
#        lightPos = lightMu+[lightX, lightY] #lightSigma@np.transpose([lightX, lightY]) # Object configuration
#        lightPos = lightPos.tolist()
#        lightPos = lightPos.tolist()
#    print('light pos from functions_obj_placement: ', lightPos)
    return lightPos  # Light Source Position
  
  
# --------------------  FUNCTIONS SPECIFIC TO AGAINST THE WALL ----------------------------------------

def headWall_footWall_configuration(room, wallIndex, wallLenSum, sampledPoint):
  ''' This function finds the configuration (x,y and theta) of the objects that is going to be placed against a wall
  :room: The room that the object is going to be placed in
  :sampledPoint: the point that is sampled on the unwrapped wall in function unwrapp_sampling()
  : wallIndex: the index of the wall that the sampledPoint corresponds to
  :wallLenSum: fibunacci style sum of the length of the wall in order of their indecis
  '''
  chosenWall = room.walls[wallIndex]  # Find the coordinate of the wall the point is chosen on
  # the start and end cooridnates of the chosen wall
  wall_x1 = chosenWall[0][0]; wall_y1 = chosenWall[0][1];
  wall_x2 = chosenWall[1][0]; wall_y2 = chosenWall[1][1];
  chosenWallLen = math.sqrt((wall_x2-wall_x1)**2+(wall_y1-wall_y2)**2) # length of the chosen wall
  '''Finding the length of the sampled point on the corresponding wall'''
  if wallIndex == 0:  # if the point is sampled on the first wall
    pointLen = sampledPoint # the distance of the sampled point from the begining point of the wall
  else: 
    pointLen = sampledPoint - wallLenSum[wallIndex-1]
#  print('sample point is :', sampledPoint, 'and the length on the corresponding wall is:',pointLen)
  ''' Configuration of the chosen point in the room space (unwrapped wall)'''
  # Position
  conf_x = (pointLen*wall_x2+(chosenWallLen-pointLen)*wall_x1)/(chosenWallLen)
  conf_y = (pointLen*wall_y2+(chosenWallLen-pointLen)*wall_y1)/(chosenWallLen)
  
#  # orientation
#  Y = wall_y1 - wall_y2
#  X = wall_x1 - wall_x2
  Y = wall_y2 - wall_y1
  X = wall_x2 - wall_x1
  theta = round(degrees(atan2(Y, X)))
#  print('x is', conf_x, 'and y is:', conf_y, 'and theta is:', theta)
  return([conf_x, conf_y, theta])


def against_wall_configuration(room, wallIndex, wallLenSum, sampledPoint):
  ''' This function finds the configuration (x,y and theta) of the objects that is going to be placed against a wall
  :room: The room that the object is going to be placed in
  :sampledPoint: the point that is sampled on the unwrapped wall in function unwrapp_sampling()
  : wallIndex: the index of the wall that the sampledPoint corresponds to
  :wallLenSum: fibunacci style sum of the length of the wall in order of their indecis
  '''
  chosenWall = room.walls[wallIndex]  # Find the coordinate of the wall the point is chosen on
  # the start and end cooridnates of the chosen wall
  wall_x1 = chosenWall[0][0]; wall_y1 = chosenWall[0][1];
  wall_x2 = chosenWall[1][0]; wall_y2 = chosenWall[1][1];
  chosenWallLen = math.sqrt((wall_x2-wall_x1)**2+(wall_y1-wall_y2)**2) # length of the chosen wall
  '''Finding the length of the sampled point on the corresponding wall'''
  if wallIndex == 0:  # if the point is sampled on the first wall
    pointLen = sampledPoint # the distance of the sampled point from the begining point of the wall
  else: 
    pointLen = sampledPoint - wallLenSum[wallIndex-1]
#  print('sample point is :', sampledPoint, 'and the length on the corresponding wall is:',pointLen)
  ''' Configuration of the chosen point in the room space (unwrapped wall)'''
  # Position
  conf_x = (pointLen*wall_x2+(chosenWallLen-pointLen)*wall_x1)/(chosenWallLen)
  conf_y = (pointLen*wall_y2+(chosenWallLen-pointLen)*wall_y1)/(chosenWallLen)
  
#  # orientation
#  Y = wall_y1 - wall_y2
#  X = wall_x1 - wall_x2
  Y = wall_y2 - wall_y1
  X = wall_x2 - wall_x1
  theta = round(degrees(atan2(Y, X)))
#  print('x is', conf_x, 'and y is:', conf_y, 'and theta is:', theta)
  return([conf_x, conf_y, theta])
  
def against_wall_room_conf(wall_conf, length):
  ''' This function finds the center of the object based on its length and the 
  point that is find on the wall'''
  length = length + 0.01
#  print('Wall conf is:', wall_conf)
  x_wall = wall_conf[0]; y_wall = wall_conf[1]; theta = wall_conf[2]
#  theta = 224 
#  x = x_wall-(length/2)*round(sin(radians(theta)))
  x = x_wall-(length/2)*(sin(radians(theta)))
#  y = y_wall+(length/2)*round(cos(radians(theta)))
  y = y_wall+(length/2)*(cos(radians(theta)))
  theta = theta + 90
  '''Keeping the angle [0,360]'''
  if theta > 360 :
    theta = theta%360
  elif theta < 0:
    theta = (theta%(-360))+360
    
#  print('The conf is:',[x , y, theta])
  return([x, y, theta])
  
  
def unwrap_wall(room):
  ''' This function takes in a room and unwrap the walls and output them as a line'''
  wallLengthList = []
  for wall in room.walls:
    wallLengthList.append(math.sqrt((wall[0][0]-wall[1][0])**2+(wall[0][1]-wall[1][1])**2))   # length of each wall
#    print(' The wall is: ', wall,'and the calculated length is:',wallLength[-1])
  unwrapLen = sum(wallLengthList) # overall length of the room
#  print(' The length of all walls, or the unwrapped length is: ', unwrapLen)
  return wallLengthList, unwrapLen

def unwrap_sampling(unwrapLen, muWall, sigmaWall):
  ''' This function samples a point on the line with the same length of the unwrapped wall.
  :UnwrapLen: is the length of the unwrapped walls of the room '''
  samplingRange = np.linspace(0, unwrapLen, int(unwrapLen*10)) # possible sampling numbers for placing an object
#  if np.all(muWall == []) and np.all(sigmaWall == []): # First round (No mu or sigma)
  if muWall ==[]:
    sampledPoint = random.choice(samplingRange)
  else:
    sampledPoint = np.random.normal(loc = muWall, scale = sigmaWall)# sample an y for the center of the object in the room
#  print('The chosen point is:', sampledPoint)
  return(sampledPoint)

def wrap_wall(samplePoint, wallList):
  ''' This function is designed to find the point that is sampled on the
  unwrapped wall, on the actual walls of the room'''

  wallSum = [] # sum of the length of the walls , something like fibonacci :D
  for i in range(len(wallList)):
    if i == 0:
      wallSum.append(wallList[0]) # The first element
    else:
      wallSum.append(wallList[i]+wallSum[i-1])
#    print('wallSum:', wallSum)
      
  for i in range(len(wallSum)):
#    print('sample point is:', samplePoint, 'and the wallSum at this iteration is:', wallSum[i])
    if samplePoint < wallSum[i] and i == 0:
      return(0, wallSum)
    if samplePoint < wallSum[i] and samplePoint > wallSum[i-1]:
      return(i, wallSum)
  return(len(wallSum)-1, wallSum) # last wall
      
  
#-------------------  USEFUL AUXILARY FUNCTIONS --------------------------------      


def get_line(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1
    ystep = None
    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(int(x1), int(x2) + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax
    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points

def light_intensity(light_code, object_library):
    obj_df = object_library.loc[object_library['Object Code'] == light_code]
    intensity = obj_df.iloc[0]['Light Intensity']
    return intensity


def object_dimension(object_code, object_library):
    obj_df = object_library.loc[object_library['Object Code'] == object_code]
    length = obj_df.iloc[0]['Length']
    width = obj_df.iloc[0]['Width']
    return length, width

def object_supportLevel(object_code, object_library):
    obj_df = object_library.loc[object_library['Object Code'] == object_code]
    support = obj_df.iloc[0]['Support Level']
    return support
    

def object_name(object_code, object_library):
    ''' This function returns the name of the object using the excel file'''
    obj_df = object_library.loc[object_library['Object Code'] == object_code[0]]
    name = obj_df.iloc[0]['Name']
    return name

def surface_name(object_code, object_library):
    ''' This function returns the name of the floor surface using the excel file'''
    obj_df = object_library.loc[object_library['Object Code'] == object_code]
    name = obj_df.iloc[0]['Notes']
    return name   

def surface_risk(surface_code, object_library):
    ''' This function returns the fall risk corresponding to the chosen surface type '''
    obj_df = object_library.loc[object_library['Object Code'] == surface_code]
    name = obj_df.iloc[0]['Floor Risk Level']
    return name  

#------------------------------------------------------------------------------
#                           MAIN FUNCTIONS    
#------------------------------------------------------------------------------
    
def object_placement(object_code, object_library, room, room_x, room_y, orientation, mu, sigma):
  
  length, width = object_dimension(object_code[0], object_library)
  conf = object_configuration(object_code[0], room_x, room_y, orientation, mu, sigma)
  support = object_supportLevel(object_code[0], object_library)
  name = object_name(object_code, object_library)
  
  return conf, length, width, support, name

def object_placement_againstWall(object_code, object_library, room, orientation, mu, sigma):
  ''' This fuction calls the functions that required to place an object against a wall'''
  length, width = object_dimension(object_code[0], object_library)
  support = object_supportLevel(object_code[0], object_library)
  name = object_name(object_code, object_library)
# ----- Fuctions specific to unwrapping the walls, sampling, and found the projection of the sampled point on the wrapped walls
  wallLenList, unwrapLen = unwrap_wall(room)
  sampledPoint = unwrap_sampling(unwrapLen, mu, sigma)
  # For test
#  sampledPoint = 2
#  sampledPoint = 18
#  sampledPoint = 8
  wallIndex, wallLenSum = wrap_wall(sampledPoint, wallLenList)
  confWall = against_wall_configuration(room, wallIndex, wallLenSum, sampledPoint)
  conf = against_wall_room_conf(confWall, length)
#  conf = against_wall_room_conf(confWall, width)
  
  return conf, length, width, support, name, sampledPoint


def bed_placement(object_code, object_library, orientation, mu, sigma, bedPlacement, room):
    length, width = object_dimension(object_code[0], object_library)
    support = object_supportLevel(object_code[0], object_library)
    name = object_name(object_code, object_library)

    wallLenList, unwrapLen = unwrap_wall(room)
    
    headWall_samplingRange = np.linspace(4.27+5.79, unwrapLen, int((unwrapLen-4.27-5.79)*10)) # possible sampling numbers for placing an object
    footWall_samplingRange = np.linspace(0, 4.27+5.79, int((4.27+5.79)*10)) # possible sampling numbers for placing an object
    samplingRange = headWall_samplingRange if bedPlacement == 'h' else footWall_samplingRange

    if mu ==[]:
      sampledPoint = random.choice(samplingRange)
    else:
      sampledPoint = np.random.normal(loc = mu, scale = sigma)# sample an y for the center of the object in the room
#    print('The chosen point is:', sampledPoint) 
    
    wallIndex, wallLenSum = wrap_wall(sampledPoint, wallLenList)
    confWall = against_wall_configuration(room, wallIndex, wallLenSum, sampledPoint)
    conf = against_wall_room_conf(confWall, length)
    
    return conf, length, width, support, name, sampledPoint

def door_placement(door_code, object_library, room, otherRoom, doorMu, doorSigma):
  ''' This function reurns variables used to place the doors'''
  sampledPoint, config = door_configuration(room, otherRoom, doorMu, doorSigma)
  length, width = object_dimension(door_code[0], object_library)
  support = object_supportLevel(door_code[0], object_library)
  return config, length, width, support, sampledPoint

def light_placement(light_code, object_library, room, lightMu, lightSigma):
    ''' This function returns the position and light density of the chosen light'''
    position = light_position(room, lightMu, lightSigma)
    density = light_intensity(light_code[0], object_library)
    return position, density

def room_surface_initialization(object_library):
    surfaceCode = sample([12,13],1)    # Surface type code (randomly chosen from object library)
    surfaceCode = surfaceCode[0]
    surfaceType = surface_name(surfaceCode, object_library)
    surfaceRisk = surface_risk(surfaceCode, object_library)
    return surfaceCode, surfaceType, surfaceRisk
