import random
from OrderGenerator import Order
from States import getPreDecisionState

def vehicleSelector(order, vehicleLocations, vehicleRoutes, numVehicles, currTime):

    pre_decision_state = getPreDecisionState(vehicleLocations, vehicleRoutes, currTime)
    return random.randint(0,numVehicles-1) #returns a number from 0 to numVehicles-1 to indicate which vehicle has been selected

