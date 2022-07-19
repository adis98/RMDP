import numpy as np

def getPreDecisionState(vehicleLocations, vehicleRoutes, currTime):
    numV = len(vehicleLocations)
    vlocarray = np.array(vehicleLocations)
    routestensor =  convertRoutesToGraph(vehicleRoutes)

def convertRoutesToGraph(vehicleRoutes):
    return None