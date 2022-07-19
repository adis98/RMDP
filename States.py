import numpy as np
from enum import Enum

class EdgeType(Enum):
    horizontal = 0
    vertical = 1

def getPreDecisionState(vehicleLocations, vehicleRoutes, currTime, mapSize):
    vlocarray = np.array(vehicleLocations).flatten()
    routestensor = convertRoutesToGraph(vehicleRoutes, mapSize)
    flattened_routes = routestensor.flatten()
    state = np.concatenate((vlocarray, flattened_routes))
    state = np.concatenate((state, np.array([currTime])))
    return state


def convertRoutesToGraph(vehicleRoutes, mapSize):
    n = mapSize
    graphDimEdgeNum = int(2*(n-1)*(n))
    graphDimVehicleCount = int(len(vehicleRoutes))
    graph = np.zeros((graphDimEdgeNum, graphDimVehicleCount), dtype=int)
    for vehicle in range(len(vehicleRoutes)):
        prev = None
        for order in vehicleRoutes[vehicle]:
            print("tanananana")
            if (prev is None):
                first = np.array([order.restaurantX, order.restaurantY])
            else:
                first = prev
            second = np.array([order.customerX, order.customerY])
            edge, sign = convertCoordinateToEdgeIndexAndSign(first, second, mapSize)
            print(edge)
            graph[edge, vehicle] = sign
            prev = second
    return graph





def convertEdgeIndexToCoordinates(val, mapSize, sign):  # val is the edge index, sign is +/-1 or 0
    n = mapSize
    if val < n * (n - 1):
        base_x = val // (n - 1)
        base_y = val % (n - 1)
        first = np.array([base_x, base_y])
        second = first + sign * (np.array([0, 1]))
        if sign < 0:
            first = first + np.array([0,1])
            second = second + np.array([0,1])
    else:
        rem = val % (n * (n - 1))
        base_y = rem // (n - 1)
        base_x = rem % (n - 1)
        first = np.array([base_x, base_y])
        second = first + sign * (np.array([1, 0]))
        if sign < 0:
            first = first + np.array([1,0])
            second = second + np.array([1,0])
    return first, second

def convertCoordinateToEdgeIndexAndSign(first, second, mapSize): #first and second are numpy arrays
    n = mapSize
    difference = second - first
    if(difference[0] != 0):
        type = EdgeType.horizontal
    elif(difference[1] != 0):
        type = EdgeType.vertical

    if np.sum(difference) < 0:
        sign = -1
        first = second #swap
    else:
        sign = 1

    if(type == EdgeType.horizontal):
        rem = (n-1)*first[1] + first[0]
        val = rem + n*(n-1)
    elif(type == EdgeType.vertical):
        val = (n-1)*first[0] + first[1]

    return int(val), sign




