import numpy as np


def computeReward(initCost, bestCost):
    return initCost - bestCost


def getPreDecisionState(vehicleLocations, vehicleHops, currTime, mapSize):
    routesTensor = convertHopsToGraph(vehicleHops, mapSize, vehicleLocations)
    flattened_routes = routesTensor.flatten()
    state = np.concatenate((flattened_routes, np.array([currTime])))
    return state


def convertHopsToGraph(vehicleHops, mapSize, vehicleLocations):
    n = mapSize
    graphDimEdgeNum = int(2 * (n - 1) * n)
    graphDimVehicleCount = int(len(vehicleHops))
    graph = np.zeros((graphDimEdgeNum, graphDimVehicleCount), dtype=int)
    for vehicle in range(len(vehicleHops)):
        currLoc = vehicleLocations[vehicle]
        for hop in vehicleHops[vehicle]:
            hop = hop[:2]
            edges, signs = convertCoordinateToEdgeIndexAndSign(currLoc, hop, mapSize)
            cols = np.array([vehicle] * len(edges))
            if len(edges) != 0:
                graph[edges, cols] = np.array(signs)
            currLoc = hop
    return graph


def convertEdgeIndexToCoordinates(val, mapSize, sign):  # val is the edge index, sign is +/-1 or 0
    n = mapSize
    if val < n * (n - 1):
        base_x = val // (n - 1)
        base_y = val % (n - 1)
        first = np.array([base_x, base_y])
        second = first + sign * (np.array([0, 1]))
        if sign < 0:
            first = first + np.array([0, 1])
            second = second + np.array([0, 1])
    else:
        rem = val % (n * (n - 1))
        base_y = rem // (n - 1)
        base_x = rem % (n - 1)
        first = np.array([base_x, base_y])
        second = first + sign * (np.array([1, 0]))
        if sign < 0:
            first = first + np.array([1, 0])
            second = second + np.array([1, 0])
    return first, second


def convertCoordinateToEdgeIndexAndSign(source, destination, mapSize):  # first and second are numpy arrays
    n = mapSize
    edges = []
    signs = []
    currPos = np.array(source)
    difference = np.array(destination) - currPos
    while not np.array_equal(difference, np.array([0, 0])):
        if difference[0] != 0:  # if theres some movement needed along the X-axis
            if difference[0] < 0:
                sign = -1
                edgeIndex = currPos[1] * (n - 1) + currPos[0] - 1
                currPos[0] -= 1
            else:
                sign = 1
                edgeIndex = currPos[1] * (n - 1) + currPos[0]
                currPos[0] += 1

        elif difference[1] != 0:  # scope for movement along Y
            if difference[1] < 0:
                sign = -1
                edgeIndex = n * (n - 1) + currPos[0] * (n - 1) + currPos[1] - 1
                currPos[1] -= 1
            else:
                sign = 1
                edgeIndex = n * (n - 1) + currPos[0] * (n - 1) + currPos[1]
                currPos[1] += 1
        edges.append(int(edgeIndex))
        signs.append(int(sign))
        difference = np.array(destination) - currPos
    return edges, signs
