

#!/usr/bin/env python
import numpy as np
import pandas as pd
import os

from shapely.geometry import Polygon, Point
from functions_object_placement import door_placement, object_placement, light_placement, room_surface_initialization
from functions_collision_detection import rectangle_vertices, door_polygon, plot_polygon, plot_lights
from functions_collision_detection import collision_detection, door_room_check, door_obj_collision_detection


#############################################################################
#                           CLASSES
#############################################################################

class Environment_Generated():
    ''' This class generates an environment with doors, lights and furniture randomly placed in two rooms, bedroom and bathroom'''
    def __init__(self, mainRoomCodes, bathRoomCodes):
        self.unit_size_m = 0.20 # Grid size in cm (X,Y).
        self.numOfRows = 50 # Number of grids in a Y direction.
        self.numOfCols = 50 # Number of grids in a X direction.
        mainFurnitureCodeArray = mainRoomCodes[0]
        mainDoorsCodeArray = mainRoomCodes[1]
        mainLightCodeArray = mainRoomCodes[2]
        room_name = mainRoomCodes[3]
#        mainRoomVertices = [(0,0), (8,0),(8,10),(0,10)] # Perfect square room -> for testing
        mainRoomVertices = [(0,0), (4.27,0), (4.27, 5.79), (1.93, 5.79), (1.93, 4.57), (1.12, 3.78), (0,3.78)]
        mainRoom = self.Room(room_name, mainRoomVertices)
        
        bathFurnitureCodeArray = bathRoomCodes[0]
        bathDoorsCodeArray = bathRoomCodes[1]
        bathLightCodeArray = bathRoomCodes[2]
        room_name = bathRoomCodes[3]
#        bathRoomVertices = [(8,1), (13,1),(13,7),(8,7)] # Perfect square bethroom-> for testing
        bathRoomVertices = [(0, 3.78), (1.12,3.78), (1.93, 4.57), (1.93, 5.79), (0, 5.79)]
        bathRoom = self.Room(room_name, bathRoomVertices)        
        
        mainLightList = light_installation(mainLightCodeArray, mainRoom)
        mainDoorList = door_collision(mainDoorsCodeArray, mainRoom, bathRoom)
        mainFurnitureList = multiple_object_collision_detection(mainFurnitureCodeArray, mainDoorList, mainRoom)
#       
        bathLightList = light_installation(bathLightCodeArray, bathRoom)
        bathDoorList = door_collision(bathDoorsCodeArray, bathRoom, mainRoom)
        bathFurnitureList = multiple_object_collision_detection(bathFurnitureCodeArray, bathDoorList, bathRoom)
        
        
        self.doorListDict = {"main":mainDoorList, "bath":bathDoorList}
        self.doorList  = create_list_of_objects(mainDoorList, bathDoorList)
        
        self.furnitureListDict = {"main":mainFurnitureList, "bath":bathFurnitureList}
        self.furnitureList  = create_list_of_objects(mainFurnitureList, bathFurnitureList)
#        
        self.lightListDict = {"main":mainLightList, "bath":bathLightList}
        self.lightList  = create_list_of_objects(mainLightList, bathLightList)
        
        self.roomList = []
        self.roomList.append(mainRoom); self.roomList.append(bathRoom)
        
        self.walls = []
        self.floor = np.zeros([self.numOfRows, self.numOfCols]) # Initializing floor_type as a zero matrix with size of number_of_rows * number_of_columns.
        for room in self.roomList:
            self.walls.append(room.wallArray)
            for row in range(self.numOfRows):
                for col in range(self.numOfCols):
                    gridCoordinate = self.grid2meter(col,row)
                    gridPoint = Point(gridCoordinate)
                    if gridPoint.within(room.polygon): # Assigning the floor type based on the room section to each grid in the space
                        self.floor[col, row] = room.surfaceRisk
    def grid2meter(self, col, row):
        x = col*self.unit_size_m
        y = row*self.unit_size_m
        return (x,y)
        

    class Room():
        ''' 
        This class generates rooms as polygons based on the list of vertices
        "vertices" passed to the class and name it "roomName 
        '''
        def __init__(self, roomName, vertices):
            library_file_name = os.path.join(os.getcwd(), 'Object_Library.csv') # The object library file address.
            object_library = pd.read_csv(library_file_name,) # Reading the object library file
            del library_file_name
            # Room Dimensions
            xAxis = []
            yAxis = []
            for item in vertices:
                xAxis.append(item[0])
                yAxis.append(item[1])
            xmin = min(xAxis)
            xmax = max(xAxis)
            ymin = min(yAxis)
            ymax = max(yAxis)
                
            self.x = np.linspace(xmin, xmax, 4*(int(xmax-xmin))+1) # m (the ability of choosing points at each 25cm)
            self.y = np.linspace(ymin, ymax, 4*(int(xmax-xmin))+1) # m (the ability of choosing points at each 25cm)
            self.polygon = Polygon(vertices)
#            print(vertices)
            self.name = roomName
            self.code, self.surfaceType, self.surfaceRisk = room_surface_initialization(object_library)
            self.numWalls, self.walls, self.wallArray = finding_walls(self)
#            plot_polygon(self.polygon)
#            plot_polygon(self.polygon, fignum = 2)
            
        
class FurniturePlacement():
    
    def __init__(self, objects_code, room):
        library_file_name = os.path.join(os.getcwd(), 'Object_Library.csv') # The object library file address.
        object_library = pd.read_csv(library_file_name,) # Reading the object library file
        del library_file_name
        orientation = np.linspace(0.0, 360.0, 361)
        # The created object should be inside the room
        self.code = objects_code
        self.room = room.name
        inside = False
        while inside == False:
            self.conf, self.length, self.width, self.support = object_placement(objects_code, object_library, room.x, room.y, orientation)
            _, _, _, _, self.polygon = rectangle_vertices(self.conf, self.length, self.width)
            _, _, _, _, obj = rectangle_vertices(self.conf, self.length, self.width)
#            plot_polygon(obj)
            inside = room.polygon.contains(obj)


class DoorPlacement():
    
    def __init__(self, door_code, room, otherRoom):
        library_file_name = os.path.join(os.getcwd(), 'Object_Library.csv') # The object library file address.
        object_library = pd.read_csv(library_file_name,) # Reading the object library file
        del library_file_name
        self.code = door_code
        outside = True
        while outside == True:  
            self.conf, self.length, self.width, self.support = door_placement(door_code, object_library, room, otherRoom)
            self.room = room.name
            _, _, _, _, self.polygon = door_polygon(self.conf, self.length, self.width, room)
            _, _, _, _, obj = door_polygon(self.conf, self.length, self.width, room)
#            plot_polygon(obj)
            outside = door_room_check(self, room)

class Lights():
    def __init__(self, light_code, room):
        library_file_name = os.path.join(os.getcwd(), 'Object_Library.csv') # The object library file address.
        object_library = pd.read_csv(library_file_name,) # Reading the object library file
        del library_file_name
        self.code = light_code
        self.room = room.name
        inside = False
        while inside == False:
            self.pos, self.intensity = light_placement(light_code, object_library, room)
            self.point = Point(self.pos)
            light_source = self.point
#            plot_lights(light_source)
            inside = room.polygon.contains(light_source)

#############################################################################
#                           FUNCTIONS/METHODS
#############################################################################
def finding_walls(room):
    '''
    This function finds the number and coordinates of the input parameter "room" as walls
    it finds each side of the rooms polygon and recognizes them as walls
    '''
    num_walls = len(room.polygon.exterior.coords[:-1])  # counts the side of the rooms polygon -> number of walls
    available_walls = (np.linspace(0, num_walls-1, num_walls)).astype(int) # create a list of walls for sampling
#    print(available_walls)
    wall_list = []
    wall_arrayType = []
    for wall in available_walls:
        # find the position of the center of the door
        if wall == num_walls-1:
    #        print("last wall")
            wall_coords = [(room.polygon.exterior.coords[:-1][wall][0], room.polygon.exterior.coords[:-1][wall][1]),
                           (room.polygon.exterior.coords[:-1][0][0], room.polygon.exterior.coords[:-1][0][1])]
            wall_array = [room.polygon.exterior.coords[:-1][wall][0], room.polygon.exterior.coords[:-1][wall][1],
                           room.polygon.exterior.coords[:-1][0][0], room.polygon.exterior.coords[:-1][0][1]]
        else:
            wall_coords = [(room.polygon.exterior.coords[:-1][wall][0], room.polygon.exterior.coords[:-1][wall][1]),
                           (room.polygon.exterior.coords[:-1][wall+1][0], room.polygon.exterior.coords[:-1][wall+1][1])]
            wall_array = [room.polygon.exterior.coords[:-1][wall][0], room.polygon.exterior.coords[:-1][wall][1],
                          room.polygon.exterior.coords[:-1][wall+1][0], room.polygon.exterior.coords[:-1][wall+1][1]]
        wall_list.append(wall_coords)
        wall_arrayType.append(wall_array)
    return num_walls, wall_list, wall_arrayType

def door_collision(door_code_array, room, otherRoom):
    '''
    This function checks the collision between multiple objects that have been sent 
    to this function as a list of objects
    :param objects_code_array: an array of the objects code of interest (the codes
    can be retrived from the corresponding object library csv file)
    :param obj_list: list of objects that are placed in the room
    '''
    #creating a list of objects
    door_list = []
    for door_code in door_code_array:
        door_list.append(DoorPlacement([door_code], room, otherRoom))    # list of the objects in the room
        restart = True
        while restart == True:  # Making sure it checks the collision between all objects even after resampling
            restart = False
            for door in door_list[:-1]:
                collision_bool = door_obj_collision_detection(door, door_list[-1])
    #            print("checking collision between ", obj.code, "and, ", obj_list[-1].code)
                if collision_bool == True:  # If the new object is colliding with any of the existing objects, recreate the latest object and assign new configuration to it
    #                print("Collision detected between objects ", obj.code, " and ", obj_list[-1].code )
                    door_list[-1] = DoorPlacement([door_code], room, otherRoom)
                    restart = True
                
    return door_list

def multiple_object_collision_detection(objects_code_array, door_list, room):
    '''
    This function checks the collision between multiple objects that have been sent 
    to this function as a list of objects
    :param objects_code_array: an array of the objects code of interest (the codes
    can be retrived from the corresponding object library csv file)
    :param obj_list: list of objects that are placed in the room
    '''
    #creating a list of objects
    obj_list = []
    for obj_code in objects_code_array:
        obj_list.append(FurniturePlacement([obj_code], room))    # list of the objects in the room
        restart = True
        while restart == True:  # Making sure it checks the collision between all objects even after resampling
            restart = False
            for obj in obj_list[:-1]:
                collision_obj = collision_detection(obj, obj_list[-1])    
#                print("checking collision between object", obj.code, "and object, ", obj_list[-1].code)
                if collision_obj == True:  # If the new object is colliding with any of the existing objects, recreate the latest object and assign new configuration to it
#                    print("COLLISION detected between objects ", obj.code, " and ", obj_list[-1].code )
                    obj_list[-1] = FurniturePlacement([obj_code], room)
                    restart = True
            for door in door_list:
                collision_door = door_obj_collision_detection(door, obj_list[-1])
#                print("checking collision between door", door.code, "and object, ", obj_list[-1].code)
                if collision_door == True:  # If the new object is colliding with any of the existing objects, recreate the latest object and assign new configuration to it
                    obj_list[-1] = FurniturePlacement([obj_code], room)
#                    print("COLLISION detected between door ", door.code, " and object ", obj_list[-1].code)
                    restart = True
    return obj_list

def light_installation(light_code_array, room):
    light_list = []
    for light_code in light_code_array:
        light_list.append(Lights([light_code], room))
    restart = True
    while restart == True:
        restart = False
        for light in light_list[:-1]:
            if light.pos == light_list[-1].pos:
                light_list[-1] = Lights([light_code], room)
                restart = True
    return light_list

def create_list_of_objects(main, bath):
    '''
    This function takes in a list of furniture for main room and bathroom 
    and save them in a list (instead of a list of lists)
    '''
    list =[]
    for item in main:
        list.append(item)
    for item in bath:
        list.append(item)
    return list


